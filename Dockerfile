FROM python:3.6-slim

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /app/
RUN pip install --upgrade pip \
  && pip install -r /app/requirements.txt

COPY ./manage.py /app/
COPY ./cognosaurus /app/cognosaurus

WORKDIR /app/
