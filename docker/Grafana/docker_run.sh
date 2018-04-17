#!/usr/bin/env bash

docker run \
    -h=grafana \
    --name=grafana \
    -p 3000:3000 \
    -d \
    grafana/grafana:5.0.4
