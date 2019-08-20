#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: type_ticket.py
@time: 2019-08-20 17:14
"""

from __future__ import unicode_literals

from flask_babel import lazy_gettext as _

from app_common.maps.default import DEFAULT_SEARCH_CHOICES_INT, DEFAULT_SELECT_CHOICES_INT

# 票据类型（1:银行,2:现金,3:支票,4:承兑）
TYPE_TICKET_BANK = 1
TYPE_TICKET_CASH = 2
TYPE_TICKET_CHECK = 3
TYPE_TICKET_ACCEPT = 4

TYPE_TICKET_DICT = {
    TYPE_TICKET_BANK: _('Bank'),  # 银行
    TYPE_TICKET_CASH: _('Cash'),  # 现金
    TYPE_TICKET_CHECK: _('Check'),  # 支票
    TYPE_TICKET_ACCEPT: _('Accept'),  # 承兑
}

TYPE_TICKET_SELECT_CHOICES = DEFAULT_SELECT_CHOICES_INT + TYPE_TICKET_DICT.items()  # 选择
TYPE_TICKET_SEARCH_CHOICES = DEFAULT_SEARCH_CHOICES_INT + TYPE_TICKET_DICT.items()  # 搜索
