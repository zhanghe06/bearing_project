# PostgresQL

主备、集群、高可用方案

## PostgresQL + KeepaliveD（基于 Hot Standby 的异步流复制、单VIP）

至少2台机器（1主，1从）

组件
- PostgresQL(node1、node2)
- KeepaliveD(node1、node2)

特点
- VIP设置在主节点，客户端通过VIP连接数据库，从库只是作为备份，只读，单VIP情景下不对外提供服务
- 不支持读写分离
- 只能手动恢复集群，新主可以立即起来，旧主可以慢慢操作，降级为新备

可采用双VIP升级为读写分离

## PostgresQL + PgPool-II

至少3台机器（1主，1从，1池）

组件
- PostgresQL(node1、node2)
- PgPool(pool)

```
echo -e "10.0.0.11 node1\n10.0.0.12 node2\n10.0.0.13 pool" >> /etc/hosts
```

## PostgresQL + PgPool-II + HAProxy


## PgPool-II + Watchdog

至少5台机器（2 PostgresQL servers and 3 PgPool-II servers）

参考: [https://www.pgpool.net/docs/pgpool-II-4.0.1/en/html/example-cluster.html](https://www.pgpool.net/docs/pgpool-II-4.0.1/en/html/example-cluster.html)
