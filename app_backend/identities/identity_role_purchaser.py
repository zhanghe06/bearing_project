#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: identity_role_purchaser.py
@time: 2019-06-27 00:55
"""

from __future__ import unicode_literals

from flask_principal import RoleNeed

from app_backend.identities import setup_section_action, setup_section

# 模块操作
role_purchaser_section_action = {
    # 基础模块
    'production': ['add', 'search', 'get', 'edit', 'del', 'audit', 'print'],
    'inventory': ['add', 'search', 'get', 'edit', 'del', 'audit', 'print'],
    'warehouse': ['add', 'search', 'get', 'edit', 'del', 'audit', 'print'],
    'rack': ['add', 'search', 'get', 'edit', 'del', 'audit', 'print'],
    'user': ['search', 'get', 'edit'],
    'futures': ['add', 'search', 'stats', 'export', 'get', 'edit', 'del', 'audit', 'print'],
    # 资源模块
    'supplier': ['add', 'search', 'stats', 'get', 'edit', 'del', 'audit', 'print'],
    'enquiry': ['add', 'search', 'stats', 'get', 'edit', 'del', 'audit', 'print'],
    'buyer_order': ['add', 'search', 'stats', 'get', 'edit', 'del', 'audit', 'print'],
    'purchase': ['add', 'search', 'stats', 'get', 'edit', 'del', 'audit', 'print'],
}


def setup(identity):
    # 配置角色身份
    identity.provides.add(RoleNeed('采购'))

    for section, actions in role_purchaser_section_action.items():
        # 配置模块身份（用于模块显示）
        setup_section(identity, section)
        # 配置模块通用操作身份（用户动作权限）
        setup_section_action(identity, section, *actions)
