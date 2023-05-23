#!/usr/bin/env bash

# https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html

# Create Docker Network
NET_NAME="efk_net"

docker network ls | grep -wq "${NET_NAME}" && echo "The network: ${NET_NAME} already exists" ||
  docker network create "${NET_NAME}" && echo "The network: ${NET_NAME} has been created"

mkdir -p data logs
chmod g+rwx data logs
chgrp 0 data logs

# Development mode
docker run \
  -h elasticsearch \
  --name elasticsearch \
  --net "${NET_NAME}" \
  --cpus ".25" \
  --memory "2g" \
  --memory-swap "2g" \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  --ulimit nofile=65536:65536 \
  --ulimit memlock=-1:-1 \
  -e "bootstrap.memory_lock=true" \
  -e ES_JAVA_OPTS="-Xms1g -Xmx1g" \
  -e ELASTIC_PASSWORD='changeme' \
  -e "discovery.type=single-node" \
  -v "${PWD}"/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml \
  -v "${PWD}"/data:/usr/share/elasticsearch/data \
  -v "${PWD}"/logs:/usr/share/elasticsearch/logs \
  -p 9200:9200 \
  -p 9300:9300 \
  -d \
  elasticsearch:7.6.0

# 服务器先优化: sysctl -w vm.max_map_count=262144
# 最小分配内存: 2G, 否则无法启动
# 堆内存默认1G，不要超过物理内存的一半和超过32G
# -e ES_JAVA_OPTS="-Xms32g -Xmx32g" 堆内存大小设置一样，防止运行时改变堆内存大小
