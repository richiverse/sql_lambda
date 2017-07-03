FROM python:3.6

MAINTAINER "rich fernandez" <richardfernandeznyc@gmail.com>

RUN apt update && \
    apt install postgresql postgresql-devel freetds-dev 

WORKDIR /var/task
COPY . /var/task

RUN python3.6 -m venv venv && \
    . ./venv/bin/activate && \
    pip install -U pip && \
    pip install -U zappa && \
    pip install -r requirements.txt 
