#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: __init__.py
@time: 2019-05-12 09:53
"""

from __future__ import unicode_literals

from collections import namedtuple

from flask_principal import Permission, RoleNeed

from config import current_config

PERMISSION_ENABLED = current_config.PERMISSION_ENABLED


class BasePermission(Permission):
    """
    自定义权限控制
    """

    def allows(self, identity):
        if not PERMISSION_ENABLED:
            return True  # 权限全局开关 (True:禁用权限控制)
        else:
            return super(BasePermission, self).allows(identity)


SectionNeed = namedtuple('Need', ['section'])
SectionActionNeed = namedtuple('Need', ['section', 'action'])
SectionActionItemNeed = namedtuple('ItemNeed', ['section', 'action', 'item_id'])

# -------------------------------------------------------------
# 角色类型 0:默认,1:系统,2:销售,3:经理,4:库管,5:财务,6:采购
roles = [
    '默认',
    '系统',
    '销售',
    '经理',
    '库管',
    '财务',
    '采购',
]

# 角色权限
permission_role_default = BasePermission(RoleNeed('默认'))
permission_role_administrator = BasePermission(RoleNeed('系统'))
permission_role_sales = BasePermission(RoleNeed('销售'))
permission_role_manager = BasePermission(RoleNeed('经理'))
permission_role_stock_keeper = BasePermission(RoleNeed('库管'))
permission_role_accountant = BasePermission(RoleNeed('财务'))
permission_role_purchaser = BasePermission(RoleNeed('采购'))
