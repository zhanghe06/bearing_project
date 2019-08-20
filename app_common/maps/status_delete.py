#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: status_delete.py
@time: 2018-03-17 16:53
"""

from __future__ import unicode_literals

from flask_babel import lazy_gettext as _

# 删除状态（0:未删除，1:已删除）
STATUS_DEL_NO = 0
STATUS_DEL_OK = 1

STATUS_DEL_DICT = {
    STATUS_DEL_NO: _('Not Deleted'),  # 未删除
    STATUS_DEL_OK: _('Deleted'),  # 已删除
}
