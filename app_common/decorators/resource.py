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
from werkzeug.exceptions import HTTPException, NotFound, InternalServerError
from sqlalchemy.exc import DatabaseError
from redis.exceptions import RedisError


def api_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            res = func(*args, **kwargs)
            return res
        # 框架内部异常
        # e.description 框架内置信息，需要屏蔽
        except HTTPException as e:
            return make_response(
                jsonify(
                    {
                        'msg': e.data.get('message', e.message),
                        'result': False,
                    }
                ),
                e.code
            )
        # 组件连接异常（数据库、消息、缓存等）
        # 拦截具体消息
        except DatabaseError as e:
            return make_response(
                jsonify(
                    {
                        'msg': '数据库异常' or ', '.join(e.args) or e.message,
                        'result': False,
                    }
                ),
                InternalServerError.code
            )
        except RedisError as e:
            return make_response(
                jsonify(
                    {
                        'msg': '缓存异常' or ', '.join(e.args) or e.message,
                        'result': False,
                    }
                ),
                InternalServerError.code
            )
        # 框架外部异常
        # raise Exception("123")
        # raise Exception("123", "456")
        except Exception as e:
            # print('Function name:', func.__name__)
            # print('Function args:', args, kwargs)
            # print('Exception error:', e)
            # print('Exception module:', e.__class__.__module__)
            # print('Exception class name:', e.__class__.__name__)
            return make_response(
                jsonify(
                    {
                        'msg': ', '.join(e.args) or e.message,
                        'result': False,
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
