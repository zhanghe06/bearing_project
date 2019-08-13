#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: identity_role_manager.py
@time: 2019-06-27 00:53
"""

from __future__ import unicode_literals

from flask_principal import RoleNeed

from app_backend.identities import setup_section_action, setup_section

# 模块操作
role_manager_section_action = {
    # 基础模块
    'production': ['add', 'search', 'stats', 'export', 'get', 'edit', 'del', 'audit', 'print'],
    'inventory': ['add', 'search', 'stats', 'export', 'get', 'edit', 'del', 'audit', 'print'],
    'warehouse': ['add', 'search', 'stats', 'export', 'get', 'edit', 'del', 'audit', 'print'],
    'rack': ['add', 'search', 'stats', 'export', 'get', 'edit', 'del', 'audit', 'print'],
    'user': ['add', 'search', 'stats', 'export', 'get', 'edit', 'del', 'audit', 'print'],
    'futures': ['add', 'search', 'stats', 'export', 'get', 'edit', 'del', 'audit', 'print'],
    # 资源模块 - 销售
    'customer': ['add', 'search', 'stats', 'export', 'get', 'edit', 'del', 'audit', 'print'],
    'quotation': ['add', 'search', 'stats', 'export', 'get', 'edit', 'del', 'audit', 'print'],
    'sales_order': ['add', 'search', 'stats', 'export', 'get', 'edit', 'del', 'audit', 'print'],
    'delivery': ['add', 'search', 'stats', 'export', 'get', 'edit', 'del', 'audit', 'print'],
    # 资源模块 - 采购
    'supplier': ['add', 'search', 'stats', 'export', 'get', 'edit', 'del', 'audit', 'print'],
    'enquiry': ['add', 'search', 'stats', 'export', 'get', 'edit', 'del', 'audit', 'print'],
    'buyer_order': ['add', 'search', 'stats', 'export', 'get', 'edit', 'del', 'audit', 'print'],
    'purchase': ['add', 'search', 'stats', 'export', 'get', 'edit', 'del', 'audit', 'print'],
}


def setup(identity):
    # 配置角色身份
    identity.provides.add(RoleNeed('经理'))

    for section, actions in role_manager_section_action.items():
        # 配置模块身份（用于模块显示）
        setup_section(identity, section)
        # 配置模块通用操作身份（用户动作权限）
        setup_section_action(identity, section, *actions)
