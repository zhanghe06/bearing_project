#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: rabbit_queue.py
@time: 2019-04-08 16:48
"""

import pika
from pika.exceptions import AMQPConnectionError, AMQPChannelError, ConnectionClosed
import json
from retry import retry


class RabbitQueue(object):
    """
    队列
    """
    def __init__(self, conn):
        self.conn = conn
        self.channel = self.conn.channel()

    def close_conn(self):
        """
        关闭连接
        :return:
        """
        self.conn.close()

    def exchange_declare(self, exchange_name='amq.topic'):
        """
        交换机申明
        :param exchange_name:
        :return:
        """
        self.channel.exchange_declare(
            exchange=exchange_name,
            exchange_type='topic',
            durable=True,
        )

    def queue_declare(self, queue_name='', **arguments):
        """
        队列申明
        :param queue_name:
        :param arguments:
        :return:
        """
        self.channel.queue_declare(
            queue=queue_name,
            durable=True,
            arguments=arguments,
        )

    def queue_bind(self, exchange_name='amq.topic', queue_name='', binding_key='#'):
        """
        绑定队列
        :param exchange_name:
        :param queue_name:
        :param binding_key:
        :return:
        """
        self.channel.queue_bind(
            exchange=exchange_name,
            queue=queue_name,
            routing_key=binding_key
        )

    def basic_qos(self):
        self.channel.basic_qos(prefetch_count=1)

    def basic_publish(self, message, exchange='amq.topic', routing_key='.'):
        """
        推送队列消息
        :param message:
        :param exchange:
        :param routing_key:
        :return:
        """
        if isinstance(message, dict):
            message = json.dumps(message)
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)
        )
        print(" [x] Sent %r" % (message,))

    def ack_message(self, delivery_tag):
        """
        Note that `channel` must be the same Pika channel instance via which
        the message being acknowledged was retrieved (AMQP protocol constraint).
        """
        if self.channel.is_open:
            self.channel.basic_ack(delivery_tag)
        else:
            # Channel is already closed, so we can't acknowledge this message;
            # log and/or do something that makes sense for your app in this case.
            pass

    def basic_get(self, queue_name):
        """
        消费队列消息(非阻塞)
        :return:
        """
        method_frame, header_frame, body = self.channel.basic_get(queue_name)
        if method_frame:
            print(" [x]  Get %r" % (body,))
            print(method_frame, header_frame, body)
            self.ack_message(delivery_tag=method_frame.delivery_tag)
        else:
            print('No message returned')

    @retry(AMQPConnectionError, delay=5, jitter=(1, 3))
    def basic_consume(self, on_message_callback, queue_name):
        """
        消费队列消息(阻塞)
        """
        self.channel.basic_consume(consumer_callback=on_message_callback, queue=queue_name)

        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
        # Don't recover connections closed by server
        except (ConnectionClosed, AMQPChannelError):
            pass
        self.close_conn()

    def example_basic_consume_with_callback(self):
        """
        示例: 消费队列消息(阻塞)
        :return:
        """
        def callback(ch, method, properties, body):
            print(" [x]  Get %r" % (body,))
            # raise Exception('test')
            ch.ack_message(delivery_tag=method.delivery_tag)

        self.basic_consume(callback)


# class RabbitQueueDelay(object):
#     """
#     延时队列
#     q_d_client = RabbitQueueDelay('amq.direct', q_name, ttl=3600*24)
#     """
#     def __init__(self, exchange, queue_name, exchange_type='direct', durable=True, **arguments):
#         self.exchange = exchange
#         self.queue_name = queue_name
#         self.delay_queue_name = '%s_delay' % queue_name
#         self.exchange_type = exchange_type
#         self.durable = durable
#         self.arguments = arguments
#         # print u'实例化附加参数:', arguments
#         self.conn = get_conn()
#
#         self.channel = self.conn.channel()
#         self.channel.confirm_delivery()
#         self.channel.queue_declare(queue=queue_name, durable=durable)
#
#         # We need to bind this channel to an exchange, that will be used to transfer
#         # messages from our delay queue.
#         self.channel.queue_bind(exchange=self.exchange,
#                                 queue=queue_name)
#
#         # 延时队列定义
#         self.delay_channel = self.conn.channel()
#         self.delay_channel.confirm_delivery()
#
#         # This is where we declare the delay, and routing for our delay channel.
#         self.delay_channel.queue_declare(queue=self.delay_queue_name, durable=durable, arguments={
#             'x-message-ttl': arguments.get('ttl', 5)*1000,  # Delay until the message is transferred in milliseconds.
#             'x-dead-letter-exchange': self.exchange,  # Exchange used to transfer the message from A to B.
#             'x-dead-letter-routing-key': self.queue_name  # Name of the queue we want the message transferred to.
#         })
#
#     def get_conn(self):
#     """
#     获取连接
#     :return:
#     """
#     if not _client_conn.get('conn'):
#         conn_mq = pika.BlockingConnection(
#             pika.ConnectionParameters(
#                 host=RABBIT_MQ.get('host', '127.0.0.1'),
#                 port=RABBIT_MQ.get('port', 5672),
#                 virtual_host=RABBIT_MQ.get('virtual_host', '/'),
#                 heartbeat_interval=RABBIT_MQ.get('heartbeat_interval', 0),
#                 retry_delay=RABBIT_MQ.get('retry_delay', 3)
#             )
#         )
#         _client_conn['conn'] = conn_mq
#         return conn_mq
#     else:
#         return _client_conn['conn']
#
#     def close_conn(self):
#         """
#         关闭连接
#         :return:
#         """
#         if _client_conn.get('conn'):
#             self.conn.close()
#             _client_conn.pop('conn')
#
#     def put(self, message):
#         """
#         推送队列消息
#         :param message:
#         :return:
#         """
#         if isinstance(message, dict):
#             message = json.dumps(message)
#         self.delay_channel.basic_publish(exchange='',
#                                          routing_key=self.delay_queue_name,
#                                          body=message,
#                                          properties=pika.BasicProperties(
#                                              delivery_mode=2 if self.durable else 1,  # make message persistent
#                                          ))
#         print " [x] Sent %r" % (message,)
#
#     def get(self):
#         """
#         获取队列消息
#         :return:
#         """
#         # data = self.channel.basic_get(self.queue_name)
#         # print data
#         method_frame, header_frame, body = self.channel.basic_get(self.queue_name)
#         if method_frame:
#             print " [x]  Get %r" % (body,)
#             print method_frame, header_frame, body
#             self.channel.basic_ack(method_frame.delivery_tag)
#         else:
#             print('No message returned')
#
#     def get_block(self):
#         """
#         获取队列消息(阻塞)
#         direct 模式下多进程消费，进程轮流获取单个消息
#         :return:
#         """
#         def callback(ch, method, properties, body):
#             try:
#                 print " [x]  Get %r" % (body,)
#                 # raise Exception('test')
#                 ch.basic_ack(delivery_tag=method.delivery_tag)
#             except Exception as e:
#                 print traceback.print_exc()
#                 raise e
#
#         self.consume(callback)
#
#     def consume(self, callback):
#         """
#         消费
#         """
#         # 处理队列
#         self.channel.basic_consume(consumer_callback=callback, queue=self.queue_name)
#         try:
#             self.channel.start_consuming()
#         except KeyboardInterrupt:
#             self.channel.stop_consuming()
#         self.close_conn()


if __name__ == '__main__':
    from app_backend.clients.client_rabbitmq import rabbitmq_client
    rq = RabbitQueue(rabbitmq_client)
    rq.exchange_declare()
    rq.queue_declare()
    binding_keys = ['', '']
    for bind_key in binding_keys:
        rq.queue_bind(binding_key=bind_key)


"""
这种方式 如果队列中前面的消息延时时间大于后面的时间 那么后面的消息将会被堵塞 应为消息在被消费前才会去检查过期时间
参考官方文档发现“Only when expired messages reach the head of a queue will they actually be discarded (or dead-lettered).”只有当过期的消息到了队列的顶端（队首），才会被真正的丢弃或者进入死信队列。
"""
