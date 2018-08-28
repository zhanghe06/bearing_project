#!/usr/bin/env bash

docker run \
    -it \
    --link redis:redis \
    --rm \
    redis:3.2.8 \
    sh -c 'exec redis-cli -h redis -p "$REDIS_ENV_REDIS_PORT" -a "$REDIS_ENV_REDIS_PASSWORD"'
