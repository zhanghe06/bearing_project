#!/usr/bin/env bash

docker run \
    -h nginx_react \
    --name nginx_react \
    -v ${PWD}/conf/nginx_react.conf:/etc/nginx/nginx.conf:ro \
    -v ${PWD}/conf/conf_react.d:/etc/nginx/conf.d:ro \
    -v ${PWD}/logs:/var/log/nginx \
    -v ${PWD}/dist:/usr/share/nginx/dist \
    -p 8500:8500 \
    -d \
    nginx:1.13.0
