#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: type_auth.py
@time: 2018-03-18 02:46
"""

from __future__ import unicode_literals

from flask_babel import lazy_gettext as _


# 认证类型（0:账号,1:邮箱,2:手机,3:QQ,4:微信,5:微博）
TYPE_AUTH_ACCOUNT = 0
TYPE_AUTH_EMAIL = 1
TYPE_AUTH_PHONE = 2
TYPE_AUTH_QQ = 3
TYPE_AUTH_WECHAT = 4
TYPE_AUTH_WEIBO = 5

TYPE_AUTH_DICT = {
    0: _('Account'),  # 账号
    1: _('Email'),  # 邮箱
    2: _('Mobile'),  # 手机
    3: _('QQ'),  # QQ
    4: _('WeChat'),  # 微信
    5: _('WeiBo'),  # 微博
}
