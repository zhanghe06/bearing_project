#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: status_audit.py
@time: 2018-04-05 22:55
"""


from __future__ import unicode_literals

from flask_babel import lazy_gettext as _


# 审核状态（0:等待审核,1:审核成功,2:审核失败）
STATUS_AUDIT_NO = 0
STATUS_AUDIT_OK = 1
STATUS_AUDIT_ER = 2

STATUS_AUDIT_DICT = {
    0: _('Pending Audit'),  # 等待审核
    1: _('Audit Success'),  # 审核成功
    2: _('Audit Failure'),  # 审核失败
}
