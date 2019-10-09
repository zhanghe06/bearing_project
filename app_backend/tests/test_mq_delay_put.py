#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: test_mq_delay_put.py
@time: 2019-10-09 17:50
"""

from app_common.libs.rabbit_queue import RabbitQueue
from config import current_config

mq_conf = current_config.RABBITMQ

ex = 'ex.project.topic'
rk = 'rk.project'
qn = 'test_mq'

ttl = 10
ex_delay = '.'.join([ex, 'delay', str(ttl)])
qn_delay = '_'.join([qn, 'delay', str(ttl)])
arguments_delay = {
    'x-message-ttl': ttl * 1000,
    'x-dead-letter-exchange': ex,
    'x-dead-letter-routing-key': rk
}

mq = RabbitQueue(**mq_conf)
mq.open_channel()
mq.exchange_declare(exchange_name=ex)
mq.queue_declare(queue_name=qn)
mq.queue_bind(exchange_name=ex, queue_name=qn, routing_key=rk)

mq.exchange_declare(exchange_name=ex_delay)
mq.queue_declare(
    queue_name=qn_delay,
    **arguments_delay
)
mq.queue_bind(exchange_name=ex_delay, queue_name=qn_delay, routing_key=rk)


def put():
    message = '123456'
    mq.basic_publish(message, exchange=ex_delay, routing_key=rk)


if __name__ == '__main__':
    # python app_backend/tests/test_mq_delay_put.py
    put()
