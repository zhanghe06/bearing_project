#!/usr/bin/env bash

docker build \
    --rm=true \
    -t fluentd:plugin_es \
    -f Dockerfile .
