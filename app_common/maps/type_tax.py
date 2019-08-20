#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: type_tax.py
@time: 2018-08-01 00:40
"""

from __future__ import unicode_literals

from flask_babel import lazy_gettext as _

from app_common.maps.default import DEFAULT_SEARCH_CHOICES_INT, DEFAULT_SELECT_CHOICES_INT

# 含税类型（1:含税,2:不含税）
TYPE_TAX_HAS = 1
TYPE_TAX_NOT = 2

TYPE_TAX_DICT = {
    TYPE_TAX_HAS: _('Has Tax'),  # 含税
    TYPE_TAX_NOT: _('Not Tax'),  # 不含税
}

TYPE_TAX_SELECT_CHOICES = DEFAULT_SELECT_CHOICES_INT + TYPE_TAX_DICT.items()  # 选择
TYPE_TAX_SEARCH_CHOICES = DEFAULT_SEARCH_CHOICES_INT + TYPE_TAX_DICT.items()  # 搜索
