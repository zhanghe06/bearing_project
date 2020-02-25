#!/usr/bin/env bash

docker run \
  --name blackbox_exporter \
  --rm \
  -d \
  -p 9115:9115 \
  -v "$PWD"/config:/config \
  prom/blackbox-exporter:master --config.file=/config/blackbox.yml

curl "http://localhost:9115/probe?target=google.com&module=http_2xx"
