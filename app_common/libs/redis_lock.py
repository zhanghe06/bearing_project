#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: redis_lock.py
@time: 2018-09-20 11:05
"""


import redis


class RedisDistributedLock(object):
    """
    Redis 分布式锁
    """
    def __init__(self, name, namespace='d_lock', redis_client=None, **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        self.__conn = redis_client or redis.Redis(**redis_kwargs)
        self.key = '%s:%s' % (namespace, name)

    def get_lock(self, request_id='0'):
        """
        获取锁
        :param request_id:
        :return: bool(获取状态)
        """
        # EX second ：设置键的过期时间为 second 秒。
        # PX millisecond ：设置键的过期时间为 millisecond 毫秒。
        # NX ：只在键不存在时，才对键进行设置操作。
        # XX ：只在键已经存在时，才对键进行设置操作。
        lock_status = bool(self.__conn.set(self.key, request_id, ex=30, px=None, nx=True, xx=False))
        print(lock_status)
        return lock_status

    def del_lock(self, request_id='0'):
        """
        释放锁
        :return:
        """
        pipe = self.__conn.pipeline()
        pipe.watch(self.key)  # 防止事务过程释放其他资源的锁
        try:
            pipe.multi()
            if request_id == pipe.get(self.key):  # 仅能释放自己的锁
                # get 与 delete 是2个命令，不能保证原子性，需要使用 watch 监听锁的变化
                pipe.delete(self.key)
            pipe.execute()
        except redis.exceptions.WatchError:
            pipe.reset()

if __name__ == '__main__':
    redis_lock_obj = RedisDistributedLock('app')
    redis_lock_obj.get_lock()
    redis_lock_obj.del_lock()

# 遗留问题: 如果业务事务执行时间超过锁过期时间, 锁被自动释放了, 如何处理?
# 锁过期时间怎么定: 业务事务多长时间才算是有问题的事务?
# request_id 可以设置为业务事务的 uuid

# A事务提交, 准备释放锁；此时因锁超时被回收, 恰巧被B事务获取, A事务不能释放不是自己的锁
