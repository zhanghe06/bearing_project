## MariaDB Cluster

[MariaDB Galera Cluster](https://mariadb.com/kb/en/library/getting-started-with-mariadb-galera-cluster/)

1. [how-to-set-up-a-virtual-machine-template](https://mariadb.com/resources/blog/setting-up-a-mariadb-enterprise-cluster-part-1-how-to-set-up-a-virtual-machine-template/)

2. [how-to-set-up-a-mariadb-cluster](https://mariadb.com/resources/blog/setting-up-a-mariadb-enterprise-cluster-part-2-how-to-set-up-a-mariadb-cluster/)

3. [setup-ha-proxy-load-balancer-with-read-and-write-pools](https://mariadb.com/resources/blog/setup-mariadb-enterprise-cluster-part-3-setup-ha-proxy-load-balancer-with-read-and-write-pools/)


### 优点

- 真正的多主架构，任何节点都可以进行读写
- 同步复制，各节点间无延迟且节点宕机不会导致数据丢失
- 紧密耦合，所有节点均保持相同状态，节点间无不同数据
- 无需主从切换操作或使用VIP
- 热Standby，在Failover过程中无停机时间（由于不需要Failover）
- 自动节点配置，无需手工备份当前数据库并拷贝至新节点
- 支持InnoDB存储引擎
- 对应于透明，无需更改应用或是进行极小的更改
- 无需进行读写分离


### 集群恢复

