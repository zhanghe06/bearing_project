#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: resource.py
@time: 2020-03-01 15:42
"""

from __future__ import print_function
from __future__ import unicode_literals

import time
from functools import wraps

from flask import jsonify, make_response
from flask_restful import abort
from werkzeug.exceptions import NotFound, InternalServerError


def api_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            res = func(*args, **kwargs)
            return res
        except Exception as e:
            return make_response(
                jsonify(
                    {
                        'msg': e.message,
                        'result': False,
                        # 'status': InternalServerError.code,
                    }
                ),
                InternalServerError.code
            )
        finally:
            end_time = time.time()
            run_time = end_time - start_time
            msg = '%s.%s 运行时间: %0.2fS' % (func.__module__, func.__name__, run_time)
            print(msg)

    return wrapper
