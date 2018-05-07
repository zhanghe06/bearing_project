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
default_choices_int = [(-1, _('All'))]  # 需要copy, 不要直接引用
default_choice_option_int = -1

# 字符索引
default_choices_str = [('', _('All'))]  # 需要copy, 不要直接引用
default_choice_option_str = ''
