FROM python:3.10.4

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt
