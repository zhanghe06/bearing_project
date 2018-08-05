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


# 含税类型（0:不含税,1:含税）
TYPE_TAX_NOT = 0
TYPE_TAX_HAS = 1

TYPE_TAX_DICT = {
    0: _('Not Tax'),  # 不含税
    1: _('Has Tax'),  # 含税
}

TYPE_TAX_CHOICES = TYPE_TAX_DICT.items()
