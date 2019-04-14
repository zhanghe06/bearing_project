#!/usr/bin/env bash

# 方式一
docker exec mariadb \
    sh -c 'exec mysql \
    -uroot \
    -p"$MYSQL_ROOT_PASSWORD" \
    -e "SELECT user, host, password FROM mysql.user\G"'

# 方式二
# 推荐，原版显示格式
docker run \
    -it \
    --link mariadb:mysql \
    --rm \
    mariadb:10.1.23 \
    sh -c 'exec mysql \
    -h"$MYSQL_PORT_3306_TCP_ADDR" \
    -P"$MYSQL_PORT_3306_TCP_PORT" \
    -uroot \
    -p"$MYSQL_ENV_MYSQL_ROOT_PASSWORD" \
    -e "SELECT user, host, password FROM mysql.user;"'
