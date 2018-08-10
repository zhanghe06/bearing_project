#!/usr/bin/env bash

[ -d ${PWD}/data ] || mkdir -p ${PWD}/data
[ -d ${PWD}/log ] || mkdir -p ${PWD}/log
[ -d ${PWD}/backup ] || mkdir -p ${PWD}/backup

docker run \
    -h mariadb \
    --name mariadb \
    -v ${PWD}/data:/var/lib/mysql \
    -v ${PWD}/log:/var/log/mysql \
    -v ${PWD}/backup:/backup \
    -e MYSQL_ROOT_PASSWORD='123456' \
    -e MYSQL_DATABASE='bearing_project' \
    -e MYSQL_USER='www' \
    -e MYSQL_PASSWORD='123456' \
    -p 3306:3306 \
    -d \
    mariadb:10.1.23