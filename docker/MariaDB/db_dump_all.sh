#!/usr/bin/env bash

# sh docker/MariaDB/db_dump_all.sh

BACKUP_DIR=${PROJECT_PATH}'/db/backup/'

[ -d ${BACKUP_DIR} ] || mkdir -p ${BACKUP_DIR}

BACKUP_SQL=${BACKUP_DIR}'databases_'`date '+%Y%m%d%H%M%S'`'.sql'
BACKUP_SQL_LATEST=${BACKUP_DIR}'databases_latest.sql'

docker exec mariadb \
    sh -c 'exec mysqldump --all-databases -uroot -p"$MYSQL_ROOT_PASSWORD" --default-character-set=utf8mb4' > ${BACKUP_SQL}

\cp ${BACKUP_SQL} ${BACKUP_SQL_LATEST}

echo ${BACKUP_SQL}

ls -alh ${BACKUP_DIR}
