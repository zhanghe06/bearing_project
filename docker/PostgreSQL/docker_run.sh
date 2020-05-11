#!/usr/bin/env bash

docker run \
    -h postgres \
    --name postgres \
    -v ${PWD}/data:/var/lib/postgresql/data \
    -e POSTGRES_USER='www' \
    -e POSTGRES_PASSWORD='123456' \
    -e POSTGRES_DB='project' \
    -p 5432:5432 \
    -d postgres:9.6

# --network some-network
