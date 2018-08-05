#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: client_redis.py
@time: 2018-03-23 15:06
"""

import redis

from config import current_config

REDIS = current_config.REDIS

redis_client = redis.Redis(**REDIS)
