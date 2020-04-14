#!/usr/bin/env bash

# 后台运行
docker run \
    --name flask_file_system \
    -h flask_file_system \
    --restart=always \
    -e TZ=Asia/Shanghai \
    -e PYTHONIOENCODING=utf-8 \
    -e PYTHONPATH=/project \
    -v "${PWD}/uploads":/project/uploads \
    -p 5000:5000 \
    -d \
    flask_file_system \
    supervisord -c etc/supervisord.conf
