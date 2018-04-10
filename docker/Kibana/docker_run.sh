#!/usr/bin/env bash

docker run \
    -h kibana \
    --name kibana \
    --add-host elasticsearch:192.168.4.1 \
    -d \
    -p 5601:5601 \
    -v "${PWD}/kibana.yml":/usr/share/kibana/config/kibana.yml \
    docker.elastic.co/kibana/kibana:6.2.3
