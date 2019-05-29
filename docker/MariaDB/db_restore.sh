#!/usr/bin/env bash

# sh docker/MariaDB/db_restore.sh bearing_project

BACKUP_DIR=${PROJECT_PATH}'/db/backup/'

DB_NAME=${1:-bearing_project}

# 获取最新的备份文件
#BACKUP_SQL='db/backup/'`ls -lt db/backup/ | grep ${DB_NAME} | head -n 1 | awk '{print $9}'`

BACKUP_SQL='db/backup/'${DB_NAME}'_latest.sql'

echo ${BACKUP_SQL}

docker run \
    -it \
    --link mariadb:mysql \
    --rm \
    -v ${BACKUP_DIR}:/db/backup/ \
    mariadb:10.1.23 \
    sh -c 'exec mysql \
    -h"$MYSQL_PORT_3306_TCP_ADDR" \
    -P"$MYSQL_PORT_3306_TCP_PORT" \
    -uroot \
    -p"$MYSQL_ENV_MYSQL_ROOT_PASSWORD" \
    --default-character-set=utf8mb4 \
    "$MYSQL_ENV_MYSQL_DATABASE" \
    -e "source '${BACKUP_SQL}'; show databases; show tables;"'

# 挂载数据目录，是因为可以使用统一的sql脚本路径
