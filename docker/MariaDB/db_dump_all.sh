#!/usr/bin/env bash

# sh docker/MariaDB/db_dump_all.sh

BACKUP_SQL='db/backup/'`date '+%Y%m%d%H%M%S'`'.sql'

docker exec mariadb \
    sh -c 'exec mysqldump --all-databases -uroot -p"$MYSQL_ROOT_PASSWORD" --default-character-set=utf8mb4' > ${BACKUP_SQL}

echo ${BACKUP_SQL}
