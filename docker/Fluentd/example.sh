#!/usr/bin/env bash

# Post a record with the tag "api.log"
curl -X POST -d 'json={"foo": "bar", "abc": "abc"}' http://192.168.4.1:9880/api.log
