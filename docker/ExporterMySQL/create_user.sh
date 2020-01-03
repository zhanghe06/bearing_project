#!/usr/bin/env bash

docker run \
    -it \
    --link mysql:mysql \
    --rm \
    mysql:5.7 \
    sh -c 'exec mysql \
    -h"$MYSQL_PORT_3306_TCP_ADDR" \
    -P"$MYSQL_PORT_3306_TCP_PORT" \
    -uroot \
    -p"$MYSQL_ENV_MYSQL_ROOT_PASSWORD" \
    --default-character-set=utf8 \
    "$MYSQL_ENV_MYSQL_DATABASE" \
    -e "CREATE USER 'exporter'@'localhost' IDENTIFIED BY '\'123456\'';GRANT PROCESS, REPLICATION CLIENT ON *.* TO 'exporter'@'localhost';GRANT SELECT ON performance_schema.* TO 'exporter'@'localhost';FLUSH PRIVILEGES;select host,user from mysql.user;"'
