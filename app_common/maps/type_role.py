#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: type_role.py
@time: 2018-03-18 00:12
"""

from __future__ import unicode_literals

from flask_babel import lazy_gettext as _

from app_common.maps.default import DEFAULT_SEARCH_CHOICES_INT, DEFAULT_SELECT_CHOICES_INT

# 角色类型（1:系统,2:销售,3:经理,4:库管,5:财务,6:采购）
TYPE_ROLE_SYSTEM = 1
TYPE_ROLE_SALES = 2
TYPE_ROLE_MANAGER = 3
TYPE_ROLE_STOREKEEPER = 4
TYPE_ROLE_ACCOUNTANT = 5
TYPE_ROLE_PURCHASER = 6

TYPE_ROLE_DICT = {
    TYPE_ROLE_SYSTEM: _('System'),  # 系统
    TYPE_ROLE_SALES: _('Sales'),  # 销售
    TYPE_ROLE_MANAGER: _('Manager'),  # 经理
    TYPE_ROLE_STOREKEEPER: _('Storekeeper'),  # 库管
    TYPE_ROLE_ACCOUNTANT: _('Finance'),  # 财务
    TYPE_ROLE_PURCHASER: _('Purchaser'),  # 采购
}

TYPE_ROLE_SELECT_CHOICES = DEFAULT_SELECT_CHOICES_INT + TYPE_ROLE_DICT.items()  # 选择
TYPE_ROLE_SEARCH_CHOICES = DEFAULT_SEARCH_CHOICES_INT + TYPE_ROLE_DICT.items()  # 搜索
