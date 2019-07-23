#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: identity_role_accountant.py
@time: 2019-06-27 00:54
"""

from __future__ import unicode_literals

from flask_principal import RoleNeed

from app_backend.identities import setup_section, setup_section_action

# 模块通用操作
role_accountant_section_action = {
    # 基础模块
    'user': ['search', 'stats', 'get'],
    # 资源模块 - 销售
    'customer': ['add', 'search', 'stats', 'export', 'get', 'edit', 'del', 'audit', 'print'],
    'sales_order': ['search', 'stats', 'get'],
    'delivery': ['search', 'stats', 'get'],
    # 资源模块 - 采购
    'supplier': ['add', 'search', 'stats', 'export', 'get', 'edit', 'del', 'audit', 'print'],
    'buyer_order': ['search', 'stats', 'get'],
    'purchase': ['search', 'stats', 'get'],
}


def setup(identity):
    # 赋予整体角色权限
    identity.provides.add(RoleNeed('财务'))

    for section, actions in role_accountant_section_action.items():
        # 配置模块身份（用于模块显示）
        setup_section(identity, section)
        # 配置模块通用操作身份（用户动作权限）
        setup_section_action(identity, section, *actions)
