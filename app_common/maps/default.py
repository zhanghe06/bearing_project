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
default_search_choices_int = [(-1, _('All'))]  # 需要copy, 不要直接引用
default_search_choice_option_int = -1

default_select_choices_int = [(0, _('Choose an option'))]  # 需要copy, 不要直接引用
default_select_choice_option_int = 0

# 字符索引
default_search_choices_str = [('', _('All'))]  # 需要copy, 不要直接引用
default_search_choice_option_str = ''

default_select_choices_str = [('', _('Choose an option'))]  # 需要copy, 不要直接引用
default_select_choice_option_str = ''
