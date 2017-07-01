FROM lambci/lambda:build

MAINTAINER "rich fernandez" <richardfernandeznyc@gmail.com>


COPY docker/yum.conf /etc/yum.conf
COPY docker/bashrc /root/.bashrc

RUN yum clean all && \
    yum -y install python27-devel python27-pip gcc \
      vim \
      # Your specific system requirements below
      postgresql postgresql-devel freetds-dev 

WORKDIR /var/task
COPY . /var/task

RUN pip install -U pip
RUN pip install -U virtualenv

RUN virtualenv venv && \
    . ./venv/bin/activate && \
    pip install -U pip && \
    pip install -U zappa && \
    pip install -r requirements.txt 
    # pip install pandas sqlalchemy
