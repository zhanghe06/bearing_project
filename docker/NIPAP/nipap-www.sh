#!/usr/bin/env bash

NET_NAME="nipap"

# docker pull nipap/nipap-www:v0.29.6

docker run \
    -h nipap-www \
    --name nipap-www \
    --net "${NET_NAME}" \
    -e NIPAPD_USERNAME='admin' \
    -e NIPAPD_PASSWORD='123456' \
    -e NIPAPD_HOST='nipapd' \
    -e NIPAPD_PORT='1337' \
    -e WWW_USERNAME='guest' \
    -e WWW_PASSWORD='guest' \
    -p 80:80 \
    -d nipap/nipap-www:v0.29.6


#   NIPAPD_USERNAME     username to authenticate to nipapd
#   NIPAPD_PASSWORD     password to authenticate to nipapd
#   NIPAPD_HOST         host where nipapd is running [nipapd]
#   NIPAPD_PORT         port of nipapd [1337]
#   WWW_USERNAME        web UI username [guest]
#   WWW_PASSWORD        web UI password [guest]
