#!/usr/bin/env bash

# Create Docker Volume
VOLUME_NAME="prometheus-vol"

# docker volume rm prometheus-vol

docker volume ls | grep -wq "$VOLUME_NAME" && \
    echo "The volume: $VOLUME_NAME already exists" || (docker volume create "$VOLUME_NAME" && \
    echo "The volume: $VOLUME_NAME has been created")

docker run \
    -h prometheus \
    --name prometheus \
    --cpus ".25" \
    --memory "1g" \
    --memory-swap "1g" \
    -v ${PWD}/conf/prometheus.yml:/etc/prometheus/prometheus.yml \
    -v "$VOLUME_NAME":/prometheus \
    -p 9090:9090 \
    -d \
    prom/prometheus:v2.16.0

# --net="host" 在容器内使用主机的网络命名空间（相比 -p 9090:9090 没有网络转发）
