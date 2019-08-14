#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: test_redis_sub.py
@time: 2019-08-14 21:03
"""

from app_common.libs.redis_pub_sub import RedisPubSub

redis_pub_sub_obj = RedisPubSub('test')


def run():
    for i in redis_pub_sub_obj.sub('k'):
        print(i)


if __name__ == '__main__':
    run()
