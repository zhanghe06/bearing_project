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


# 角色类型（0:默认,1:系统,2:销售,3:经理,4:库管,5:财务）
TYPE_ROLE_DEFAULT = 0
TYPE_ROLE_SYSTEM = 1
TYPE_ROLE_SALES = 2
TYPE_ROLE_MANAGER = 3
TYPE_ROLE_STOREKEEPER = 4
TYPE_ROLE_ACCOUNTANT = 5

TYPE_ROLE_DICT = {
    0: _('Default'),  # 默认
    1: _('System'),  # 系统
    2: _('Sales'),  # 销售
    3: _('Manager'),  # 经理
    4: _('Storekeeper'),  # 库管
    5: _('Finance'),  # 财务
}

TYPE_ROLE_CHOICES = TYPE_ROLE_DICT.items()
