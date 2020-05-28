#!/usr/bin/env bash

docker run \
    -h cadvisor \
    --name cadvisor \
    --cpus ".25" \
    --memory "500m" \
    --memory-swap "500m" \
    --log-opt max-size=10m \
    --log-opt max-file=3 \
    -v /:/rootfs:ro \
    -v /var/run:/var/run:rw \
    -v /sys:/sys:ro \
    -v /var/lib/docker/:/var/lib/docker:ro \
    -v /dev/disk/:/dev/disk:ro \
    -p "${1-8080}":8080 \
    -d \
    google/cadvisor:v0.32.0

# sh docker_run.sh
# sh docker_run.sh 8090
