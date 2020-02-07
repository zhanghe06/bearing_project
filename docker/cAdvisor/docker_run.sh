#!/usr/bin/env bash

docker run \
    -h cadvisor \
    --name cadvisor \
    --cpus ".25" \
    --memory "500m" \
    --memory-swap "500m" \
    -v /:/rootfs:ro \
    -v /var/run:/var/run:rw \
    -v /sys:/sys:ro \
    -v /var/lib/docker/:/var/lib/docker:ro \
    -v /dev/disk/:/dev/disk:ro \
    -p 8080:8080 \
    -d \
    google/cadvisor:v0.32.0
