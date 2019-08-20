#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: test_redis_sub.py
@time: 2019-08-17 15:29
"""
import time

from app_backend import redis_client
from app_common.decorators.exception import ignore_exception
from app_common.libs.redis_pub_sub import RedisPubSub

redis_pub_sub_obj = RedisPubSub('test', redis_client=redis_client)


@ignore_exception
def sub(retry_num=0):
    if retry_num > 0:
        print('Retry: %d' % retry_num)
    for message in redis_pub_sub_obj.sub('t'):
        print(message)


def run():
    """守护运行"""
    retry_num = 0
    while 1:
        sub(retry_num)
        time.sleep(3)
        retry_num += 1


if __name__ == '__main__':
    run()
