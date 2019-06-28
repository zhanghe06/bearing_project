#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: identity_global.py
@time: 2019-06-27 01:29
"""

from __future__ import unicode_literals

from app_backend.permissions import SectionActionNeed


def setup(identity):
    # 公共权限（查询）
    identity.provides.add(SectionActionNeed('user', 'search'))  # 用户查询
    identity.provides.add(SectionActionNeed('production', 'search'))  # 产品查询
    identity.provides.add(SectionActionNeed('inventory', 'search'))  # 库存查询
    identity.provides.add(SectionActionNeed('warehouse', 'search'))  # 仓库查询
    identity.provides.add(SectionActionNeed('customer', 'search'))  # 客户查询
    identity.provides.add(SectionActionNeed('supplier', 'search'))  # 渠道查询
    identity.provides.add(SectionActionNeed('delivery', 'search'))  # 销货查询
    identity.provides.add(SectionActionNeed('purchase', 'search'))  # 进货查询
    identity.provides.add(SectionActionNeed('sales_order', 'search'))  # 销售查询
    identity.provides.add(SectionActionNeed('buyer_order', 'search'))  # 采购查询

    # 公共权限（创建）

    # 公共权限（编辑）

    # 公共权限（删除）

