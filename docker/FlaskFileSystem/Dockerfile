FROM python:2.7
MAINTAINER zhanghe "zhang_he06@163.com"

RUN apt-get update && apt-get install -qy --no-install-recommends \
    python-dev \
    vim \
    ntpdate \
    net-tools

ADD ./ /project
RUN pip install Flask && pip install supervisor

EXPOSE 5000 9001

WORKDIR /project
