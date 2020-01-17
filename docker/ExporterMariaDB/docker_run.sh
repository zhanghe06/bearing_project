#!/usr/bin/env bash

docker run \
    --name mysqld-exporter \
    -d \
    -p 9104:9104 \
    --link=mariadb:bdd \
    -e DATA_SOURCE_NAME="exporter:123456@(bdd:3306)/" \
    prom/mysqld-exporter
