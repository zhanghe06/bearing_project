# RabbitMQ

[http://www.rabbitmq.com](http://www.rabbitmq.com)

[https://pika.readthedocs.io/en/stable/](https://pika.readthedocs.io/en/stable/)


## 社区最佳实践

[http://www.rabbitmq.com/best-practices.html](http://www.rabbitmq.com/best-practices.html)


## 架构图

```graph
graph LR

    P1((producer01)) --> | message | EX1[exchange]
    P2((producer02)) --> | message | EX1[exchange]
    P3((producer03)) --> | message | EX2[exchange]

    EX1[exchange] --> RK1[RoutingKey01]
    EX1[exchange] --> RK2[RoutingKey02]
    EX2[exchange] --> RK3[RoutingKey03]

    RK1[RoutingKey01] --> Q1(Queue01)
    RK2[RoutingKey02] --> Q2(Queue02)
    RK3[RoutingKey03] --> Q3(Queue03)

    Q1(Queue01) --> BK1[BindingKey01]
    Q2(Queue02) --> BK2[BindingKey02]
    Q3(Queue03) --> BK2[BindingKey02]

    BK1[BindingKey] --> | message | C1((consumer01))
    BK2[BindingKey] --> | message | C2((consumer02))
```


## 项目结构

<escape>
<table>
    <tr>
        <th>Project</th>
        <th>Exchange</th>
        <th>Queue</th>
        <th>Routing Key</th>
        <th>Binding Key</th>
    </tr>
    <tr>
        <td rowspan="5">项目（生产者）</td>
    </tr>
    <tr>
        <td>EX</td>
        <td></td>
        <td>record.a.create</td>
        <td></td>
    </tr>
    <tr>
        <td>EX</td>
        <td></td>
        <td>record.b.create</td>
        <td></td>
    </tr>
    <tr>
        <td>EX</td>
        <td></td>
        <td>record.a.delete</td>
        <td></td>
    </tr>
    <tr>
        <td>EX</td>
        <td></td>
        <td>record.b.delete</td>
        <td></td>
    </tr>
    <tr>
        <td rowspan="3">项目（消费者A）</td>
    </tr>
    <tr>
        <td>EX</td>
        <td>QA</td>
        <td></td>
        <td>record.a.create</td>
    </tr>
    <tr>
        <td>EX</td>
        <td>QA</td>
        <td></td>
        <td>record.a.delete</td>
    </tr>
    <tr>
        <td rowspan="3">项目（消费者B）</td>
    </tr>
    <tr>
        <td>EX</td>
        <td>QB</td>
        <td></td>
        <td>record.b.create</td>
    </tr>
    <tr>
        <td>EX</td>
        <td>QB</td>
        <td></td>
        <td>record.b.delete</td>
    </tr>

</table>
</escape>


## Producer 生产者

Message -> Exchange -- Routing Key -- Queue


## Consumer 消费者

Exchange -- Binding Key -- Queue -> Message


## Exchange Type 协议类型

- fanout    广播
- direct    直接交换（可以绑定多个队列, 甚至达到广播效果）
- topic     主题
- headers   头部

声明 durable 不能动态从 true 变为 false, 报错`PRECONDITION_FAILED`, 需要手动删除


## Routing Key & Binding Key

- Routing Key 为一个句点号“.”分隔的字符串（我们将被句点号“.”分隔开的每一段独立的字符串称为一个单词）
- Binding Key 与 routing key 一样也是句点号“.”分隔的字符串

Binding Key 中可以存在两种特殊字符“\*”与“#”, 用于做模糊匹配, 其中“\*”用于匹配一个单词, “#”用于匹配多个单词（可以是零个）

一个完整的 Routing Key 可以理解为多种分类交叉组合的一种


## Queue

1. 消费者是无法订阅或者获取不存在的 MessageQueue 中信息

2. 消息被 Exchange 接受以后, 如果没有匹配的 Queue, 则会被丢弃

最佳实践:

```
consumer 和 producer 都可以创建 Queue, 如果 consumer 来创建, 避免 consumer 订阅一个不存在的 Queue 的情况.
但是这里要承担一种风险: 消息已经投递但是consumer尚未创建队列, 那么消息就会被扔到黑洞, 换句话说消息丢了;
避免这种情况的好办法就是producer和consumer都尝试创建一下queue. 
```
如果consumer在已经订阅了另外一个Queue的情况下无法完成新Queue的创建, 必须取消之前的订阅将Channel置为传输模式("transmit")才能创建新的Channel.


## Work Type 工作类型

- 订阅发布  不指定队列名称
- 生产消费  指定队列名称

```
不事先绑定队列, 消费者工作时, 系统自动创建新的临时队列
消费者永远拿到的是最新的消息
消费者关闭连接后应该删除队列
```


## 消息确认 & 数据持久化

- 消费确认  避免消费者意外中止导致消息丢失
- 数据持久  防止消息系统退出或崩溃时丢失队列和消息
- 发布确认  防止操作系统退出或崩溃时丢失在内存中的消息


**确认种类**

- 消息发送确认
    - 是否到达交换器
    - 是否到达队列

- 消费接收确认

**AcknowledgeMode 确认模式**

- NONE 不确认
- AUTO 自动确认
- MANUAL 手动确认

**Acknowledger**
 - Ack
 - Nack
 - Reject

**autoDelete**
```
Queue: 当所有消费客户端连接断开后，是否自动删除队列
true: 宕机期间的消息则会丢失（适用于时效性的场景，比如短信验证码发送）
false: 接收包括宕机期间的消息

Exchange: 当所有绑定队列都不在使用时，是否自动删除交换器
```

**持久化配置**

- 队列持久化，重启队列还在
- 消息持久化，重启消息还在

Queue持久化
```
durable=true        # 持久化
exclusive=false     # 排他性
```

Message持久化
```
delivery_mode=2
```

若消息没有持久化，RabbitMQ重启之后，Unacked和Ready全部丢失。  
当消息持久化后，RabbitMQ被重启之后，Unacked会回到Ready中。


## consumer Acknowledgements and publisher confirms

[https://www.rabbitmq.com/confirms.html](https://www.rabbitmq.com/confirms.html)

consumer Acknowledgements

动作 | 描述 | 说明
--- | --- | ---
basic.ack | 肯定确认 | 消息删除
basic.nack | 否定确认 | 消息删除/重新入队（参数控制）
basic.reject | 否定确认 | 消息删除

publisher confirms


## Channel Prefetch Setting (QoS)

[https://www.rabbitmq.com/confirms.html#channel-qos-prefetch](https://www.rabbitmq.com/confirms.html#channel-qos-prefetch)


## 任务系统的几种场景（间隔、定时、延时）

下面结合 RabbitMQ 来处理这些场景

- 间隔

- 定时

- 延时


## rabbitmqctl

```
rabbitmqctl list_connections | wc -l
rabbitmqctl list_channels | wc -l
rabbitmqctl list_queues name messages_ready messages_unacknowledged
```

## 关于 conn 和 channel

1. 一个进程一个conn(TCP连接)
2. 多个channel共享一个conn，实践中，channel与conn的比例无需过高，若任务过多，可多开进程
