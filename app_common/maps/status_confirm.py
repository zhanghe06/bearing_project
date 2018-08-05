#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: status_confirm.py
@time: 2018-07-27 20:23
"""


from __future__ import unicode_literals

from flask_babel import lazy_gettext as _


# 确认状态（0:等待确认,1:确认成功,2:确认失败）
STATUS_CONFIRM_NO = 0
STATUS_CONFIRM_OK = 1
STATUS_CONFIRM_ER = 1

STATUS_CONFIRM_DICT = {
    0: _('Pending Confirm'),  # 等待确认
    1: _('Confirm Success'),  # 确认成功
    2: _('Confirm Failure'),  # 确认失败
}
