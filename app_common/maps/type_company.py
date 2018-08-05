#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: type_company.py
@time: 2018-03-19 00:02
"""

from __future__ import unicode_literals

from flask_babel import lazy_gettext as _


# 认证类型（0:未知,1:中间商2:最终用户）
TYPE_COMPANY_DEFAULT = 0
TYPE_COMPANY_MIDDLEMAN = 1
TYPE_COMPANY_END_USER = 2

TYPE_COMPANY_DICT = {
    0: _('Unknown'),  # 未知
    1: _('Middle Man'),  # 中间商
    2: _('Final User'),  # 最终用户
}

TYPE_COMPANY_CHOICES = TYPE_COMPANY_DICT.items()
