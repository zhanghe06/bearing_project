#!/usr/bin/env bash

docker run \
    -d \
    --name=consul \
    -e CONSUL_BIND_INTERFACE=eth0 \
    -p 8300-8302:8300-8302 \
    -p 8500:8500 \
    -p 8301-8302:8301-8302/udp \
    -p 8600:8600 \
    -p 8600:8600/udp \
    consul
