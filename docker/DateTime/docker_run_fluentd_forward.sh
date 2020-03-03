#!/usr/bin/env bash

docker rm -f datetime

docker run \
    -h datetime \
    --name datetime \
    --log-driver=fluentd \
    --log-opt fluentd-address=192.168.4.1:24224 \
    --log-opt mode=non-blocking \
    --log-opt tag={{.Name}} \
    -d \
    python:2.7 sh -c "while true
do
date +'%Y-%m-%d %H:%M:%S'
sleep 1
done"


# i=0; while true; do echo "[$(uname -n)] $(date)"; i=$((i+1)); sleep 1; done

#     --add-host fluentd:192.168.4.1 \
