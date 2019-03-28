## MariaDB

https://hub.docker.com/_/mariadb/
```
$ sudo docker pull mariadb:10.1.23
```

环境变量 | 说明
--- | ---
MYSQL_ROOT_PASSWORD | 创建root用户密码
MYSQL_USER | 创建用户
MYSQL_PASSWORD | 创建用户密码


查看环境变量
```
$ sh env.sh
```

客户端连接
```
$ sh cli.sh
```

建库建表
```
$ sh db_init.sh
```

备份数据
```
$ sh db_dump.sh [db_name]
$ sh db_dump_all.sh
```

### 监控指标

- QPS   每秒处理的查询数
- TPS   每秒处理的事务数（InnoDB）
- IOPS  每秒磁盘进行的I/O操作次数

计算方式
```
# QPS
Questions = SHOW GLOBAL STATUS LIKE 'Questions';
Uptime = SHOW GLOBAL STATUS LIKE 'Uptime';
QPS=Questions/Uptime

# TPS
Com_commit = SHOW GLOBAL STATUS LIKE 'Com_commit';
Com_rollback = SHOW GLOBAL STATUS LIKE 'Com_rollback';
Uptime = SHOW GLOBAL STATUS LIKE 'Uptime';
TPS=(Com_commit + Com_rollback)/Uptime
```
