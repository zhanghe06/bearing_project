#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: identity_role_administrator.py
@time: 2019-06-27 00:51
"""

from __future__ import unicode_literals

from flask_principal import RoleNeed

from app_backend.identities import setup_section, setup_section_action

# 模块通用操作
role_administrator_section_action = {
    # 基础模块
    'production': ['add', 'search', 'stats', 'export'],
    'inventory': ['add', 'search', 'stats', 'export'],
    'warehouse': ['add', 'search', 'stats', 'export'],
    'rack': ['add', 'search', 'stats', 'export'],
    'user': ['add', 'search', 'stats', 'export'],
    # 资源模块 - 销售
    'customer': ['add', 'search', 'stats', 'export'],
    'quotation': ['add', 'search', 'stats', 'export'],
    'sales_order': ['add', 'search', 'stats', 'export'],
    'delivery': ['add', 'search', 'stats', 'export'],
    # 资源模块 - 采购
    'supplier': ['add', 'search', 'stats', 'export'],
    'enquiry': ['add', 'search', 'stats', 'export'],
    'buyer_order': ['add', 'search', 'stats', 'export'],
    'purchase': ['add', 'search', 'stats', 'export'],
}


def setup(identity):
    # 赋予整体角色权限
    identity.provides.add(RoleNeed('系统'))

    for section, actions in role_administrator_section_action.items():
        # 配置模块身份（用于模块显示）
        setup_section(identity, section)
        # 配置模块通用操作身份（用户动作权限）
        setup_section_action(identity, section, *actions)