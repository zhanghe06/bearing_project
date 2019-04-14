#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: client_rabbitmq.py
@time: 2019-04-09 00:31
"""

from __future__ import unicode_literals

import pika

from config import current_config


RABBITMQ = current_config.RABBITMQ


rabbitmq_client = pika.BlockingConnection(pika.ConnectionParameters(**RABBITMQ))
