#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: status_default.py
@time: 2018-08-09 15:06
"""


from __future__ import unicode_literals

from flask_babel import lazy_gettext as _


# 默认状态（0:空,1:默认）
STATUS_DEFAULT_NO = 0
STATUS_DEFAULT_OK = 1

STATUS_DEFAULT_DICT = {
    0: _('-'),  # 空
    1: _('Default'),  # 默认
}
