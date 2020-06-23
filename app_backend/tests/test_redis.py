#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: test_redis.py
@time: 2020-06-19 00:13
"""

from app_backend.clients.client_redis import redis_client


def func():

    redis_client.set('test', 123)
    a = redis_client.get('test')
    print(type(a), a)   # (<type 'str'>, '123')

    b = redis_client.incr('test', 0)
    print(type(b), b)   # (<type 'int'>, 123)


if __name__ == '__main__':
    func()
