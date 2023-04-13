FROM python:3.12.0a7-alpine3.17

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip

WORKDIR /project

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
