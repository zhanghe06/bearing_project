#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: type_delivery.py
@time: 2019-08-20 18:36
"""

from __future__ import unicode_literals

from flask_babel import lazy_gettext as _

from app_common.maps.default import DEFAULT_SEARCH_CHOICES_INT, DEFAULT_SELECT_CHOICES_INT

# 销货类型（1:正常销售,2:赠送样品,3:盘亏,4:拆卸）
TYPE_DELIVERY_NORMAL = 1
TYPE_DELIVERY_GIVE = 2
TYPE_DELIVERY_LOSS = 3
TYPE_DELIVERY_TEARDOWN = 4

TYPE_DELIVERY_DICT = {
    TYPE_DELIVERY_NORMAL: _('Normal Delivery'),  # 正常销售
    TYPE_DELIVERY_GIVE: _('Give Sample'),  # 赠送样品
    TYPE_DELIVERY_LOSS: _('Inventory Loss'),  # 盘亏
    TYPE_DELIVERY_TEARDOWN: _('Teardown'),  # 拆卸
}

TYPE_DELIVERY_SELECT_CHOICES = DEFAULT_SELECT_CHOICES_INT + TYPE_DELIVERY_DICT.items()  # 选择
TYPE_DELIVERY_SEARCH_CHOICES = DEFAULT_SEARCH_CHOICES_INT + TYPE_DELIVERY_DICT.items()  # 搜索
