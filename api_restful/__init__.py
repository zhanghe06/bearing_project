#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: __init__.py.py
@time: 2020-02-28 21:01
"""


from flask import Flask

from logging.config import dictConfig
from api_restful.apis import api_bearing
from api_restful.blueprints import bp_bearing
from config import current_config
# from api_restful.middlewares.logger_middleware import LoggerMiddleware

app = Flask(__name__)

# app.wsgi_app = LoggerMiddleware(app.wsgi_app)

# Load Config
app.config.from_object(current_config)

# Register Blueprint
app.register_blueprint(bp_bearing)

# 配置日志
dictConfig(app.config['LOG_CONFIG'])

# Add Resource Urls
from api_restful import urls
from api_restful.user import url
