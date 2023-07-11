import os
import openai
import json
import pypdf
from flask import Flask, request
from dotenv import load_dotenv, find_dotenv
import shutil
import functools

import utils
from langchain.vectorstores.faiss import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings


# load envorinment varibles
_ = load_dotenv(find_dotenv())  # read local .env file
openai.api_key = os.environ['OPENAI_API_KEY']

app = Flask(__name__)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2")
K = 5


def formulate_prompt(query, docs_with_score):
    # # " Try to be quite descriptive but without repeating yourself or making things up. " + \
    prompt = "You are a system to answer questions about some documents. " + \
        "You don't have access to the entire document, but the most relevant exerpts from the document will be provided to you for reference, alongside with scores of how relevant those texts are to the question asked. The lower the score the more relevant the exerpt is according to some imperfect scoring technique. " + \
        "You are required to answer truthfully and acklowedge so when you don't know the answer " + \
        " or provided texts do not provide you with enought context to make a confident answer. " + \
        "\n" + \
        f"The question is: {query} \n" + \
        "Here are the most relevant exerpts and their scores: \n" + \
        ('\n').join([f"Exerpt: {doc.page_content}; Score: " +
                     str(round(scr, 3)) for doc, scr in docs_with_score])
    return prompt


@app.route('/api/message', methods=['POST'])
def send_message():
    message = eval(request.data.decode("utf-8"))
    FAISS_SAVE_DIR = message['FAISS']['FAISS_SAVE_DIR']
    print(FAISS_SAVE_DIR)
    print(len(FAISS_SAVE_DIR))
    if len(FAISS_SAVE_DIR) != 0:
        print('using faiss')
        vectorstores = [FAISS.load_local(faiss_dir, embeddings)
                        for faiss_dir in FAISS_SAVE_DIR]
        docsearch = functools.reduce(lambda x, y: (
            z := x).merge_from(y) or z, vectorstores)
        query = message['message']['message']
        docs_with_score = docsearch.similarity_search_with_score(query, k=K)
        for doc, scr in docs_with_score:
            print('score: ', scr)
            print(doc.page_content, '\n')
        prompt = formulate_prompt(query, docs_with_score)
    else:
        prompt = message['message']['message']
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
    }
    return json.dumps(chat_msg)


@app.route('/api/document', methods=['POST'])
def upload_document():
    pdf_files = eval(request.data.decode("utf-8"))
    faiss_paths = []
    for pdf_file, pdf_name in zip(pdf_files['filepath'], pdf_files['filename']):
        list_of_texts = utils.read_PDF_PyMuPDF(pdf_file)
        list_of_texts = utils.remove_end_of_lines(list_of_texts)
        list_of_texts = utils.remove_short_chunks(list_of_texts)
        print('Number of paragraphs loaded: ', len(list_of_texts))
        print('creating FAISS...')
        docsearch: FAISS = FAISS.from_texts(list_of_texts, embeddings)
        FAISS_SAVE_DIR = f"./public/FAISS/{pdf_name}"
        print(FAISS_SAVE_DIR, '\n')
        docsearch.save_local(FAISS_SAVE_DIR)
        faiss_paths.append(FAISS_SAVE_DIR)
    data = {"FAISS_SAVE_DIR": faiss_paths}
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json',
    )
    return response


if __name__ == '__main__':
    app.run(port=5328)
