#!/usr/bin/env bash

docker run \
    -h alertmanager \
    --name alertmanager \
    --cpus ".25" \
    --memory "500m" \
    --memory-swap "500m" \
    -v "$PWD"/conf/alertmanager.yml:/etc/alertmanager/alertmanager.yml \
    -p 9093:9093 \
    -d \
    prom/alertmanager:v0.20.0

# --net="host" 在容器内使用主机的网络命名空间（相比 -p 9093:9093 没有网络转发）
