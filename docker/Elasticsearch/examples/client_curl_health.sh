#!/usr/bin/env bash

#ES_HOSTNAME="elasticsearch"
ES_HOSTNAME='127.0.0.1'
ES_PORT=9200
ES_USERNAME='elastic'
ES_PASSWORD='changeme'

# curl --basic -u "elastic:changeme" http://127.0.0.1:9200/_cat/health
CMD="curl -u '${ES_USERNAME}:${ES_PASSWORD}' ${ES_HOSTNAME}:${ES_PORT}/_cat/health"
echo "${CMD}"
sh -c "${CMD}"
