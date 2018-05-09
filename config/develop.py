#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: develop.py
@time: 2018-03-05 15:02
"""

from __future__ import unicode_literals

from flask_babel import lazy_gettext as _

import os
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = True

CSRF_ENABLED = True
SECRET_KEY = '\x03\xabjR\xbbg\x82\x0b{\x96f\xca\xa8\xbdM\xb0x\xdbK%\xf2\x07\r\x8c'

PREFERRED_URL_SCHEME = 'https'


# 会话配置
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_NAME_BACKEND = 's_a'

PERMANENT_SESSION_LIFETIME = timedelta(minutes=20)  # 登录状态保持，默认31天
REMEMBER_COOKIE_DURATION = timedelta(days=14)       # 记住登录状态，默认365天
REMEMBER_COOKIE_SECURE = True                       # 限制 “Remember Me” cookie 在某些安全通道下有用 （典型地 HTTPS）。默认值： None
REMEMBER_COOKIE_HTTPONLY = True                     # 保护 “Remember Me” cookie 不能通过客户端脚本访问。 默认值： False
REMEMBER_COOKIE_NAME_BACKEND = 'r_a'

REDIS_SESSION_PREFIX_BACKEND = 's:a:'


# requests 超时设置
REQUESTS_TIME_OUT = (30, 30)

HOST = '0.0.0.0'

# 数据库 MySQL
DB_MYSQL = {
    'host': HOST,
    'user': 'root',
    'passwd': '123456',
    'port': 3306,
    'db': 'bearing_project'
}

SQLALCHEMY_DATABASE_URI_MYSQL = \
    'mysql+mysqldb://%s:%s@%s:%s/%s?charset=utf8' % \
    (DB_MYSQL['user'], DB_MYSQL['passwd'], DB_MYSQL['host'], DB_MYSQL['port'], DB_MYSQL['db'])

SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI_MYSQL
# SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 打开自动提交 官方已经移除(http://flask-sqlalchemy.pocoo.org/2.1/changelog/#version-2-0)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_SIZE = 5        # 默认 pool_size=5
SQLALCHEMY_MAX_OVERFLOW = 10    # 默认 10 连接池达到最大值后可以创建的连接数
SQLALCHEMY_POOL_TIMEOUT = 10    # 默认 10秒
SQLALCHEMY_POOL_RECYCLE = 500   # 配置要小于 数据库配置 wait_timeout
SQLALCHEMY_ECHO = False


# 缓存，队列
REDIS = {
    'host': HOST,
    'port': 6379,
    # 'password': '123456'  # redis-cli AUTH 123456
}

REDIS_URL = 'redis://:%s@%s' % (REDIS['password'], REDIS['host']) \
    if REDIS.get('password') else 'redis://%s' % REDIS['host']


DOCUMENT_INFO = {
    'TITLE': '',        # 标题
    'KEYWORDS': '',     # 关键词
    'DESCRIPTION': '',  # 描述
    'AUTHOR': '',       # 作者
    'PROJECT_NAME': _('Website Name'),  # 网站名称
    'ICP_CODE': '沪ICP备12024750号',
    'APP_NAME': _('App Name'),  # 应用名称
}

PER_PAGE_FRONTEND = 20
PER_PAGE_BACKEND = 20


BABEL_DEFAULT_LOCALE = 'zh'     # en, zh, zh_Hans_CN
BABEL_DEFAULT_TIMEZONE = 'UTC'


AJAX_SUCCESS_MSG = {
    'result': True,
    'msg': '',
}

AJAX_FAILURE_MSG = {
    'result': False,
    'msg': '',
}


# 图形验证码参数配置
CAPTCHA_CONFIG = {
    'size': (68, 34),
    'fg_color': (180, 180, 180),
    'line_color': (100, 100, 100),
    'point_color': (100, 100, 100)
}
# 图形验证码支持类型
CAPTCHA_ENTITY = [
    'reg',      # 注册
    'login',    # 登录
    'reset'     # 重置密码（找回密码）
]


# 第三方开放授权登陆
GITHUB_OAUTH = {
    'consumer_key': '0ccd9367a1f81288b127',
    'consumer_secret': '711b6afcc938d760e9e57215dfbdcb115150ddc6',
    'request_token_params': {'scope': 'user:email'},
    'base_url': 'https://api.github.com/',
    'request_token_url': None,
    'access_token_method': 'POST',
    'access_token_url': 'https://github.com/login/oauth/access_token',
    'authorize_url': 'https://github.com/login/oauth/authorize'
}

QQ_OAUTH = {
    'consumer_key': '101187283',  # QQ_APP_ID
    'consumer_secret': '993983549da49e384d03adfead8b2489',  # QQ_APP_KEY
    'base_url': 'https://graph.qq.com',
    'request_token_url': None,
    'request_token_params': {'scope': 'get_user_info'},
    'access_token_url': '/oauth2.0/token',
    'authorize_url': '/oauth2.0/authorize',
}

WEIBO_OAUTH = {
    'consumer_key': '909122383',
    'consumer_secret': '2cdc60e5e9e14398c1cbdf309f2ebd3a',
    'request_token_params': {'scope': 'email,statuses_to_me_read'},
    'base_url': 'https://api.weibo.com/2/',
    'authorize_url': 'https://api.weibo.com/oauth2/authorize',
    'request_token_url': None,
    'access_token_method': 'POST',
    'access_token_url': 'https://api.weibo.com/oauth2/access_token',
    # since weibo's response is a shit, we need to force parse the content
    'content_type': 'application/json',
}
