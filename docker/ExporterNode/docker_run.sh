#!/usr/bin/env bash

docker run \
    -h node-exporter \
    --name node-exporter \
    --pid "host" \
    --cpus ".25" \
    --memory "500m" \
    --memory-swap "500m" \
    -v "/:/host:ro" \
    -p 9100:9100 \
    -d \
    prom/node-exporter:v0.18.1 \
    --path.rootfs /host

# --net="host" 在容器内使用主机的网络命名空间（相比-p 9100:9100没有网络转发）
# --pid="host" 在容器内使用主机的进程进程空间

#docker run \
#    -d --name node-exporter \
#    -v "/proc:/host/proc" \
#    -v "/sys:/host/sys" \
#    -v "/:/rootfs" \
#    --net="host" \
#    prom/node-exporter:v0.18.1 \
#    --path.procfs=/host/proc \
#    --path.sysfs=/host/proc \
#    --collector.filesystem.ignored-mount-points "^/(sys|proc|dev|host|etc)($|/)"
