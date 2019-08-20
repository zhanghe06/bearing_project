#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: test_redis_pub.py
@time: 2019-08-17 15:29
"""

from app_backend import redis_client
from app_common.libs.redis_pub_sub import RedisPubSub

redis_pub_sub_obj = RedisPubSub('test', redis_client=redis_client)


def pub():
    redis_pub_sub_obj.pub('t', '123456')


if __name__ == '__main__':
    pub()
