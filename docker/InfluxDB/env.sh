#!/usr/bin/env bash

docker run \
    --rm \
    --link=influxdb \
    -it \
    influxdb:1.4.2 \
    env
