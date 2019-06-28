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

from app_backend.permissions import SectionActionNeed


def setup(identity):
    # 赋予整体角色权限
    identity.provides.add(RoleNeed('系统'))

    # 版块基本操作权限（系统）
    # 用户-----------------------------------------------------------------------
    # 用户创建
    identity.provides.add(SectionActionNeed('user', 'add'))
    # 用户统计
    identity.provides.add(SectionActionNeed('user', 'stats'))
    # 产品-----------------------------------------------------------------------
    # 产品创建
    identity.provides.add(SectionActionNeed('production', 'add'))
    # 产品统计
    identity.provides.add(SectionActionNeed('production', 'stats'))

    # 版块明细操作权限（系统）
    # 系统角色拥有全部版块权限，不区分明细权限
