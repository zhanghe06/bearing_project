#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: redis_token_bucket.py
@time: 2019-07-26 16:54
"""

# https://github.com/titan-web/rate-limit

# https://www.cnblogs.com/kangoroo/p/7700758.html

import abc
import time
from datetime import datetime

import redis


class TokenBucket(object):
    # rate是令牌发放速度，capacity是桶的大小
    def __init__(self, rate, capacity):
        self._rate = rate
        self._capacity = capacity
        self._current_amount = 0
        self._last_consume_time = int(time.time())

    # token_amount是发送数据需要的令牌数
    def consume(self, token_amount):
        increment = (int(time.time()) - self._last_consume_time) * self._rate  # 计算从上次发送到这次发送，新发放的令牌数量
        self._current_amount = min(
            increment + self._current_amount, self._capacity)  # 令牌数量不能超过桶的容量
        if token_amount > self._current_amount:  # 如果没有足够的令牌，则不能发送数据
            return False
        self._last_consume_time = int(time.time())
        self._current_amount -= token_amount
        return True


class RedisTokenBucket(object):
    def __init__(self, rate, capacity):
        """
        :param rate: 令牌发放速度
        :param capacity: 桶的大小
        """
        self._rate = rate
        self._capacity = capacity
        self._current_amount = 0
        self._last_consume_time = int(time.time())

    def consume(self, token_amount):
        increment = (int(time.time() - self._last_consume_time)) * self._rate
        self._current_amount = min(increment + self._current_amount, self._capacity)

        if token_amount > self._current_amount:
            return False

        self._last_consume_time = int(time.time())
        self._current_amount -= token_amount

    def produce(self):
        pass


class BaseRateLimiter(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, rate):
        self.rate = rate

    @abc.abstractmethod
    def acquire(self, count):
        return


class Cache(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        self.key = "DEFAULT"
        self.namespace = "RATELIMITER"

    @abc.abstractmethod
    def fetch_token(self, rate, key=None):
        return


class RedisTokenCache(Cache):

    def __init__(self, host, port, db=0, password=None, max_connections=None):
        Cache.__init__(self)
        self.redis = redis.Redis(
            connection_pool=
                redis.ConnectionPool(
                    host=host, port=port, db=db,
                    password=password,
                    max_connections=max_connections
                ))

    def fetch_token(self, rate=100, count=1, expire=3, key=None):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        key = ":".join([self.namespace, key if key else self.key, date])
        try:
            current = self.redis.get(key)
            if int(current if current else "0") > rate:
                raise Exception("to many requests in current second: %s" % date)
            else:
                with self.redis.pipeline() as p:
                    p.multi()
                    p.incr(key, count)
                    p.expire(key, expire)
                    p.execute()
                    return True
        except Exception as e:
            return False


class RedisRateLimiter(BaseRateLimiter):
    def __init__(self, rate, cache):
        BaseRateLimiter.__init__(self, rate)
        self.cache = cache

    def acquire(self, count=1, expire=3, key=None, callback=None):
        try:
            if isinstance(self.cache, Cache):
                return self.cache.fetch_token(rate=self.rate, count=count, expire=expire, key=key)
        except Exception as e:
            return True


if __name__ == '__main__':
    pass
