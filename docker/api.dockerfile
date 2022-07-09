FROM python:3.10.1-buster
ENV PYTHONUNBUFFERED 1

WORKDIR /api

COPY ./api/requirements.txt /api/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
