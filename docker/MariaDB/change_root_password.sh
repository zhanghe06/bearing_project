#!/usr/bin/env bash

[ -d ${PWD}/data ] || mkdir -p ${PWD}/data
[ -d ${PWD}/backup ] || mkdir -p ${PWD}/backup


docker rm -f mariadb

ROOT_USER_NAME='root'
ROOT_PASS_WORD='123456'

#MYSQL_CMD='exec mysql -e "use mysql; show tables;"'
MYSQL_CMD='exec mysql -e "use mysql; update user set password=PASSWORD('\'${ROOT_PASS_WORD}\'') where User='\'${ROOT_USER_NAME}\''; flush privileges;"'

echo "${MYSQL_CMD}"

docker run \
    -h mariadb \
    --name mariadb \
    -v ${PWD}/data:/var/lib/mysql \
    -d \
    mariadb:10.1.23 --skip-grant-tables

# 等待时间必须设置（等待容器数据库完全创建成功后执行下一步）
sleep 3

docker exec -it mariadb sh -c "${MYSQL_CMD}"

docker rm -f mariadb


# 作用:
# 1. 修改密码(注意: 真实密码与容器启动时设置的环境变量 MYSQL_ROOT_PASSWORD 不是一回事)
# 2. 真实密码与容器内环境变量 MYSQL_ENV_MYSQL_ROOT_PASSWORD 不一致, 如果服务器被攻击, 拿到环境变量的密码也没有用
