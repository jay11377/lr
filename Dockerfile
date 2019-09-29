FROM python:3.7.3-stretch

ENV PYTHONUNBUFFERED 1

ARG REQUIREMENTS_FILENAME=base

RUN apt-get update && apt-get install -y \
  gettext \
  libpq-dev

COPY ./requirements /requirements

RUN pip install --upgrade pip && pip install -r /requirements/${REQUIREMENTS_FILENAME}.txt
RUN pip install https://github.com/darklow/django-suit/tarball/v2
RUN pip install pillow

WORKDIR /code
COPY ./src/ /code/
