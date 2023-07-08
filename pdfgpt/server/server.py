import os
import openai
import json
import pypdf
from flask import Flask, request
from dotenv import load_dotenv, find_dotenv
import shutil

import utils
from langchain.vectorstores.faiss import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings


# load envorinment varibles
_ = load_dotenv(find_dotenv())  # read local .env file
openai.api_key = os.environ['OPENAI_API_KEY']

app = Flask(__name__)


@app.route('/api/message', methods=['POST'])
def send_message():
    message = eval(request.data.decode("utf-8"))
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message['message']}]
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
    pdf_file = request.data.decode("utf-8")
    list_of_texts = utils.read_PDF_PyPDF(pdf_file)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2")
    docsearch: FAISS = FAISS.from_texts(texts, embeddings)
    FAISS_SAVE_DIR = './public/FAISS/faiss_index'
    docsearch.save_local(FAISS_SAVE_DIR)
    data = {"FAISS_directory": FAISS_SAVE_DIR}
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json',
    )
    return response


if __name__ == '__main__':
    app.run(port=5328)
