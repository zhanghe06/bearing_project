#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: operation_log.py
@time: 2020-03-01 01:22
"""


# from flask.signals import Namespace
import logging
import json
from blinker import Namespace
from api_restful import app
# udp_logger = logging.getLogger('udp')
# http_logger = logging.getLogger('http')

_signal = Namespace()


signal_operation_log = _signal.signal('signal_operation_log')


@signal_operation_log.connect_via(app)
def operation_log(sender, **extra):
    """
    操作日志
    :param sender:
    :param extra:
    :return:
    """
    print(sender, extra)

    # api_log_msg = {'tag': 'api.log', 'json': extra}

    # tcp_logger.info(json.dumps(extra))
    # udp_logger.info(api_log_msg)
    # http_logger.info(extra)
    # http_logger.info(api_log_msg)

# 调试日志请求
# ➜  ~ nc -lk 192.168.4.1 9880
