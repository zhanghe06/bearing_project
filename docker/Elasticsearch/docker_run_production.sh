#!/usr/bin/env bash

# Create Docker Network
NET_NAME="efk_net"

docker network ls | grep -wq "$NET_NAME" && echo "The network: $NET_NAME already exists" || (docker network create "$NET_NAME" && echo "The network: $NET_NAME has been created")

mkdir -p data logs

# Production mode
docker run \
    -h elasticsearch \
    --name elasticsearch \
    --net "$NET_NAME" \
    --cpus ".25" \
    --memory "2g" \
    --memory-swap "2g" \
    --ulimit nofile=65536:65536 \
    -e ELASTIC_PASSWORD='changeme' \
    -v "${PWD}/elasticsearch.yml":/usr/share/elasticsearch/config/elasticsearch.yml \
    -v "${PWD}/data":/usr/share/elasticsearch/data \
    -v "${PWD}/logs":/usr/share/elasticsearch/logs \
    -p 9200:9200 \
    -p 9300:9300 \
    -d \
    elasticsearch:7.6.0

# 最小分配内存: 2G, 否则无法启动
