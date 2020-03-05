#!/usr/bin/env bash

# https://docs.docker.com/config/containers/logging/syslog/
# udp 模式的好处: Fluentd重启不影响之后的日志收集

docker rm -f udp

docker run \
    -h udp \
    --name udp \
    --log-driver syslog \
    --log-opt syslog-address=udp://192.168.4.1:24224 \
    --log-opt tag={{.Name}} \
    -d \
    python:2.7 sh -c "while true
do
echo 'I0304 03:19:04.014420    48 stream_decoder_manager.cc:103] RID: e13674e5-5dc6-11ea-996f-0242ac110002  400 74 0.185'
echo 'xxxxxx xxxxxx'
echo 'I0304 03:19:04.014420    48 stream_decoder_manager.cc:103] RID: e13674e5-5dc6-11ea-996f-0242ac110002  400 500 1.25'
echo 'I0304 03:19:04.014420    48 stream_decoder_manager.cc:103] RID: e13674e5-5dc6-11ea-996f-0242ac110002  400 220 0.55'
sleep 1
done"


# i=0; while true; do echo "[$(uname -n)] $(date)"; i=$((i+1)); sleep 1; done

#     --add-host fluentd:192.168.4.1 \
