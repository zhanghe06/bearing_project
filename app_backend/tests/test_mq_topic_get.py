#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: test_mq_topic_get.py
@time: 2019-10-03 17:50
"""

import time

from app_common.libs.rabbit_queue import RabbitQueue
from config import current_config

mq_conf = current_config.RABBITMQ

ex = 'ex.project.topic'
bk = ['rk.*', '*.project']
qn = 'test_mq'

mq = RabbitQueue(**mq_conf)
mq.open_channel()
mq.exchange_declare(exchange_name=ex)
mq.queue_declare(queue_name=qn)

for rk in bk:
    mq.queue_bind(exchange_name=ex, queue_name=qn, routing_key=rk)


def get():
    def callback(ch, method, properties, body):
        try:
            print(' [x]  %d, Get %r' % (method.delivery_tag, body,))
            # raise Exception('test')  # 测试业务异常
            time.sleep(1)  # 测试连接异常（手动停止rabbitmq服务）
            mq.ack_message(delivery_tag=method.delivery_tag)
        except Exception as e:
            mq.nack_message(delivery_tag=method.delivery_tag)
            # print(e.message)
            raise e

    mq.basic_consume(queue_name=qn, on_message_callback=callback)


if __name__ == '__main__':
    get()
