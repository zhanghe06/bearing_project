#!/usr/bin/env bash

# Create Docker Network
NET_NAME="efk_net"

docker network ls | grep -wq "${NET_NAME}" && echo "The network: ${NET_NAME} already exists" ||
  docker network create "${NET_NAME}" && echo "The network: ${NET_NAME} has been created"

#mkdir -p etc log plugins
#
#docker run \
#  -h fluentd_tail \
#  --name fluentd_tail \
#  --net "$NET_NAME" \
#  -u fluent \
#  --cpus ".25" \
#  --memory "500m" \
#  --memory-swap "500m" \
#  --log-opt max-size=10m \
#  --log-opt max-file=3 \
#  -v "$PWD"/etc:/fluentd/etc \
#  -v "$PWD"/log:/fluentd/log \
#  -p 24224:24224 \
#  -p 24224:24224/udp \
#  -d \
#  fluentd:plugin_es
#


#!/usr/bin/env bash

HOST_NAME="${1-localhost}"
#ES_HOST="${2-172.31.46.52}"
#LOG_PATH="${3-/Users/zhanghe/code/bearing_project/docker/Fluentd/log}"
TAG="tail"
SUFFIX="_${TAG}"
CONTAINER_NAME=fluentd"${SUFFIX}"

mkdir -p log"${SUFFIX}"
chmod g+rwx log"${SUFFIX}"
chgrp 0 log"${SUFFIX}"

docker run \
  -h "${CONTAINER_NAME}" \
  --name "${CONTAINER_NAME}" \
  --net "$NET_NAME" \
  --restart always \
  -u fluent \
  --cpus ".25" \
  --memory "500m" \
  --memory-swap "500m" \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  --log-opt tag="${TAG}.${HOST_NAME}.${CONTAINER_NAME}" \
  -v "${PWD}"/etc"${SUFFIX}":/fluentd/etc \
  -v "${PWD}"/log"${SUFFIX}":/fluentd/log \
  -v "${PWD}"/log"${SUFFIX}":/log"${SUFFIX}" \
  -d \
  fluentd:plugin_es

# sh docker_goodsrobot.sh lb0
# sh docker_goodsrobot.sh lb0 172.31.46.52 /mnt/data/deploy/goodsrobot/ssd/log
