FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "5328"]
# run outside of docker: uvicorn app.server:app --port 5328 