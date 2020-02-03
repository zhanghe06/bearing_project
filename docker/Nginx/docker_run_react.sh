#!/usr/bin/env bash

docker run \
    -h nginx_react \
    --name nginx_react \
    -v ${PWD}/conf/nginx_react.conf:/etc/nginx/nginx.conf:ro \
    -v ${PWD}/conf/conf_react.d:/etc/nginx/conf.d:ro \
    -v ${PWD}/logs:/var/log/nginx \
    -v ${PWD}/dist_react:/usr/share/nginx/dist \
    -p 8500:8500 \
    -d \
    nginx:logrotate

# 注意这里挂载设置了:ro只读，宿主机更新文件之后，不会更新到docker内，需要删除容器，重开容器
