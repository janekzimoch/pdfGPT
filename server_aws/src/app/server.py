from fastapi.security import HTTPAuthorizationCredentials
import jwt
import os
import openai
import time

import app.utils as utils
import app.parse_pdf as parser
from app.auth_utils import (access_token, get_user_id)

from fastapi import FastAPI, UploadFile, File, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv, find_dotenv
from supabase import create_client, Client
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

# load envorinment varibles
_ = load_dotenv(find_dotenv())  # read local .env file
openai.api_key = os.environ['OPENAI_API_KEY']


app = FastAPI()


# Set allowed origins and HTTP methods for CORS
origins = [
    "http://localhost",
    "http://localhost:3000",  # Replace with your frontend URL
    "https://pdf-gpt-eta.vercel.app",
    "http://pdf-gpt-eta.vercel.app",
    "http://gptlegal.net",
    "https://gptlegal.net",
    "http://www.gptlegal.net",
    "https://www.gptlegal.net",
    "https://www.gptlegal.net/app",
    "http://0.0.0.0",
    "http://0.0.0.0:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


class Message(BaseModel):
    client: str
    message: str
    paragraphs: List[str]


class Documents(BaseModel):
    filepath: List[str]
    filename: List[str]


class DocumentName(BaseModel):
    filename: str


@app.get("/")
async def health_check():
    return {"status": "root healthy"}


@app.get("/health")
async def health_check():
    return {"status": "health healthy"}


@app.post('/api/message')
async def send_message(message: Message, token: str = Depends(access_token)):
    ''' 1. load data from the DB
    2. retirve embeddings
    3. create the FAISS
    4. search for query
    5. formulate a prompt
    '''
    # message = eval(request.data.decode("utf-8"))
    print(message)
    utils.user_login(supabase, token)
    if utils.is_not_empty(supabase):
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
        query = message.message
        docs_with_score = docsearch.similarity_search_with_score(query, k=K)
        for doc, scr in docs_with_score:
            print('score: ', scr)
            print(doc.page_content, '\n')
        # 5. formulate a prompt
        prompt = utils.formulate_prompt(query, docs_with_score)
        paragraphs = [{'paragraph': doc.page_content, 'page': doc.metadata['page'], 'title': doc.metadata['title']}
                      for doc, scr in docs_with_score]
    else:
        prompt = message.message
        paragraphs = []
    print(prompt)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    response_content = response.choices[0].message.content
    chat_msg = {
        "client": "chat",
        "message": response_content,
        "paragraphs": paragraphs
    }
    utils.user_logout(supabase, key)
    return chat_msg


@app.put('/api/document')
async def remove_document(request_body: DocumentName, token: str = Depends(access_token)):
    print(request_body)
    utils.user_login(supabase, token)
    data = supabase.table(TABLE_NAME).delete().eq(
        "title", request_body.filename).execute()
    # 6. sent response to front end client
    utils.user_logout(supabase, key)
    return {'success'}


@app.post('/api/document')
# , user_id: str = Depends(get_user_id)
async def upload_document(files: List[UploadFile] = File(...), token: str = Depends(access_token), user_id: str = Depends(get_user_id)):
    utils.user_login(supabase, token)
    for file in files:
        pdf_name = file.filename
        pdf_file = 'temp.pdf'
        with open(pdf_file, "wb") as f:
            f.write(await file.read())
        # 1. convert documents to paragraphs
        text_objects = parser.get_paragraphs(
            pdf_file, pdf_name, long=True)
        # 2. collect metadata
        texts, metadata = utils.get_metadata(text_objects)
        # 3. create embeddings
        embeddings = embedding_model.embed_documents(texts)
        # 4. combine data
        text_objects = [dict(item, embedding=embed, session_id=0, user_id=user_id)
                        for item, embed in zip(text_objects, embeddings)]
        # remove temorary file
        os.remove(pdf_file)
    # 5. save to the database
    data = supabase.table(TABLE_NAME).insert(text_objects).execute()
    # 6. sent response to front end client
    utils.user_logout(supabase, key)
    return {'success'}


@app.get('/api/document')
async def get_documents(token: str = Depends(access_token)):
    utils.user_login(supabase, token)
    data = supabase.table(TABLE_NAME).select('*').execute()
    text_objects = data.data
    unique_titles = list({par['title'] for par in text_objects})
    utils.user_logout(supabase, key)
    return {'unique_titles': unique_titles}
