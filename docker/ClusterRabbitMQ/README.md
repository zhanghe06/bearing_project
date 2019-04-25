# RabbitMQ Clustering Guide && Highly Available (Mirrored) Queues

Clustering Guide: [https://www.rabbitmq.com/clustering.html](https://www.rabbitmq.com/clustering.html)

Highly Available (Mirrored) Queues: [https://www.rabbitmq.com/ha.html](https://www.rabbitmq.com/ha.html)

- 集群节点对等
- 除了消息队列，数据、状态均在节点间复制
- 默认情况，队列的内容位于单个节点（声明队列的节点）上


## 集群主节点切换

可能产生的问题

1. 消息可能丢弃（从节点未及时同步主节点的消息）
2. 消息可能重发（从节点存在主节点已经确认消息）

解决方案

1. [https://www.rabbitmq.com/ha.html#confirms-transactions](https://www.rabbitmq.com/ha.html#confirms-transactions)
2. [https://www.rabbitmq.com/ha.html#cancellation](https://www.rabbitmq.com/ha.html#cancellation)
