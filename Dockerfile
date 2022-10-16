FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apk add libmagic

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

COPY .env.prod .env

RUN ["chmod", "+x", "/code/docker-entrypoint.sh"]

ENTRYPOINT [ "/code/docker-entrypoint.sh" ]