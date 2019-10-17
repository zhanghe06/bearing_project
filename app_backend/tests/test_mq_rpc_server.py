#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: test_mq_rpc_server.py
@time: 2019-10-08 18:08
"""

import json

import pika

from config import current_config

mq_conf = current_config.RABBITMQ


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


class RpcServer(object):
    corr_id = ''
    qn = 'rpc_queue'
    fun_map = {}

    def __init__(self, **conf):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(**conf))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.qn)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.qn, on_message_callback=self.on_request)

    def register_fun(self, func_name):
        if func_name not in globals():
            print(" [x] function %s doesn't exist" % func_name)
            return
        self.fun_map[func_name] = globals()[func_name]

    def on_request(self, ch, method, props, body):

        req_body_obj = json.loads(body)
        req_method = req_body_obj['req_method']
        req_payload = req_body_obj['req_payload']

        args = req_payload['args']
        kwargs = req_payload['kwargs']

        args_fmt = (', '.join([str(i) for i in list(args) + ['%s=%s' % (i, j) for i, j in kwargs.items()]]))
        print(" [.] %s(%s), correlation_id: %s" % (req_method, args_fmt, props.correlation_id))

        result = self.fun_map[req_method](*args, **kwargs)
        res_body_obj = {'res_result': result}
        res_body = json.dumps(res_body_obj)

        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(correlation_id=props.correlation_id),
            body=res_body
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        if not self.fun_map:
            print(" [x] The registered function is empty")
            return
        print(" [x] Awaiting RPC requests")
        self.channel.start_consuming()


def server():
    rpc_server = RpcServer(**mq_conf)
    rpc_server.register_fun('fib')
    rpc_server.run()


if __name__ == '__main__':
    # python app_backend/tests/test_mq_rpc_server.py
    server()
