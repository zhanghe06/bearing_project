#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: type_current.py
@time: 2019-08-17 23:39
"""

from __future__ import unicode_literals

from flask_babel import lazy_gettext as _

from app_common.maps.default import DEFAULT_SEARCH_CHOICES_INT, DEFAULT_SELECT_CHOICES_INT

# 往来类型（1:客户,2:渠道）
TYPE_CURRENT_CUSTOMER = 1
TYPE_CURRENT_SUPPLIER = 2

TYPE_CURRENT_DICT = {
    TYPE_CURRENT_CUSTOMER: _('Customer'),  # 客户
    TYPE_CURRENT_SUPPLIER: _('Supplier'),  # 渠道
}

TYPE_CURRENT_SELECT_CHOICES = DEFAULT_SELECT_CHOICES_INT + TYPE_CURRENT_DICT.items()  # 选择
TYPE_CURRENT_SEARCH_CHOICES = DEFAULT_SEARCH_CHOICES_INT + TYPE_CURRENT_DICT.items()  # 搜索
