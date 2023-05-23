#FROM ubuntu:18.04
#RUN apt-get update && \
#    apt-get install --no-install-recommends -y gcc && \
#    apt-get clean && rm -rf /var/lib/apt/lists/*


FROM python:3.6-alpine

RUN set -eux && sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && \
    apk add --no-cache -U build-base linux-headers openldap-dev mysql-dev && \
    rm -rf /var/cache/apk/*
