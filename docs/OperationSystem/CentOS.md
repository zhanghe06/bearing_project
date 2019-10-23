# CentOS

## 下载（指定版本 7.6 最小化安装 即server版）
[https://www.centos.org](https://www.centos.org) -> 
[Get CentOS Now](https://www.centos.org/download/) -> 
[list of current mirrors](https://www.centos.org/download/mirrors/) -> 
[aliyun mirrors](http://mirrors.aliyun.com/centos/) -> 
[7.6.1810/](http://mirrors.aliyun.com/centos/7.6.1810/)

提示版本停止更新，需要跳转到[http://vault.centos.org/](http://vault.centos.org/)

[7.6.1810/](http://vault.centos.org/7.6.1810/) -> 
[isos](http://vault.centos.org/7.6.1810/isos/) -> 
[x86_64/](http://vault.centos.org/7.6.1810/isos/x86_64/) -> 
[CentOS-7-x86_64-Minimal-1810.iso](http://vault.centos.org/7.6.1810/isos/x86_64/CentOS-7-x86_64-Minimal-1810.iso)

## 初始配置

默认网络没有开启，需要手动开启
```
# nmcli connection show                                 # 连接情况
# nmcli device status                                   # 设备状态
# nmcli connection up ens33                             # 开启网卡
# nmcli conn mod ens33 connection.autoconnect yes       # 开机启动
# curl https://ip.cn                                    # 测试网络
```

查看监听端口
```
ss -lnt
```

设置hostname
```
[root@node2 ~]# hostnamectl
hostname: localhost.localdomain
Transient hostname: node2
         Icon name: computer-vm
           Chassis: vm
        Machine ID: c1d9b60b1

# hostnamectl set-hostname node2 --static
```

## 集群搭建

```
node1   192.168.64.133       # master
node2   192.168.64.134       # backup
vip     192.168.64.130
```

```
# vim /etc/hosts
192.168.64.133 node1
192.168.64.134 node2
# ping -c 4 node1
# ping -c 4 node2
```

关闭selinux
```
# setenforce 0
# sed -i.bak "s/SELINUX=enforcing/SELINUX=disabled/g" /etc/selinux/config
```

免密登录(非root用户)

node1、node2设置普通用户密码
```
# passwd postgres
更改用户 postgres 的密码 。
新的 密码：123456
无效的密码： 密码少于 8 个字符
重新输入新的 密码：123456
passwd：所有的身份验证令牌已经成功更新。
```

node1
```
# su - postgres
$ ssh-keygen
```

node2
```
# su - postgres
$ ssh-keygen
```

node1
```
# su - postgres
$ ssh-copy-id node2
# reboot
```

node2
```
# su - postgres
$ ssh-copy-id node1
# reboot
```


参考: [docs/Components/Keepalived.md](../Components/Keepalived.md)

## Docker

[https://docs.docker.com/install/linux/docker-ce/centos](https://docs.docker.com/install/linux/docker-ce/centos)

参考: [docs/Deployment/Docker.md](../Deployment/Docker.md#Docker)

## PostgresQL

### 单节点(docker)
安装 PostgresQL-10
```
# docker pull postgres:10
```

docker_run.sh
```
#!/usr/bin/env bash

docker run \
    -h postgres \
    --name postgres \
    -v ${PWD}/data:/var/lib/postgresql/data \
    -v ${PWD}/archive:/var/lib/postgresql/archive \
    -e POSTGRES_USER='www' \
    -e POSTGRES_PASSWORD='123456' \
    -e POSTGRES_DB='project' \
    -p 5432:5432 \
    -d postgres:10
```

docker容器内部安装网络工具
```
apt-get update
apt install -y net-tools           # ifconfig
apt install -y iputils-ping        # ping
apt install -y vim
```

创建用户
```
[root@node1 postgresql]# docker exec -it postgres bash
root@postgres:/# psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}
psql (10.10 (Debian 10.10-1.pgdg90+1))
Type "help" for help.

project=# create user repl replication password '123456';
CREATE ROLE
project=# \du
                                   List of roles
 Role name |                         Attributes                         | Member of
-----------+------------------------------------------------------------+-----------
 repl      | Replication                                                | {}
 www       | Superuser, Create role, Create DB, Replication, Bypass RLS | {}
```

### 配置主备

[https://www.pgpool.net/docs/pgpool-II-3.7.2/en/html/example-cluster.html](https://www.pgpool.net/docs/pgpool-II-3.7.2/en/html/example-cluster.html)

[https://www.xiaomastack.com/2019/08/16/postgresql%E4%B8%BB%E5%A4%87%E5%88%87%E6%8D%A2/](https://www.xiaomastack.com/2019/08/16/postgresql%E4%B8%BB%E5%A4%87%E5%88%87%E6%8D%A2/)

[https://www.postgresql.org/download/linux/redhat](https://www.postgresql.org/download/linux/redhat)

安装服务
```
yum install https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm
yum install postgresql10 postgresql10-server postgresql10-contrib postgresql10-devel
/usr/pgsql-10/bin/postgresql-10-setup initdb
systemctl status postgresql-10
systemctl enable postgresql-10
systemctl start postgresql-10
```

修改密码
```
[root@node1 postgresql]# su - postgres
-bash-4.2$ psql -c "alter user postgres with password '123456'"
ALTER ROLE
```

测试
```
[root@node1 postgresql]# su - postgres
上一次登录：三 11月 13 04:22:52 CST 2019pts/0 上
-bash-4.2$ psql
psql (10.10)
输入 "help" 来获取帮助信息.

postgres=# \du
                             角色列表
 角色名称 |                    属性                    | 成员属于
----------+--------------------------------------------+----------
 postgres | 超级用户, 建立角色, 建立 DB, 复制, 绕过RLS | {}

postgres=# show data_directory;
     data_directory
------------------------
 /var/lib/pgsql/10/data
(1 行记录)
```

更新配置

更新之前
```
[root@node1 postgresql]# ss -lnt | grep 5432
LISTEN     0      128    127.0.0.1:5432                     *:*
LISTEN     0      128        ::1:5432                    :::*
```

更新
```
echo "host    all             all             0.0.0.0/0               md5" >> /var/lib/pgsql/10/data/pg_hba.conf
echo "listen_addresses = '*'" >> /var/lib/pgsql/10/data/postgresql.conf
mkdir /var/lib/pgsql/archivedir
chown postgres:postgres -R /var/lib/pgsql/archivedir
systemctl restart postgresql-10
```

验证
```
[root@node1 postgresql]# systemctl restart postgresql-10
[root@node1 postgresql]# ss -lnt | grep 5432
LISTEN     0      128          *:5432                     *:*
LISTEN     0      128         :::5432                    :::*
```


#### 配置主库

创建用户
```
[root@node1 postgresql]# su - postgres
上一次登录：三 11月 13 03:33:11 CST 2019pts/0 上
-bash-4.2$ createuser --replication -P replica
为新角色输入的口令: 123456
再输入一遍: 123456
-bash-4.2$ psql
psql (10.10)
输入 "help" 来获取帮助信息.

postgres=# \du
                             角色列表
 角色名称 |                    属性                    | 成员属于
----------+--------------------------------------------+----------
 postgres | 超级用户, 建立角色, 建立 DB, 复制, 绕过RLS | {}
 replica  | 复制                                       | {}
```

修改配置 pg_hba.conf
```
host    replication     replica         0.0.0.0/0               md5
```

修改配置 postgresql.conf
```
#------------------------------------------------------------------------------
# CONNECTIONS AND AUTHENTICATION
#------------------------------------------------------------------------------
listen_addresses = '*'

#------------------------------------------------------------------------------
# WRITE AHEAD LOG
#------------------------------------------------------------------------------
wal_level = replica
archive_mode = on
archive_command = 'cp %p /var/lib/pgsql/archivedir/%f'

#------------------------------------------------------------------------------
# REPLICATION
#------------------------------------------------------------------------------
max_wal_senders = 10    # 并发的从库数量
wal_keep_segments = 64  # 默认是0,代表主库wal日志文件保存的个数,设置数量多一点可以防止主库生成日志太快而被覆盖的情况发生
```

重启服务
```
systemctl restart postgresql-10
```

#### 配置备库

```
PGDATA=/var/lib/pgsql/10/data
systemctl stop postgresql-10
rm -rf ${PGDATA}
pg_basebackup -h node1 -U replica -Fp -Xs -v -P -R -D ${PGDATA}
chown postgres:postgres -R ${PGDATA}
```

```
#-h指定连接的数据库的主机名或IP地址
#-U指定连接的用户名
#-F指定了输出的格式，支持p（原样输出）或者t（tar格式输出）
#-X表示备份开始后，启动另一个流复制连接从主库接收WAL日志
#-P表示允许在备份过程中实时的打印备份的进度
#-R表示会在备份结束后自动生成recovery.conf文件
#-D指定备份写入的数据目录,需要与数据库配置的数据库目录一致,初次备份之前从库的数据目录需要手动清空
#-l表示指定一个备份的标识
```

修改配置文件 /var/lib/pgsql/10/data/postgresql.conf
```
hot_standby = on
sed -i.bak "s/#hot_standby = off/hot_standby = on/g" /var/lib/pgsql/10/data/postgresql.conf
```

重启
```
systemctl restart postgresql-10
```

#### 验证主备

验证主
```
[root@node1 postgresql]# ps -ef | grep wal
postgres  15327  15321  0 04:36 ?        00:00:00 postgres: wal writer process
postgres  15710  15321  0 05:27 ?        00:00:00 postgres: wal sender process replica 192.168.64.150(58960) streaming 0/60179F8

[root@node1 postgresql]# su - postgres
上一次登录：三 11月 13 04:23:51 CST 2019pts/0 上

-bash-4.2$ /usr/pgsql-10/bin/pg_controldata | grep 数据库簇状态
数据库簇状态:                         在运行中

-bash-4.2$ psql
psql (10.10)
输入 "help" 来获取帮助信息.

postgres=# select pg_is_in_recovery();
 pg_is_in_recovery
-------------------
 f
(1 行记录)

postgres=# select pid,application_name,client_addr,client_port,state,sync_state from pg_stat_replication;
  pid  | application_name |  client_addr   | client_port |   state   | sync_state
-------+------------------+----------------+-------------+-----------+------------
 15710 | walreceiver      | 192.168.64.150 |       58960 | streaming | async
(1 行记录)
```

验证备
```
[root@node2 postgresql]# ps -ef | grep wal
postgres  15533  15526  0 06:16 ?        00:00:01 postgres: wal receiver process   streaming 0/60179F8

[root@node2 postgresql]# su - postgres
上一次登录：三 11月 13 05:32:22 CST 2019pts/0 上

-bash-4.2$ /usr/pgsql-10/bin/pg_controldata | grep 数据库簇状态
数据库簇状态:                         正在归档恢复

-bash-4.2$ psql
psql (10.10)
输入 "help" 来获取帮助信息.

postgres=# select pg_is_in_recovery();
 pg_is_in_recovery
-------------------
 t
(1 行记录)

postgres=# select pid,application_name,client_addr,client_port,state,sync_state from pg_stat_replication;
 pid | application_name | client_addr | client_port | state | sync_state
-----+------------------+-------------+-------------+-------+------------
(0 行记录)
```

主库更新数据
```
[root@node1 postgresql]# su - postgres
上一次登录：三 11月 13 04:40:47 CST 2019pts/0 上
-bash-4.2$ psql
psql (10.10)
输入 "help" 来获取帮助信息.

postgres=# create table tb (id int4, create_time timestamp(0) without time zone);
CREATE TABLE
postgres=# insert into tb values (1, now());
INSERT 0 1
postgres=# select * from tb;
 id |     create_time
----+---------------------
  1 | 2019-11-13 04:50:29
(1 行记录)

postgres=#
```

备库验证数据
```
[root@node2 postgresql]# su - postgres
上一次登录：三 11月 13 05:34:00 CST 2019pts/0 上
-bash-4.2$ psql
psql (10.10)
输入 "help" 来获取帮助信息.

postgres=# \d
              关联列表
 架构模式 | 名称 |  类型  |  拥有者
----------+------+--------+----------
 public   | tb   | 数据表 | postgres
(1 行记录)

postgres=# select * from tb;
 id |     create_time
----+---------------------
  1 | 2019-11-13 04:50:29
(1 行记录)

postgres=# insert into tb values (1, now());
错误:  不能在一个只读模式的事务中执行INSERT
```

#### 主备切换

1. 主库停止服务
2. 备库切为主库
3. 虚拟IP漂移至新主
4. 修复原主转为新备

激活备库
```
-bash-4.2$ /usr/pgsql-10/bin/pg_ctl promote
waiting for server to promote.... 完成
server promoted
-bash-4.2$ /usr/pgsql-10/bin/pg_controldata | grep 数据库簇状态
数据库簇状态:                         在运行中
-bash-4.2$ psql
psql (10.10)
输入 "help" 来获取帮助信息.

postgres=#
postgres=# insert into tb values (3, now());
INSERT 0 1

ls /var/lib/pgsql/10/data/recovery.done
```

## Pgpool
安装 Pgpool-II 4.0.0
```
# yum install http://www.pgpool.net/yum/rpms/4.0/redhat/rhel-7-x86_64/pgpool-II-release-4.0-1.noarch.rpm
# yum install pgpool-II-pg10 pgpool-II-pg10-debuginfo pgpool-II-pg10-devel pgpool-II-pg10-extensions
```

创建用户(仅主库操作，备库自动同步)
```
[root@node1 postgresql]# su - postgres
上一次登录：三 11月 13 04:59:38 CST 2019pts/0 上
-bash-4.2$ psql
psql (10.10)
输入 "help" 来获取帮助信息.

postgres=# CREATE ROLE cluster REPLICATION LOGIN PASSWORD '123456';
CREATE ROLE
postgres=# \du
                             角色列表
 角色名称 |                    属性                    | 成员属于
----------+--------------------------------------------+----------
 cluster  | 复制                                       | {}
 postgres | 超级用户, 建立角色, 建立 DB, 复制, 绕过RLS | {}
 replica  | 复制                                       | {}
```

```
mkdir /var/log/pgpool
chown -R postgres:postgres /var/log/pgpool
```

修改配置文件
```
cat /etc/pgpool-II/pgpool.conf.sample-stream > /etc/pgpool-II/pgpool.conf
```

```
listen_addresses = '*'
backend_hostname0 = 'node1'
backend_data_directory0 = '/var/lib/pgsql/10/data'

backend_hostname1 = 'node2'
backend_port1 = 5432
backend_weight1 = 1
backend_data_directory1 = '/var/lib/pgsql/10/data'
backend_flag1 = 'ALLOW_TO_FAILOVER'

enable_pool_hba = on

sr_check_user = 'cluster'
sr_check_password = '123456'

health_check_period = 5
health_check_timeout = 20
health_check_max_retries = 10

health_check_user = 'cluster'
health_check_password = '123456'

failover_command = '/etc/pgpool-II/failover.sh %d %P %H %R'

recovery_user = 'postgres'
recovery_password = '123456'

wd_lifecheck_user = 'postgres'
wd_lifecheck_password = '123456'

recovery_1st_stage_command = 'recovery_1st_stage'

```

/etc/pgpool-II/failover.sh
```
#! /bin/sh -x
# Execute command by failover.
# special values:  %d = node id
#                  %h = host name
#                  %p = port number
#                  %D = database cluster path
#                  %m = new master node id
#                  %M = old master node id
#                  %H = new master node host name
#                  %P = old primary node id
#                  %R = new master database cluster path
#                  %r = new master port number
#                  %% = '%' character

falling_node=$1          # %d
old_primary=$2           # %P
new_primary=$3           # %H
pgdata=$4                # %R

pghome=/usr/pgsql-10
log=/var/log/pgpool/failover.log

date >> $log
echo "failed_node_id=$falling_node new_primary=$new_primary" >> $log

if [ $falling_node = $old_primary ]; then
    if [ $UID -eq 0 ]
    then
        su postgres -c "ssh -T postgres@$new_primary $pghome/bin/pg_ctl promote -D $pgdata"
    else
        ssh -T postgres@$new_primary $pghome/bin/pg_ctl promote -D $pgdata
    fi
    exit 0;
fi;
exit 0;
```

/var/lib/pgsql/10/data/recovery_1st_stage
```
#!/bin/bash -x
# Recovery script for streaming replication.

pgdata=$1
remote_host=$2
remote_pgdata=$3
port=$4

pghome=/usr/pgsql-10
archivedir=/var/lib/pgsql/archivedir
hostname=$(hostname)

ssh -T postgres@$remote_host "
rm -rf $remote_pgdata
$pghome/bin/pg_basebackup -h $hostname -U replica -D $remote_pgdata -x -c fast
rm -rf $archivedir/*

cd $remote_pgdata
cp postgresql.conf postgresql.conf.bak
sed -e 's/#*hot_standby = off/hot_standby = on/' postgresql.conf.bak > postgresql.conf
rm -f postgresql.conf.bak
cat > recovery.conf << EOT
standby_mode = 'on'
primary_conninfo = 'host="$hostname" port=$port user=replica'
restore_command = 'scp $hostname:$archivedir/%f %p'
EOT
"
```

/var/lib/pgsql/10/data/pgpool_remote_start
```
#! /bin/sh -x

pghome=/usr/pgsql-10
remote_host=$1
remote_pgdata=$2

# Start recovery target PostgreSQL server
ssh -T $remote_host $pghome/bin/pg_ctl -w -D $remote_pgdata start > /dev/null 2>&1 < /dev/null &
```

```
# vi /etc/pgpool-II/failover.sh
# vi /var/lib/pgsql/10/data/recovery_1st_stage
# vi /var/lib/pgsql/10/data/pgpool_remote_start
# chmod 755 /etc/pgpool-II/failover.sh
# chmod 755 /var/lib/pgsql/10/data/recovery_1st_stage
# chmod 755 /var/lib/pgsql/10/data/pgpool_remote_start
# chown postgres:postgres /etc/pgpool-II/failover.sh
# chown postgres:postgres -R /var/lib/pgsql/10/data
```


安装恢复模块
```
# su - postgres
$ psql template1 -c "CREATE EXTENSION pgpool_recovery"
```

修改配置 /etc/pgpool-II/pool_hba.conf
```
# echo "host    all         cluster          0.0.0.0/0          md5" >> /etc/pgpool-II/pool_hba.conf
# echo "host    all         replica          0.0.0.0/0          md5" >> /etc/pgpool-II/pool_hba.conf
# echo "host    all         postgres         0.0.0.0/0          md5" >> /etc/pgpool-II/pool_hba.conf
```

```
# pg_md5 --md5auth --username=cluster 123456
# pg_md5 --md5auth --username=replica 123456
# pg_md5 --md5auth --username=postgres 123456
```

/etc/pgpool-II/pcp.conf
```
# pg_md5 123456
e10adc3949ba59abbe56e057f20f883e
# echo "cluster:e10adc3949ba59abbe56e057f20f883e" >> /etc/pgpool-II/pcp.conf
# echo "replica:e10adc3949ba59abbe56e057f20f883e" >> /etc/pgpool-II/pcp.conf
# echo "postgres:e10adc3949ba59abbe56e057f20f883e" >> /etc/pgpool-II/pcp.conf
```

```
# systemctl enable pgpool
# systemctl status pgpool
# systemctl restart pgpool
```

登录测试
```
# su - postgres
上一次登录：三 11月 13 09:10:59 CST 2019pts/0 上
-bash-4.2$ psql postgres -h node1 -p 9999 -U postgres
用户 postgres 的口令：
psql (10.10)
输入 "help" 来获取帮助信息.

postgres=# show pool_nodes;
 node_id | hostname | port | status | lb_weight |  role   | select_cnt | load_balance_node | replication_delay | last_status_change
---------+----------+------+--------+-----------+---------+------------+-------------------+-------------------+---------------------
 0       | node1    | 5432 | up     | 0.500000  | primary | 1          | true              | 0                 | 2019-11-13 09:18:53
 1       | node2    | 5433 | down   | 0.500000  | standby | 0          | false             | 0                 | 2019-11-13 09:18:53
```

/var/lib/pgsql/.pgpass
```
node1:5432:replication:replica:123456
node2:5432:replication:replica:123456
```

```
chmod 0600 /var/lib/pgsql/.pgpass
chown postgres:postgres /var/lib/pgsql/.pgpass
```

node_id=1的standby节点状态为down，现在将它加入集群
```
pcp_attach_node -h 192.168.64.130 -p 9898 -U postgres -n 1
```
还是不行

下线节点、添加节点
```
pcp_detach_node -h 192.168.64.130 -p 9898 -U postgres -n 0
pcp_attach_node -h 192.168.64.130 -p 9898 -U postgres -n 0
```

恢复节点
```
pcp_recovery_node -h 192.168.64.130 -p 9898 -U postgres -n 1
```

