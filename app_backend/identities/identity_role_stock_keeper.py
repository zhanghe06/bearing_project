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

from app_backend.identities import setup_section, setup_section_action

# 模块通用操作
role_stock_keeper_section_action = {
    # 基础模块
    'production': ['add', 'search', 'stats'],
    'inventory': ['add', 'search', 'stats'],
    'warehouse': ['add', 'search', 'stats'],
    'rack': ['add', 'search', 'stats'],
}


def setup(identity):
    # 配置角色身份
    identity.provides.add(RoleNeed('库管'))

    for section, actions in role_stock_keeper_section_action.items():
        # 配置模块身份（用于模块显示）
        setup_section(identity, section)
        # 配置模块通用操作身份（用户动作权限）
        setup_section_action(identity, section, *actions)