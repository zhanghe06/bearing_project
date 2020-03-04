#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: urls.py
@time: 2020-02-28 21:21
"""


from __future__ import unicode_literals

from uuid import uuid4
import logging
import time
from collections import defaultdict
from flask import jsonify, request, g, make_response
from werkzeug.exceptions import NotFound, InternalServerError
from api_restful.signals.operation_log import signal_operation_log
from api_restful import app

# api_logger = logging.getLogger('api')
debug_logger = logging.getLogger('debug')

SUCCESS_MSG = app.config['API_SUCCESS_MSG']
FAILURE_MSG = app.config['API_FAILURE_MSG']


@app.before_request
def api_before_request():
    request_id = request.headers.get('X-Request-Id', str(uuid4()))  # 不带短横: uuid4().get_hex()
    g.request_id = request_id
    debug_logger.debug('before_request')
    g.req_time = time.time()


@app.after_request
def after_request(response):
    request_id = g.get('request_id', str(uuid4()))
    g.request_id = request_id
    debug_logger.debug('after_request')

    # 头部注入
    response.headers.add('X-Request-Id', request_id)

    g.status_code = response.status_code
    g.project = app.name
    g.res_time = time.time()
    latency = time.time() - g.req_time
    g.latency = latency
    # api_log = defaultdict(lambda: '-')
    # api_logger.info('-')

    # 操作日志
    operation_log = {
        'project': app.name,
        'latency': latency,
        'client_host': request.host,
        'client_addr': request.remote_addr,
        'req_id': request_id,
        'req_method': request.method,
        'req_path': request.path,
        'req_json': request.json,
        'req_args': request.args.to_dict(),
        'res_status_code': response.status_code,
        'res_json': {},
    }
    # Get请求错误时记录返回，正确返回忽略，避免日志过大
    if request.method in ['GET', 'HEAD', 'OPTIONS'] and response.status_code / 2 != 100:
        operation_log['res_json'] = response.json
    if request.method in ['POST', 'PUT', 'DELETE']:
        operation_log['res_json'] = response.json
    signal_operation_log.send(app, **operation_log)
    return response  # 必须返回response


# @app.after_request
# def after_request(response):
#     request_id = g.get('request_id', str(uuid4()))
#     g.request_id = request_id
#     debug_logger.debug('after_request')
#
#     g.status_code = response.status_code
#
#     # 头部注入
#     response.headers.add('X-Request-Id', request_id)
#
#     return response  # 必须返回response


# @app.teardown_request
# def teardown_request(exception=None):
#     request_id = g.get('request_id', str(uuid4()))
#     g.request_id = request_id
#     debug_logger.debug('teardown_request')
#
#     g.project = app.name
#     g.res_time = time.time()
#     g.latency = g.res_time - g.req_time
#
#     # 接口日志
#     g.api_log = defaultdict(lambda: '-')
#     g.api_log['project_name'] = app.name
#
#     if exception:
#         exception_info = {
#             'module': exception.__class__.__module__,
#             'name': exception.__class__.__name__,
#             'message': exception.message,
#         }
#         g.api_log['exception'] = '%(module)s.%(name)s: %(message)s' % exception_info
#         api_logger.error(dict(g.api_log))
#     else:
#         api_logger.info(dict(g.api_log))
#     return exception


@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def heartbeat():
    return jsonify(SUCCESS_MSG.copy())


# 全局路由错误
@app.errorhandler(NotFound.code)
def url_not_found(error):
    return make_response(
        jsonify(
            {
                'msg': '路径错误' or error.description,
                'result': False,
                # 'status': exceptions.NotFound.code,
            }
        ),
        NotFound.code
    )


# 全局异常错误(DEBUG模式生效)
@app.errorhandler(Exception)
def exception(error):
    return make_response(
        jsonify(
            {
                'msg': error.message or InternalServerError.description,
                'result': False,
                # 'status': InternalServerError.code,
            }
        ),
        InternalServerError.code
    )
