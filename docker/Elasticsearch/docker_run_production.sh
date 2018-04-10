#!/usr/bin/env bash

# Production mode
docker run \
    -h elasticsearch \
    --name elasticsearch \
    -d \
    --ulimit nofile=65536:65536 \
    -p 9200:9200 \
    -p 9300:9300 \
    -e ELASTIC_PASSWORD='changeme' \
    -v "${PWD}/elasticsearch.yml":/usr/share/elasticsearch/config/elasticsearch.yml \
    -v "${PWD}/data":/usr/share/elasticsearch/data \
    -v "${PWD}/logs":/usr/share/elasticsearch/logs \
    docker.elastic.co/elasticsearch/elasticsearch:6.2.3
