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

#HOST_NAME="${1}"
#ES_HOST="${2-172.31.46.52}"
FL_PORT_TCP="${1-24224}"
FL_PORT_UDP="${1-24224}"
TAG="udp"
SUFFIX="_${TAG}"

docker run \
  -h fluentd"${SUFFIX}" \
  --name fluentd"${SUFFIX}" \
  --net "$NET_NAME" \
  --restart always \
  -u fluent \
  --cpus ".25" \
  --memory "500m" \
  --memory-swap "500m" \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  -v "${PWD}"/etc"${SUFFIX}":/fluentd/etc \
  -p "${FL_PORT_TCP}":24224 \
  -p "${FL_PORT_UDP}":24224/udp \
  -d \
  fluentd:plugin_es

# sh docker_run_udp.sh
