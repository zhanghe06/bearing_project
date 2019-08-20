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

from app_common.maps.default import DEFAULT_SEARCH_CHOICES_INT, DEFAULT_SELECT_CHOICES_INT

# 认证类型（1:中间商2:最终用户）
TYPE_COMPANY_MIDDLEMAN = 1
TYPE_COMPANY_FINAL_USER = 2

TYPE_COMPANY_DICT = {
    TYPE_COMPANY_MIDDLEMAN: _('Middle Man'),  # 中间商
    TYPE_COMPANY_FINAL_USER: _('Final User'),  # 最终用户
}

TYPE_COMPANY_SELECT_CHOICES = DEFAULT_SELECT_CHOICES_INT + TYPE_COMPANY_DICT.items()  # 选择
TYPE_COMPANY_SEARCH_CHOICES = DEFAULT_SEARCH_CHOICES_INT + TYPE_COMPANY_DICT.items()  # 搜索
