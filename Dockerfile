FROM python:3.12.0a7-alpine3.17

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev python3-dev build-base \
    sox ffmpeg cairo cairo-dev texlive-full

# Зависимости для Pillow
RUN apk add tiff-dev jpeg-dev openjpeg-dev zlib-dev freetype-dev lcms2-dev \
    libwebp-dev tcl-dev tk-dev harfbuzz-dev fribidi-dev libimagequant-dev \
    libxcb-dev libpng-dev
    
RUN pip install --upgrade pip

WORKDIR /project

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
