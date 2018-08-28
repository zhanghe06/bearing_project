#!/usr/bin/env bash

[ -d ${PWD}/data ] || mkdir -p ${PWD}/data

docker run \
    -h redis \
    --name redis \
    -v ${PWD}/data:/data \
    -e REDIS_PORT='6379' \
    -e REDIS_PASSWORD='123456' \
    -p 6379:6379 \
    -d \
    redis:3.2.8 \
    sh -c 'exec redis-server --port "$REDIS_PORT" --requirepass "$REDIS_PASSWORD"'
