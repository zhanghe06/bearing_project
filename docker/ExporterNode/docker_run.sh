#!/usr/bin/env bash

docker run \
    --name node-exporter \
    -d \
    --net="host" \
    --pid="host" \
    -v "/:/host:ro,rslave" \
    prom/node-exporter \
    --path.rootfs /host
