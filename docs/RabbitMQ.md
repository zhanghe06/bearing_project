## RabbitMQ

[http://www.rabbitmq.com](http://www.rabbitmq.com)

[https://pika.readthedocs.io/en/stable/](https://pika.readthedocs.io/en/stable/)


### 社区最佳实践

[http://www.rabbitmq.com/best-practices.html](http://www.rabbitmq.com/best-practices.html)


### 架构图

```graph
graph TD

    P1((producer 1)) --> | message | EX1[exchange]
    P2((producer 2)) --> | message | EX1[exchange]
    P3((producer 3)) --> | message | EX2[exchange]

    EX1[exchange] --> RK1[Routing Key 1]
    EX1[exchange] --> RK2[Routing Key 2]
    EX2[exchange] --> RK3[Routing Key 3]

    RK1[Routing Key 1] --> Q1(Queue 1)
    RK2[Routing Key 2] --> Q2(Queue 2)
    RK3[Routing Key 2] --> Q3(Queue 3)

    Q1(Queue 1) --> BK1[Binding Key 1]
    Q2(Queue 2) --> BK2[Binding Key 2]
    Q3(Queue 3) --> BK2[Binding Key 2]

    BK1[Binding Key] --> | message | C1((consumer 1))
    BK2[Binding Key] --> | message | C2((consumer 2))
```


### Producer 生产者

Message -> Exchange -- Routing Key -- Queue


### Consumer 消费者

Exchange -- Binding Key -- Queue -> Message


### Exchange Type 协议类型

- fanout    广播
- direct    直接交换（可以绑定多个队列, 甚至达到广播效果）
- topic     主题
- headers   头部


### Routing Key & Binding Key

- Routing Key 为一个句点号“.”分隔的字符串（我们将被句点号“.”分隔开的每一段独立的字符串称为一个单词）
- Binding Key 与 routing key 一样也是句点号“.”分隔的字符串

Binding Key 中可以存在两种特殊字符“*”与“#”, 用于做模糊匹配, 其中“*”用于匹配一个单词, “#”用于匹配多个单词（可以是零个）

一个完整的 Routing Key 可以理解为多种分类交叉组合的一种


### Queue

1. 消费者是无法订阅或者获取不存在的 MessageQueue 中信息

2. 消息被 Exchange 接受以后, 如果没有匹配的 Queue, 则会被丢弃

最佳实践:

```
consumer 和 producer 都可以创建 Queue, 如果 consumer 来创建, 避免 consumer 订阅一个不存在的 Queue 的情况.
但是这里要承担一种风险: 消息已经投递但是consumer尚未创建队列, 那么消息就会被扔到黑洞, 换句话说消息丢了;
避免这种情况的好办法就是producer和consumer都尝试创建一下queue. 
```
如果consumer在已经订阅了另外一个Queue的情况下无法完成新Queue的创建, 必须取消之前的订阅将Channel置为传输模式("transmit")才能创建新的Channel.


### Work Type 工作类型

- 订阅发布  不指定队列名称
- 生产消费  指定队列名称

```
不事先绑定队列, 消费者工作时, 系统自动创建新的临时队列
消费者永远拿到的是最新的消息
消费者关闭连接后应该删除队列
```


### 消息确认 & 数据持久化

- 消费确认  避免消费者意外中止导致消息丢失
- 数据持久  防止消息系统退出或崩溃时丢失队列和消息
- 发布确认  防止操作系统退出或崩溃时丢失在内存中的消息


### 任务系统的几种场景（间隔、定时、延时）

下面结合 RabbitMQ 来处理这些场景

- 间隔

- 定时

- 延时
