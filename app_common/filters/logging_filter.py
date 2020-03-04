#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: logging_filter.py
@time: 2020-02-20 17:33
"""


import logging
from uuid import uuid4

from flask import request, g, has_request_context, current_app


class ContextFilter(logging.Filter):

    def filter(self, record):
        if has_request_context():
            record.request_path = request.path
            record.method = request.method
            record.host = request.host
            record.agent = request.headers.get('User-Agent', '-')
            record.ip = request.environ.get('REMOTE_ADDR', '-')
            record.request_id = g.get('request_id', str(uuid4()))
            record.project = g.get('project', '-')
            record.latency = g.get('latency', 0.000)
            record.status_code = g.get('status_code', '-')
        else:
            record.request_path = '-'
            record.method = '-'
            record.host = '-'
            record.agent = '-'
            record.ip = '-'
            record.request_id = '-'
            record.project = '-'
            record.latency = 0.000
            record.status_code = '-'
        return True
