#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: route.py
@time: 2019-06-26 23:12
"""

from __future__ import print_function
from __future__ import unicode_literals

import time
from functools import wraps


def route_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            func_res = func(*args, **kwargs)
            return func_res
        except Exception as e:
            print(e.message)
            return '123232'
        finally:
            end_time = time.time()
            run_time = end_time - start_time
            msg = '%s.%s 运行时间: %0.2fS' % (func.__module__, func.__name__, run_time)
            print(msg)

    return wrapper


def log_api_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            func_res = func(*args, **kwargs)
            return func_res
        except Exception as e:
            print(e.message)
        finally:
            end_time = time.time()
            run_time = end_time - start_time
            msg = '%s.%s 运行时间: %0.2fS' % (func.__module__, func.__name__, run_time)
            print(msg)

    return wrapper


if __name__ == '__main__':
    pass
