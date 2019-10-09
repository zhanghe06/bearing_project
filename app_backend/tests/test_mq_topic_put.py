#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: test_mq_topic_put.py
@time: 2019-10-03 17:50
"""

from app_common.libs.rabbit_queue import RabbitQueue
from config import current_config

mq_conf = current_config.RABBITMQ

ex = 'ex.project.topic'
rk = 'rk.project'
qn = 'test_mq'

mq = RabbitQueue(**mq_conf)
mq.open_channel()
mq.exchange_declare(exchange_name=ex)
mq.queue_declare(queue_name=qn)  # 发消息也需要声明，避免数据无法到达队列而丢弃
mq.queue_bind(exchange_name=ex, queue_name=qn, routing_key=rk)


def put():
    message = '123456'
    mq.basic_publish(message, exchange=ex, routing_key=rk)


if __name__ == '__main__':
    # python app_backend/tests/test_mq_topic_put.py
    put()
