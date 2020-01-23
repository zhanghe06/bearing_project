#!/usr/bin/env bash

docker build \
    --rm=true \
    -t nginx:logrotate \
    -f Dockerfile .
