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

from app_common.maps.default import DEFAULT_SEARCH_CHOICES_INT, DEFAULT_SELECT_CHOICES_INT

# 认证类型（1:账号,2:邮箱,3:手机,4:QQ,5:微信,6:微博）
TYPE_AUTH_ACCOUNT = 1
TYPE_AUTH_EMAIL = 2
TYPE_AUTH_PHONE = 3
TYPE_AUTH_QQ = 4
TYPE_AUTH_WECHAT = 5
TYPE_AUTH_WEIBO = 6

TYPE_AUTH_DICT = {
    TYPE_AUTH_ACCOUNT: _('Account'),  # 账号
    TYPE_AUTH_EMAIL: _('Email'),  # 邮箱
    TYPE_AUTH_PHONE: _('Mobile'),  # 手机
    TYPE_AUTH_QQ: _('QQ'),  # QQ
    TYPE_AUTH_WECHAT: _('WeChat'),  # 微信
    TYPE_AUTH_WEIBO: _('WeiBo'),  # 微博
}

TYPE_AUTH_SELECT_CHOICES = DEFAULT_SELECT_CHOICES_INT + TYPE_AUTH_DICT.items()  # 选择
TYPE_AUTH_SEARCH_CHOICES = DEFAULT_SEARCH_CHOICES_INT + TYPE_AUTH_DICT.items()  # 搜索
