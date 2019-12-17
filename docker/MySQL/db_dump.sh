#!/usr/bin/env bash

# sh db_dump.sh test_project

DB_NAME=${1:-test_project}

BACKUP_SQL='backup/'"$DB_NAME"'_'$(date '+%Y%m%d%H%M%S')'.sql'

docker exec mysql \
    sh -c 'exec mysqldump --databases '"$DB_NAME"' -uroot -p"$MYSQL_ROOT_PASSWORD" --default-character-set=utf8mb4' > "$BACKUP_SQL"

echo "$BACKUP_SQL"
