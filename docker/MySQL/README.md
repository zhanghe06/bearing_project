# MySQL

https://hub.docker.com/_/mysql/
```
$ sudo docker pull mysql:5.7
```

环境变量 | 说明
--- | ---
MYSQL_ROOT_PASSWORD | 创建root用户密码
MYSQL_USER | 创建用户
MYSQL_PASSWORD | 创建用户密码

## 配置文件

修改配置，支持大文件导入，避免报错: ERROR 2006 (HY000)

查看默认配置（4M）
```
mysql> show global variables like "%max_allowed_packet%";
+--------------------------+------------+
| Variable_name            | Value      |
+--------------------------+------------+
| max_allowed_packet       | 4194304    |
| slave_max_allowed_packet | 1073741824 |
+--------------------------+------------+
```

修改为 512M
```
>>> 512*1024*1024
536870912
```

```
mysql> set global max_allowed_packet=536870912;
Query OK, 0 rows affected (0.00 sec)
```

## 自定义配置

/etc/my.cnf
my.ini
