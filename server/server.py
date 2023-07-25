import os
import openai
import json
import shutil
import functools

import utils
import parse_pdf as parser

from flask import Flask, request
from dotenv import load_dotenv, find_dotenv
from supabase import create_client, Client
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

# load envorinment varibles
_ = load_dotenv(find_dotenv())  # read local .env file
openai.api_key = os.environ['OPENAI_API_KEY']


app = Flask(__name__)

# create supbabase client using sqlalchemy
TABLE_NAME = 'documents'
url: str = os.environ.get("DB_SUPABASE_URL")
key: str = os.environ.get("DB_SUPABASE_KEY")
# Note: By default, Supabase projects return a maximum of 1,000 rows. This setting can be changed in your project's API settings.
supabase: Client = create_client(url, key)

# create hugging face sentence-transformer model
K = 12
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2")


@app.route('/api/message', methods=['POST'])
def send_message():
    ''' 1. load data from the DB
    2. retirve embeddings
    3. create the FAISS
    4. search for query
    5. formulate a prompt
    '''
    message = eval(request.data.decode("utf-8"))
    user = utils.user_login(supabase)
    if utils.is_not_empty():
        # 1. load data from DB
        data = supabase.table(TABLE_NAME).select("*").execute()
        text_objects = data.data
        # 2. retrive embeddings
        embeddings = [par['embedding'] for par in text_objects]
        texts, metadata = utils.get_metadata(text_objects)
        # 3. create FAISS
        text_embedding_pairs = list(zip(texts, embeddings))
        docsearch = FAISS.from_embeddings(
            text_embedding_pairs, embedding_model, metadatas=metadata)
        # 4. search for the query
        query = message['message']['message']
        docs_with_score = docsearch.similarity_search_with_score(query, k=K)
        for doc, scr in docs_with_score:
            print('score: ', scr)
            print(doc.page_content, '\n')
        # 5. formulate a prompt
        prompt = utils.formulate_prompt(query, docs_with_score)
        paragraphs = [{'paragraph': doc.page_content, 'page': doc.metadata['page'], 'title': doc.metadata['title']}
                      for doc, scr in docs_with_score]
    else:
        prompt = message['message']['message']
        paragraphs = []
    print(prompt)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    response_content = response.choices[0].message.content
    chat_msg = {
        "client": "chat",
        "time": 1000,
        "message": response_content,
        "paragraphs": paragraphs
    }
    utils.user_logout(supabase, key)
    return json.dumps(chat_msg)


@app.route('/api/document', methods=['POST', 'PUT', 'GET'])
def upload_document():
    user = utils.user_login(supabase)
    if request.method == 'POST':
        request_body = eval(request.data.decode("utf-8"))
        for pdf_file, pdf_name in zip(request_body['filepath'], request_body['filename']):
            # 1. convert documents to paragraphs
            text_objects = parser.get_paragraphs(
                pdf_file, pdf_name, long=True)
            # 2. collect metadata
            texts, metadata = utils.get_metadata(text_objects)
            # 3. create embeddings
            embeddings = embedding_model.embed_documents(texts)
            # 4. combine data
            text_objects = [dict(item, embedding=embed, session_id=0, user_id=user.user.id)
                            for item, embed in zip(text_objects, embeddings)]
        # 5. save to the database
        data = supabase.table(TABLE_NAME).insert(text_objects).execute()
    elif request.method == 'PUT':
        request_body = eval(request.data.decode("utf-8"))
        request_body = eval(request_body)
        data = supabase.table(TABLE_NAME).delete().eq(
            "title", request_body['filename']).execute()
    elif request.method == 'GET':
        unique_titles = None
        data = supabase.table(TABLE_NAME).select('*').execute()
        text_objects = data.data
        unique_titles = list({par['title'] for par in text_objects})
        response = app.response_class(
            response=json.dumps({
                'unique_titles': unique_titles
            }),
            status=200,
            mimetype='application/json',
        )
        utils.user_logout(supabase, key)
        return response
    # 6. sent response to front end client
    response = app.response_class(
        response=json.dumps('success'),
        status=200,
        mimetype='application/json',
    )
    utils.user_logout(supabase, key)
    return response


if __name__ == '__main__':
    app.run(port=os.environ.get("BACKEND_PORT"))
