FROM python:36-slim

MAINTAINER "rich fernandez" <richardfernandeznyc@gmail.com>

WORKDIR /var/task
COPY . /var/task

RUN python3.6 -m venv venv && \
    . ./venv/bin/activate && \
    pip install -U pip && \
    pip install -U zappa && \
    pip install -r requirements.txt 
