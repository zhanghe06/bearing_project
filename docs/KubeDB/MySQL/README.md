# MySQL

[https://kubedb.com/docs/0.12.0/guides/mysql/](https://kubedb.com/docs/0.12.0/guides/mysql/)


## MGR的局限性：
- 仅支持InnodDB存储引擎的表，并且每个表必须有主键ID, 用做wirte set的冲突检测 
- 必须启用GTID特性，binlog日志格式必须为row模式 
- 目前一个MGR集群最多支持9个节点 
- 不支持外健的save point特性，无法做全局间的约束检测和部分回滚 
- 二进制日志不支持binlog event checksum

## 升级路径

[https://dev.mysql.com/doc/refman/8.0/en/upgrade-paths.html](https://dev.mysql.com/doc/refman/8.0/en/upgrade-paths.html)

应该检查支持的MySQL升级路径，以了解您可以升级到哪个版本，不支持跳过版本的升级。  
例如，支持从5.7.9+升级到8.0，但不支持直接从MySQL 5.6升级到8.0。
