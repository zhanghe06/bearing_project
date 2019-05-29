#!/usr/bin/env bash

docker run \
    -it \
    --link mariadb:mysql \
    --rm \
    -v ${PROJECT_PATH}/db/data/:/db/data/ \
    -v ${PROJECT_PATH}/db/schema/:/db/schema/ \
    mariadb:10.1.23 \
    sh -c 'exec mysql \
    -h"$MYSQL_PORT_3306_TCP_ADDR" \
    -P"$MYSQL_PORT_3306_TCP_PORT" \
    -uroot \
    -p"$MYSQL_ENV_MYSQL_ROOT_PASSWORD" \
    --default-character-set=utf8mb4 \
    "$MYSQL_ENV_MYSQL_DATABASE" \
    -e "source db/schema/mysql.sql; source db/data/mysql.sql; show databases; show tables;"'

# 挂载数据目录，是因为可以使用统一的sql脚本路径
