#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: identity_role_sales.py
@time: 2019-06-27 00:52
"""

from __future__ import unicode_literals

from flask_principal import RoleNeed

from app_backend.identities import setup_section_action, setup_section

# 模块通用操作
role_sales_section_action = {
    # 基础模块
    'production': ['add', 'search', 'get', 'edit', 'del', 'audit', 'print'],
    'inventory': ['add', 'search', 'get', 'edit', 'del', 'audit', 'print'],
    'warehouse': ['add', 'search', 'get', 'edit', 'del', 'audit', 'print'],
    'rack': ['add', 'search', 'get', 'edit', 'del', 'audit', 'print'],
    'user': ['search', 'get', 'edit'],
    'futures': ['search', 'get'],
    # 资源模块
    'customer': ['add', 'search', 'stats', 'get', 'edit', 'del', 'audit', 'print'],
    'quotation': ['add', 'search', 'stats', 'get', 'edit', 'del', 'audit', 'print'],
    'sales_order': ['add', 'search', 'stats', 'get', 'edit', 'del', 'audit', 'print'],
    'delivery': ['add', 'search', 'stats', 'get', 'edit', 'del', 'audit', 'print'],
}


def setup(identity):
    # 配置角色身份
    identity.provides.add(RoleNeed('销售'))

    for section, actions in role_sales_section_action.items():
        # 配置模块身份（用于模块显示）
        setup_section(identity, section)
        # 配置模块通用操作身份（用户动作权限）
        setup_section_action(identity, section, *actions)
