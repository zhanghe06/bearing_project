#!/usr/bin/env bash

mkdir -p data
docker run -h zookeeper --name zookeeper -v ${PWD}/data:/data -d -p 2181:2181 zookeeper:3.4.14
