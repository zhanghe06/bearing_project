#!/usr/bin/env bash

docker run \
    -h nginx_vue \
    --name nginx_vue \
    -v ${PWD}/conf/nginx_vue.conf:/etc/nginx/nginx.conf:ro \
    -v ${PWD}/conf/conf_vue.d:/etc/nginx/conf.d:ro \
    -v ${PWD}/logs:/var/log/nginx \
    -v ${PWD}/dist_vue:/usr/share/nginx/dist \
    -p 8600:8600 \
    -d \
    nginx:logrotate

# 注意这里挂载设置了:ro只读，宿主机更新文件之后，不会更新到docker内，需要删除容器，重开容器
