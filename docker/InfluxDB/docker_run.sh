#!/usr/bin/env bash

docker run \
    -h=influxdb \
    --name=influxdb \
    -v $PWD/conf/influxdb.conf:/etc/influxdb/influxdb.conf:ro \
    -v $PWD/data:/var/lib/influxdb \
    -p 8086:8086 \
    -p 2003:2003 \
    -e INFLUXDB_HTTP_AUTH_ENABLED=true \
    -e INFLUXDB_ADMIN_ENABLED=true \
    -e INFLUXDB_ADMIN_USER="admin" \
    -e INFLUXDB_ADMIN_PASSWORD="123456" \
    -e INFLUXDB_GRAPHITE_ENABLED=true \
    -e INFLUXDB_DB="example" \
    -e INFLUXDB_READ_USER="r_user" \
    -e INFLUXDB_READ_USER_PASSWORD="123456" \
    -e INFLUXDB_WRITE_USER="w_user" \
    -e INFLUXDB_WRITE_USER_PASSWORD="123456" \
    -d \
    influxdb:1.4.2
