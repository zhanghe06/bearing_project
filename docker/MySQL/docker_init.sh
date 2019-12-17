#!/usr/bin/env bash

# CREATE DATABASE /*!32312 IF NOT EXISTS*/ `icall_project` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;

docker exec -i mysql sh -c 'exec mysql -uroot -p"$MYSQL_ROOT_PASSWORD" icall_project' < schema/schema.sql
