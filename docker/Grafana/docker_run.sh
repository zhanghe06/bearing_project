#!/usr/bin/env bash

# Create Docker Volume
VOLUME_NAME="grafana-vol"

# docker volume rm grafana-vol

docker volume ls | grep -wq "$VOLUME_NAME" && \
    echo "The volume: $VOLUME_NAME already exists" || (docker volume create "$VOLUME_NAME" && \
    echo "The volume: $VOLUME_NAME has been created")

docker run \
    -h grafana \
    --name grafana \
    --cpus ".25" \
    --memory "1g" \
    --memory-swap "1g" \
    -e GF_SECURITY_ADMIN_USER='admin' \
    -e GF_SECURITY_ADMIN_PASSWORD='123456' \
    -e GF_USERS_ALLOW_SIGN_UP=false \
    -v "$VOLUME_NAME":/var/lib/grafana \
    -p 3000:3000 \
    -d \
    grafana/grafana:6.6.2

# http://0.0.0.0:3000
