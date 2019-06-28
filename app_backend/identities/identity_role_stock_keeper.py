#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: identity_role_stock_keeper.py
@time: 2019-06-27 00:54
"""


from __future__ import unicode_literals

from flask_principal import RoleNeed

from app_backend.permissions import SectionActionNeed


def setup(identity):
    # 赋予整体角色权限
    identity.provides.add(RoleNeed('库管'))
    # 库存-----------------------------------------------------------------------
    # 库存创建
    identity.provides.add(SectionActionNeed('inventory', 'add'))
    # 库存统计
    identity.provides.add(SectionActionNeed('inventory', 'stats'))
    # 仓库-----------------------------------------------------------------------
    # 仓库创建
    identity.provides.add(SectionActionNeed('warehouse', 'add'))
    # 仓库统计
    identity.provides.add(SectionActionNeed('warehouse', 'stats'))
    # 货架-----------------------------------------------------------------------
    # 货架创建
    identity.provides.add(SectionActionNeed('rack', 'add'))
    # 货架统计
    identity.provides.add(SectionActionNeed('rack', 'stats'))
