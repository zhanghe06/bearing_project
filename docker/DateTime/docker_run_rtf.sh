#!/usr/bin/env bash

docker rm -f rtf

docker run \
    -h rtf \
    --name rtf \
    --log-driver=fluentd \
    --log-opt fluentd-address=192.168.4.1:24224 \
    --log-opt mode=non-blocking \
    --log-opt tag={{.Name}} \
    -d \
    python:2.7 sh -c "while true
do
echo 'I0304 03:19:04.014420    48 stream_decoder_manager.cc:103] RTF: e13674e5-5dc6-11ea-996f-0242ac110002  400 74 0.185'
echo 'I0304 03:19:04.014420    48 stream_decoder_manager.cc:103] RTF: e13674e5-5dc6-11ea-996f-0242ac110002  400 500 1.25'
echo 'I0304 03:19:04.014420    48 stream_decoder_manager.cc:103] RTF: e13674e5-5dc6-11ea-996f-0242ac110002  400 220 0.55'
sleep 1
done"


# i=0; while true; do echo "[$(uname -n)] $(date)"; i=$((i+1)); sleep 1; done

#     --add-host fluentd:192.168.4.1 \
