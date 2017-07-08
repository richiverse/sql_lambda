FROM lambci/lambda:build-python2.7

MAINTAINER "rich fernandez" <richardfernandeznyc@gmail.com>

RUN yum clean all && \
    yum -y install \
    python27-devel python27-virtualenv \
    postgresql postgresql-devel freetds-devel gcc \


COPY yum.conf /etc/yum.conf
COPY bashrc /root/.bashrc

WORKDIR /var/task

COPY requirements.txt /var/task

RUN rm -rf ./venv && \
    virtualenv venv && \
    . ./venv/bin/activate && \
    pip install -U pip && \
    pip install -U zappa && \
    pip install -r requirements.txt && \
    deactivate

COPY . /var/task
