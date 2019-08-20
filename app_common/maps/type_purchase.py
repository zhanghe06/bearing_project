#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: type_purchase.py
@time: 2019-08-20 18:31
"""

from __future__ import unicode_literals

from flask_babel import lazy_gettext as _

from app_common.maps.default import DEFAULT_SEARCH_CHOICES_INT, DEFAULT_SELECT_CHOICES_INT

# 进货类型（1:正常采购,2:获赠样品,3:盘盈,4:组装）
TYPE_PURCHASE_NORMAL = 1
TYPE_PURCHASE_RECEIVE = 2
TYPE_PURCHASE_PROFIT = 3
TYPE_PURCHASE_ASSEMBLY = 4

TYPE_PURCHASE_DICT = {
    TYPE_PURCHASE_NORMAL: _('Normal Purchase'),  # 正常采购
    TYPE_PURCHASE_RECEIVE: _('Receive Sample'),  # 获赠样品
    TYPE_PURCHASE_PROFIT: _('Inventory Profit'),  # 盘盈
    TYPE_PURCHASE_ASSEMBLY: _('Assembly'),  # 组装
}

TYPE_PURCHASE_SELECT_CHOICES = DEFAULT_SELECT_CHOICES_INT + TYPE_PURCHASE_DICT.items()  # 选择
TYPE_PURCHASE_SEARCH_CHOICES = DEFAULT_SEARCH_CHOICES_INT + TYPE_PURCHASE_DICT.items()  # 搜索
