FROM python:3.8-slim

WORKDIR /backend

COPY ./requirements.txt /backend/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt

COPY . /backend

ENV PYTHONPATH="$PATH:/backend"

EXPOSE 8000
