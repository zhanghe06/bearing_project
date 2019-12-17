#!/usr/bin/env bash

# sh db_restore.sh tagging_system

DB_NAME=${1:-test_project}

BACKUP_SQL='backup/'"$DB_NAME"'.sql'

echo "$BACKUP_SQL"

docker exec -i mysql sh -c 'exec mysql -uroot -p"$MYSQL_ROOT_PASSWORD"' < "$BACKUP_SQL"

docker run \
    -it \
    --link mysql:mysql \
    --rm \
    mysql:5.7 \
    sh -c 'exec mysql \
    -h"$MYSQL_PORT_3306_TCP_ADDR" \
    -P"$MYSQL_PORT_3306_TCP_PORT" \
    -uroot \
    -p"$MYSQL_ENV_MYSQL_ROOT_PASSWORD" \
    --default-character-set=utf8mb4 \
    "$MYSQL_ENV_MYSQL_DATABASE" \
    -e "show databases; use '"$DB_NAME"'; show tables;"'
