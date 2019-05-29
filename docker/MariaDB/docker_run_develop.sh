#!/usr/bin/env bash

DB_DIR=${PROJECT_PATH}'/docker/MariaDB/'

[ -d ${DB_DIR}data ] || mkdir -p ${DB_DIR}data
[ -d ${DB_DIR}log ] || mkdir -p ${DB_DIR}log

docker run \
    -h mariadb \
    --name mariadb \
    -v ${DB_DIR}data:/var/lib/mysql \
    -v ${DB_DIR}log:/var/log/mysql \
    -e MYSQL_ROOT_PASSWORD='123456' \
    -e MYSQL_DATABASE='bearing_project' \
    -e MYSQL_USER='www' \
    -e MYSQL_PASSWORD='123456' \
    -p 3306:3306 \
    -d \
    mariadb:10.1.23
