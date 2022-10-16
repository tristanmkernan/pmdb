FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apk add libmagic
RUN apk add jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers
RUN apk add libffi-dev

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

COPY .env.prod .env

RUN ["chmod", "+x", "/code/docker-entrypoint.sh"]

ENTRYPOINT [ "/code/docker-entrypoint.sh" ]