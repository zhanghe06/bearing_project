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

### 字符编码
```
DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_general_ci
```

1. utf8与utf8mb4（utf8 most bytes 4）

utf8字符集表示一个字符需要使用1～4个字节，但是我们常用的一些字符使用1～3个字节就可以表示了。
而在MySQL中字符集表示一个字符所用最大字节长度在某些方面会影响系统的存储和性能，所以设计MySQL的大叔偷偷的定义了两个概念：

- utf8mb3：阉割过的utf8字符集，只使用1～3个字节表示字符。
- utf8mb4：正宗的utf8字符集，使用1～4个字节表示字符。

有一点需要大家十分的注意：在MySQL中utf8是utf8mb3的别名，所以之后在MySQL中提到utf8就意味着使用1~3个字节来表示一个字符，如果大家有使用4字节编码一个字符的情况，比如存储一些emoji表情啥的，那请使用utf8mb4。

2. 字符集、连接字符集、排序字符集

utf8mb4对应的排序字符集有utf8mb4_unicode_ci、utf8mb4_general_ci.

utf8mb4_unicode_ci和utf8mb4_general_ci的对比：

- 准确性：

utf8mb4_unicode_ci是基于标准的Unicode来排序和比较，能够在各种语言之间精确排序
utf8mb4_general_ci没有实现Unicode排序规则，在遇到某些特殊语言或者字符集，排序结果可能不一致。
但是，在绝大多数情况下，这些特殊字符的顺序并不需要那么精确。

- 性能

utf8mb4_general_ci在比较和排序的时候更快
utf8mb4_unicode_ci在特殊情况下，Unicode排序规则为了能够处理特殊字符的情况，实现了略微复杂的排序算法。
但是在绝大多数情况下发，不会发生此类复杂比较。相比选择哪一种collation，使用者更应该关心字符集与排序规则在db里需要统一。

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
