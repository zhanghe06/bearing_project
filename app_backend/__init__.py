#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: __init__.py
@time: 2018-03-06 00:00
"""

from __future__ import unicode_literals

from logging.config import dictConfig
from config import current_config

from flask import Flask
from flask_login import LoginManager
from flask_moment import Moment
from flask_oauthlib.client import OAuth
from flask_principal import Principal
import flask_excel as excel

from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel, gettext as _

from app_common.libs.redis_session import RedisSessionInterface
from app_backend.clients.client_redis import redis_client


app = Flask(__name__)
app.config.from_object(current_config)
app.config['REMEMBER_COOKIE_NAME'] = app.config['REMEMBER_COOKIE_NAME_BACKEND']
app.session_cookie_name = app.config['SESSION_COOKIE_NAME_BACKEND']
app.session_interface = RedisSessionInterface(
    redis=redis_client,
    prefix=app.config['REDIS_SESSION_PREFIX_BACKEND'],
)

login_manager = LoginManager()
login_manager.init_app(app)  # setup_app 方法已淘汰
login_manager.login_view = 'auth.index'
login_manager.login_message = _('Please log in to access this page.')
login_manager.login_message_category = 'info'   # 设置消息分类
login_manager.localize_callback = _             # 设置翻译回调
login_manager.session_protection = "strong"     # 设置安全等级（basic、strong、None）


db = SQLAlchemy()
db.init_app(app)

# Moment 时间插件
moment = Moment(app)

# 权限管理插件
principals = Principal(app)

# 国际化 本地化
babel = Babel(app)

excel.init_excel(app)

# 第三方开放授权登录
oauth = OAuth(app)

# GitHub
oauth_github = oauth.remote_app(
    'github',
    **app.config['GITHUB_OAUTH']
)

# QQ
oauth_qq = oauth.remote_app(
    'qq',
    **app.config['QQ_OAUTH']
)

# WeiBo
oauth_weibo = oauth.remote_app(
    'weibo',
    **app.config['WEIBO_OAUTH']
)

# Google
# 要银子，妹的


# 配置日志
# dictConfig(app.config['LOG_CONFIG'])

# 这个 import 语句放在这里, 防止views, models import发生循环import
from app_backend.models import bearing_project

from app_backend import views

from app_backend.views.captcha import bp_captcha
from app_backend.views.customer import bp_customer
from app_backend.views.user import bp_user
from app_backend.views.user_auth import bp_auth


# 注册蓝图
app.register_blueprint(bp_captcha)
app.register_blueprint(bp_customer)
app.register_blueprint(bp_user)
app.register_blueprint(bp_auth)

# 导入自定义过滤器
from app_backend import filters
