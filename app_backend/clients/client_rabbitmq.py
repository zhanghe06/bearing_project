#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: client_rabbitmq.py
@time: 2019-04-09 00:31
"""

from __future__ import unicode_literals

from app_common.libs.rabbit_queue import RabbitQueue
from config import current_config

mq_conf = current_config.RABBITMQ

consumer = RabbitQueue(**mq_conf)
