#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: default.py
@time: 2018-03-23 01:48
"""

from __future__ import unicode_literals

from flask_babel import lazy_gettext as _

# 整数索引（默认）
DEFAULT_SEARCH_CHOICES_INT = [(-1, _('All'))]  # 需要copy, 不要直接引用
DEFAULT_SEARCH_CHOICES_INT_OPTION = -1

DEFAULT_SELECT_CHOICES_INT = [(0, _('Choose an option'))]  # 需要copy, 不要直接引用
DEFAULT_SELECT_CHOICES_INT_OPTION = 0

# 字符索引
DEFAULT_SEARCH_CHOICES_STR = [('', _('All'))]  # 需要copy, 不要直接引用
DEFAULT_SEARCH_CHOICES_STR_OPTION = ''

DEFAULT_SELECT_CHOICES_STR = [('', _('Choose an option'))]  # 需要copy, 不要直接引用
DEFAULT_SELECT_CHOICES_STR_OPTION = ''
