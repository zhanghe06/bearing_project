#!/usr/bin/env bash

[ -d ${PWD}/conf ] || mkdir -p ${PWD}/conf

docker run \
    --name prometheus \
    -d \
    -p 9090:9090 \
    -v ${PWD}/conf/prometheus.yml:/etc/prometheus/prometheus.yml \
    prom/prometheus
