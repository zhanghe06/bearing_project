#!/usr/bin/env bash

rm -rf uploads

docker build \
    --rm=true \
    -t flask_file_system \
    -f Dockerfile .
