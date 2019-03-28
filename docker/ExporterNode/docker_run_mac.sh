#!/usr/bin/env bash

docker run \
    --name node-exporter \
    -d \
    -p 9100:9100 \
    prom/node-exporter
