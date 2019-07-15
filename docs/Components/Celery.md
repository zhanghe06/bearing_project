# Celery

http://docs.celeryproject.org/en/latest/

http://docs.jinkan.org/docs/celery/


## 用武之地

## 本地事务 vs 分布式事务 vs 消息队列

如果多张表都在同一个数据库实例上，本地事务就可以搞定

业务量很大的情况下，多表分布在不同实例上，可能就需要考虑分布式事务

但是分布式事务锁资源太耗性能，可能就要考虑消息队列避免分布式事务

用到了消息队列，那要考虑的问题变成了如何保证消息可靠
