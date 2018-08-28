#!/usr/bin/env bash

db_name=${1}

backup_file_name=`date '+%Y%m%d%H%M%S'`'.sql'

docker exec mariadb \
    sh -c 'exec mysqldump --databases '${db_name}' -uroot -p"$MYSQL_ROOT_PASSWORD"' > backup/${backup_file_name}
