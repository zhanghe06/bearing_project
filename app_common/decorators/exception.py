#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: exception.py
@time: 2019-07-29 18:50
"""

from __future__ import print_function
from __future__ import unicode_literals

import time
from functools import wraps


def ignore_exception(func):
    @wraps(func)  # 为了保留被装饰函数的函数名和帮助文档信息
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            print(res)
            return res
        except Exception as e:
            print('Function name:', func.__name__)
            print('Function args:', args, kwargs)
            print('Exception error:', e)
            print('Exception module:', e.__class__.__module__)
            print('Exception class name:', e.__class__.__name__)

    return wrapper


def log_api_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            res = func(*args, **kwargs)
            print(res)
            return res
        except Exception as e:
            print(e.message)
            raise e
        finally:
            end_time = time.time()
            run_time = end_time - start_time
            msg = '%s.%s 运行时间: %0.2fS' % (func.__module__, func.__name__, run_time)
            print(msg)

    return wrapper


if __name__ == '__main__':
    @ignore_exception
    def test_ignore():
        raise Exception('test ignore')


    @log_api_exception
    def test_log_api():
        raise Exception('test log api')


    test_ignore()
    test_log_api()
