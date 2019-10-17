#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: test_mq_rpc_client.py
@time: 2019-10-08 18:09
"""

import pika
import uuid
import json

from config import current_config

mq_conf = current_config.RABBITMQ


class RpcClient(object):
    response = ''
    corr_id = ''
    qn = 'rpc_queue'
    rk = qn

    def __init__(self, **conf):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(**conf))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, req_method='', *args, **kwargs):
        print(" [x] RPC Requesting")
        self.response = ''
        self.corr_id = str(uuid.uuid4())
        # print(" [.] fib(%s), correlation_id: %s" % (n, self.corr_id))
        req_payload = {
            'args': args,
            'kwargs': kwargs,
        }
        body_obj = {
            'req_method': req_method,
            'req_payload': req_payload,
        }

        args_fmt = (', '.join([str(i) for i in list(args) + ['%s=%s' % (i, j) for i, j in kwargs.items()]]))
        print(" [.] %s(%s), correlation_id: %s" % (req_method, args_fmt, self.corr_id))

        self.channel.basic_publish(
            exchange='',
            routing_key=self.rk,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(body_obj)
        )
        while not self.response:
            self.connection.process_data_events()  # todo 超时
        return self.response


def client():
    rpc_client = RpcClient(**mq_conf)
    response = rpc_client.call('fib', 30)
    print(" [.] Got %r" % response)


if __name__ == '__main__':
    # python app_backend/tests/test_mq_rpc_client.py
    client()
