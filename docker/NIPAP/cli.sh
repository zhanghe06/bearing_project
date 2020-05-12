#!/usr/bin/env bash

NET_NAME="nipap"

docker run \
    -it \
    --rm \
    --net "${NET_NAME}" \
    nipap/postgres-ip4r:latest \
    psql -h nipap-db -U www -d nipap

# 123456
