FROM python:3.11.4-alpine3.18

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk --no-cache --update add build-base python3-dev linux-headers
RUN pip install --upgrade pip

WORKDIR /project

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
