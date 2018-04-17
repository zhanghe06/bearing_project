#!/usr/bin/env bash

docker run --rm \
    influxdb:1.4.2 influxd config > conf/influxdb.conf
