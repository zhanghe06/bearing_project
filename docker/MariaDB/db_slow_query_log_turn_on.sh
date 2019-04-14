#!/usr/bin/env bash

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
    --default-character-set=utf8mb4 \
    "$MYSQL_ENV_MYSQL_DATABASE" \
    -e "set global slow_query_log=1;
    show variables like '\'%low_query_log%\'';
    show variables like '\'%long_query_time%\'';
    show variables like '\'%log_output%\'';
    "'

# 测试
# MariaDB [flask_project]> select sleep(12);
# less log/mariadb-slow.log
