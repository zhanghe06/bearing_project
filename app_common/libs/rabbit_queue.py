#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: rabbit_queue.py
@time: 2019-04-08 16:48
"""

import json
import uuid

import pika
from pika.exceptions import AMQPConnectionError, AMQPChannelError
from pika.spec import PERSISTENT_DELIVERY_MODE
from retry import retry


class RabbitQueue(object):
    """
    队列
    """
    conf = None
    conn = None
    channel = None

    def __init__(self, **conf):
        self.conf = conf
        self.open_conn()

    def open_conn(self):
        """
        打开连接
        :return:
        """
        if self.conn and self.conn.is_open:
            return
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(**self.conf))
        # self.channel = self.conn.channel()

    def close_conn(self):
        """
        关闭连接
        :return:
        """
        if not self.conn:
            return
        if self.conn.is_closed:
            print('[x] Conn is closed')
            return
        self.conn.close()

    def open_channel(self):
        """
        打开通道
        :return:
        """
        if self.channel and self.channel.is_open:
            return
        self.channel = self.conn.channel()

    def close_channel(self):
        """
        关闭通道
        :return:
        """
        if not self.channel:
            return
        if self.channel.is_closed:
            print('[x] Channel is closed')
            return
        self.channel.close()

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

    def queue_bind(self, exchange_name='amq.topic', queue_name='', routing_key='#'):
        """
        绑定队列
        :param exchange_name:
        :param queue_name:
        :param routing_key:
        :return:
        """
        self.channel.queue_bind(
            exchange=exchange_name,
            queue=queue_name,
            routing_key=routing_key
        )

    def basic_qos(self, prefetch_count=1):
        self.channel.basic_qos(prefetch_count=prefetch_count)

    def basic_publish(self, message, exchange='amq.topic', routing_key='.', message_id=None):
        """
        推送队列消息
        :param message:
        :param exchange:
        :param routing_key:
        :param message_id:
        :return:
        """
        message_id = message_id or str(uuid.uuid4())
        if isinstance(message, dict):
            message = json.dumps(message)
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=PERSISTENT_DELIVERY_MODE,
                message_id=message_id
            )
        )
        print('[x] %s Sent %r' % (message_id, message,))

    def basic_get(self, queue_name):
        """
        消费队列消息(非阻塞)
        :return:
        """
        method_frame, header_frame, body = self.channel.basic_get(queue_name)
        if method_frame:
            print('[x] %d, Get %r' % (method_frame.delivery_tag, body,))
            print(method_frame, header_frame, body)
            self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        else:
            print('No message returned')

    @retry((AMQPConnectionError, AMQPChannelError), tries=-1, delay=5, jitter=(1, 3))
    def basic_consume(self, on_message_callback, queue_name):
        """
        消费队列消息(阻塞)
        """
        try:
            self.open_conn()  # 断线重连
            self.open_channel()

            self.channel.basic_qos(prefetch_count=1)
            self.channel.basic_consume(queue=queue_name, on_message_callback=on_message_callback)
            self.channel.start_consuming()
        except KeyboardInterrupt:
            print('KeyboardInterrupt')
            self.channel.stop_consuming()
        except AMQPConnectionError as e:
            print(e.__class__.__name__)
            raise e
        except AMQPChannelError as e:
            print(e.__class__.__name__)
            raise e
        finally:
            self.close_channel()
            self.close_conn()

    def example_basic_consume_with_callback(self):
        """
        示例: 消费队列消息(阻塞)
        :return:
        """
        def callback(ch, method, properties, body):
            try:
                print('[x] %s %d, Get %r' % (properties.message_id, method.delivery_tag, body,))
                ch.basic_ack(delivery_tag=method.delivery_tag)
                print('[x] %s %d, ACK' % (properties.message_id, method.delivery_tag,))
            except Exception as e:
                ch.basic_nack(delivery_tag=method.delivery_tag)
                print('[x] %s %d, NACK' % (properties.message_id, method.delivery_tag,))
                raise e

        self.basic_consume(callback)


class RabbitQueueDelay(RabbitQueue):
    conf = None
    conn = None
    channel = None

    def __init__(self, **conf):
        super(RabbitQueueDelay, self).__init__(**conf)


"""
这种方式 如果队列中前面的消息延时时间大于后面的时间 那么后面的消息将会被堵塞 应为消息在被消费前才会去检查过期时间
参考官方文档发现“Only when expired messages reach the head of a queue will they actually be discarded (or dead-lettered).”只有当过期的消息到了队列的顶端（队首），才会被真正的丢弃或者进入死信队列。
"""
