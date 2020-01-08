#!/usr/bin/env bash

# Create Docker Network
NET_NAME="efk_net"

docker network ls | grep -wq "$NET_NAME" && echo "The network: $NET_NAME already exists" || (docker network create "$NET_NAME" && echo "The network: $NET_NAME has been created")

# 对接其他平台ES
#docker run \
#    -h kibana \
#    --name kibana \
#    --add-host elasticsearch:192.168.4.1 \
#    -d \
#    -p 5601:5601 \
#    -v "${PWD}/kibana.yml":/usr/share/kibana/config/kibana.yml \
#    kibana:7.6.0

# 对接同网环境ES
docker run \
    -h kibana \
    --name kibana \
    --net "$NET_NAME" \
    -d \
    -p 5601:5601 \
    -v "${PWD}/kibana.yml":/usr/share/kibana/config/kibana.yml \
    kibana:7.6.0
