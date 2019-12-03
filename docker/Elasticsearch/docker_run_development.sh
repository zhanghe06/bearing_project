#!/usr/bin/env bash

# Create Docker Network
NET_NAME="efk_net"

docker network ls | grep -wq "$NET_NAME" && echo "The network: $NET_NAME already exists" || (docker network create "$NET_NAME" && echo "The network: $NET_NAME has been created")

mkdir -p data logs

# Development mode
docker run \
    -h elasticsearch \
    --name elasticsearch \
    --net "$NET_NAME" \
    -d \
    --ulimit nofile=65536:65536 \
    -p 9200:9200 \
    -p 9300:9300 \
    -e "discovery.type=single-node" \
    -e ELASTIC_PASSWORD='changeme' \
    -v "${PWD}/elasticsearch.yml":/usr/share/elasticsearch/config/elasticsearch.yml \
    -v "${PWD}/data":/usr/share/elasticsearch/data \
    -v "${PWD}/logs":/usr/share/elasticsearch/logs \
    elasticsearch:7.6.0
