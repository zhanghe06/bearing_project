#!/usr/bin/env bash

# Create Docker Network
NET_NAME="efk_net"

docker network ls | grep -wq "$NET_NAME" && echo "The network: $NET_NAME already exists" || (docker network create "$NET_NAME" && echo "The network: $NET_NAME has been created")

mkdir -p etc log plugins

docker run \
  -h fluentd_forward \
  --name fluentd_forward \
  --net "$NET_NAME" \
  -u fluent \
  --cpus ".25" \
  --memory "500m" \
  --memory-swap "500m" \
  -v "$PWD"/etc:/fluentd/etc \
  -p 24224:24224 \
  -p 24224:24224/udp \
  -d \
  fluentd:plugin_es
