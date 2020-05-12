#!/usr/bin/env bash

NET_NAME="nipap"

# docker pull nipap/nipapd:v0.29.6

docker run \
    -h nipapd \
    --name nipapd \
    --net "${NET_NAME}" \
    -e DB_HOST='nipap-db' \
    -e DB_PORT='5432' \
    -e DB_USERNAME='www' \
    -e DB_PASSWORD='123456' \
    -e DB_NAME='nipap' \
    -e NIPAP_USERNAME='admin' \
    -e NIPAP_PASSWORD='123456' \
    -p 1337:1337 \
    -d nipap/nipapd:v0.29.6


#   DB_HOST             host where database is running
#   DB_PORT             port of database [5432]
#   DB_NAME             name of database
#   DB_USERNAME         username to authenticate to database
#   DB_PASSWORD         password to authenticate to database
#   DB_SSLMODE          require ssl? [disable]
#   NIPAP_USERNAME      name of account to create
#   NIPAP_PASSWORD      password of account to create

