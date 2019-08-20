#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: type_account.py
@time: 2019-08-17 23:22
"""

from __future__ import unicode_literals

from flask_babel import lazy_gettext as _

from app_common.maps.default import DEFAULT_SEARCH_CHOICES_INT, DEFAULT_SELECT_CHOICES_INT

# 账目类型（1:收款,2:付款,3:退回,4:退出）
TYPE_ACCOUNT_RECEIPT = 1
TYPE_ACCOUNT_PAYMENT = 2
TYPE_ACCOUNT_HAND_BACK = 3
TYPE_ACCOUNT_SEND_BACK = 4

TYPE_ACCOUNT_DICT = {
    TYPE_ACCOUNT_RECEIPT: _('Receipt'),  # 收款
    TYPE_ACCOUNT_PAYMENT: _('Payment'),  # 付款
    TYPE_ACCOUNT_HAND_BACK: _('Hand Back'),  # 退回
    TYPE_ACCOUNT_SEND_BACK: _('Send Back'),  # 退出
}

TYPE_ACCOUNT_SELECT_CHOICES = DEFAULT_SELECT_CHOICES_INT + TYPE_ACCOUNT_DICT.items()  # 选择
TYPE_ACCOUNT_SEARCH_CHOICES = DEFAULT_SEARCH_CHOICES_INT + TYPE_ACCOUNT_DICT.items()  # 搜索
