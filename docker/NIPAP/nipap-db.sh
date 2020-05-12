#!/usr/bin/env bash

NET_NAME="nipap"

# docker pull postgres:9.5
# docker pull nipap/postgres-ip4r:latest

docker run \
    -h nipap-db \
    --name nipap-db \
    --net "${NET_NAME}" \
    -v ${PWD}/data:/var/lib/postgresql/data \
    -e POSTGRES_USER='www' \
    -e POSTGRES_PASSWORD='123456' \
    -e POSTGRES_DB='nipap' \
    -p 5432:5432 \
    -d nipap/postgres-ip4r:latest
