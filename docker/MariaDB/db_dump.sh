#!/usr/bin/env bash

# sh docker/MariaDB/db_dump.sh bearing_project

[ -d ${PWD}/db/backup ] || mkdir -p ${PWD}/db/backup

DB_NAME=${1:-bearing_project}

BACKUP_SQL='db/backup/'${DB_NAME}'_'`date '+%Y%m%d%H%M%S'`'.sql'

docker exec mariadb \
    sh -c 'exec mysqldump --databases '${DB_NAME}' -uroot -p"$MYSQL_ROOT_PASSWORD" --default-character-set=utf8mb4' > ${BACKUP_SQL}

echo ${BACKUP_SQL}
