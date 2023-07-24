import os
import openai
import json
import shutil
import functools
import pandas as pd

import utils
import parse_pdf_V2 as parser
from DBClient import DBClient

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
host = os.environ.get("DB_SUPABASE_URL")
port = os.environ.get("DB_SUPABASE_PORT")
password = os.environ.get("DB_SUPABASE_PASSWORD")
client = DBClient(host=host, port=port, password=password)
TABLE_NAME = 'documents'
# url: str = os.environ.get("DB_SUPABASE_URL")
# key: str = os.environ.get("DB_SUPABASE_KEY")
# supabase: Client = create_client(url, key)  # Note: By default, Supabase projects return a maximum of 1,000 rows. This setting can be changed in your project's API settings.

# create hugging face sentence-transformer model
K = 8
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
    if client.is_not_empty(TABLE_NAME):
        # 1. load data from DB
        query = f"SELECT * FROM {TABLE_NAME}"
        df = client.query_to_df(query)
        text_objects = df.to_dict('records')
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
    return json.dumps(chat_msg)


@app.route('/api/document', methods=['POST', 'PUT'])
def upload_document():
    ''' 1. convert document to paragraphs
    2. collect metadata
    3. create embedings
    4. combine data
    5. save to database. Database has fields: title, page, content, embedding (leter we will add: user_id, session_id)
    6. send response
    '''
    request_body = eval(request.data.decode("utf-8"))
    if request.method == 'POST':
        for pdf_file, pdf_name in zip(request_body['filepath'], request_body['filename']):
            # 1. convert documents to paragraphs
            text_objects = parser.get_paragraphs(
                pdf_file, pdf_name, long=False)
            # 2. collect metadata
            texts, metadata = utils.get_metadata(text_objects)
            # 3. create embeddings
            embeddings = embedding_model.embed_documents(texts)
            # 4. combine data
            text_objects = [dict(item, embedding=embed)
                            for item, embed in zip(text_objects, embeddings)]
        # 5. save to the database
        df = pd.DataFrame(text_objects)
        print(df[:2])
        # perhaps i should make sure no duplicates are stored. I will do that later using: user_id, and session_id as keys.
        client.write(df, TABLE_NAME, if_exists="append")
        df2 = client.query_to_df("SELECT * FROM documents")
        print(df2[:2])
        # 6. sent response to front end client
        response = app.response_class(
            response=json.dumps('success'),
            status=200,
            mimetype='application/json',
        )
        return response

    elif request.method == 'PUT':
        query = f"DELETE FROM test WHERE title={request_body['filename']}"
        # DELETE FROM <table_name> WHERE <condition>


if __name__ == '__main__':
    app.run(port=os.environ.get("BACKEND_PORT"))
