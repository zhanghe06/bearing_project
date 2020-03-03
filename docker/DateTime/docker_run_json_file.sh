#!/usr/bin/env bash

docker rm -f datetime

docker run \
    -h datetime \
    --name datetime \
    -d \
    python:2.7 sh -c "while true
do
date +'%Y-%m-%d %H:%M:%S'
sleep 1
done"
