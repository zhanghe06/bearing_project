#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: stress_testing.py
@time: 2019-10-04 14:40
"""


from __future__ import unicode_literals

from flask import (
    request,
    flash,
    render_template,
    url_for,
    redirect,
    abort,
    jsonify,
    Blueprint,
)

from app_backend.clients.client_rabbitmq import consumer
from app_common.libs.rabbit_queue import RabbitQueue
from config import current_config

mq_conf = current_config.RABBITMQ


ex = 'ex.project.topic'
rk = 'rk.project'
bk = ['rk.*', '*.project']
qn = 'test_mq'

# 定义蓝图
bp_stress_testing = Blueprint('stress_testing', __name__, url_prefix='/stress_testing')


@bp_stress_testing.route('/rabbitmq_put', methods=['GET', 'POST'])
def rabbitmq_put():
    """
    siege -c 100 -r 100 -b http://0.0.0.0:8160/stress_testing/rabbitmq_put
    测试用例：
    1、测试连接数 - 关闭连接
    2、测试连接数 - 不关连接
    :return:
    """
    producer = RabbitQueue(**mq_conf)
    producer.open_channel()
    producer.exchange_declare(exchange_name=ex)
    producer.queue_declare(queue_name=qn)  # 发消息也需要定义，避免数据存储不到队列
    producer.queue_bind(exchange_name=ex, queue_name=qn, routing_key=rk)

    message = '123456'
    producer.basic_publish(message, exchange=ex, routing_key=rk)
    producer.close_conn()  # 注意关闭
    return jsonify({'message': message})


@bp_stress_testing.route('/rabbitmq_get', methods=['GET', 'POST'])
def rabbitmq_get():
    """
    siege -c 100 -r 100 -b http://0.0.0.0:8160/stress_testing/rabbitmq_get
    测试用例：
    1、测试连接数 - 关闭连接
    2、测试连接数 - 不关连接
    :return:
    """
    try:
        consumer.open_channel()
        consumer.exchange_declare(exchange_name=ex)
        consumer.queue_declare(queue_name=qn)

        for rk in bk:
            consumer.queue_bind(exchange_name=ex, queue_name=qn, routing_key=rk)

        def callback(ch, method, properties, body):
            try:
                print(" [x]  %s, Get %r" % (method.delivery_tag, body,))
                raise Exception('test')  # 测试业务异常
                # time.sleep(1)  # 测试连接异常（手动停止rabbitmq服务）
                consumer.ack_message(delivery_tag=method.delivery_tag)
            except Exception as ec:
                consumer.nack_message(delivery_tag=method.delivery_tag)
                raise ec

        consumer.basic_consume(on_message_callback=callback, queue_name=qn)
    except Exception as e:
        print(e.message)
    finally:
        # consumer.close_channel()
        return jsonify({'message': ''})
