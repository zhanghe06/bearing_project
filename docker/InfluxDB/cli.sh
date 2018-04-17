#!/usr/bin/env bash

docker run \
    --rm \
    --link=influxdb \
    -it \
    influxdb:1.4.2 \
    sh -c 'influx -host influxdb -username "$INFLUXDB_ENV_INFLUXDB_ADMIN_USER" -password "$INFLUXDB_ENV_INFLUXDB_ADMIN_PASSWORD"'
