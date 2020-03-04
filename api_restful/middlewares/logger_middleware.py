#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: logger_middleware.py
@time: 2020-03-01 17:56
"""

from werkzeug.wrappers import Request, Response, ResponseStream
from uuid import uuid4
import time
import logging


from werkzeug.middleware.http_proxy import ProxyMiddleware

api_logger = logging.getLogger('api')
debug_logger = logging.getLogger('debug')


class LoggerMiddleware(object):
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        debug_logger.debug('before_request')
        request = Request(environ)
        request_id = request.headers.get('X-Request-Id', str(uuid4()))  # 不带短横: uuid4().get_hex()
        request_path = request.path
        request_method = request.method
        request_args = request.args
        request_data = request.data

        req_time = time.time()

        # 响应头部注入
        def new_start_response(status, response_headers, exc_info=None):
            response_headers.append(('X-Request-Id', request_id))
            return start_response(status, response_headers, exc_info)

        res = self.wsgi_app(environ, new_start_response)

        res_time = time.time()
        latency = res_time - req_time
        # # %(request_id)s %(project)s %(url)s %(method)s %(levelname)s
        log_info = {
            'request_id': request_id,
            # 'request_path': request_path,
            # 'request_method': request_method,
            # 'request_args': request_args,
            # 'request_data': request_data,
            'latency': latency,
        }
        api_logger.info(log_info)

        debug_logger.debug('after_request')
        return res
