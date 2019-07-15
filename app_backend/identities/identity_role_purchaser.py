#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: identity_role_purchaser.py
@time: 2019-06-27 00:55
"""

from __future__ import unicode_literals

import six
from flask_login import current_user
from flask_principal import RoleNeed

from app_backend.api.buyer_order import get_buyer_order_rows
from app_backend.api.enquiry import get_enquiry_rows
from app_backend.api.purchase import get_purchase_rows
from app_backend.api.supplier import get_supplier_rows
from app_backend.identities import setup_section_action, setup_section, setup_section_item_action

# 模块通用操作
role_purchaser_section_action = {
    # 基础模块
    'production': ['add', 'search', 'stats'],
    'inventory': ['add', 'search', 'stats'],
    'warehouse': ['add', 'search', 'stats'],
    'rack': ['add', 'search', 'stats'],
    # 资源模块
    'supplier': ['add', 'search', 'stats'],
    'enquiry': ['add', 'search', 'stats'],
    'buyer_order': ['add', 'search', 'stats'],
    'purchase': ['add', 'search', 'stats'],
}

# 模块明细操作
role_purchaser_section_item_action = {
    'supplier': ['get', 'edit', 'del', 'audit', 'print'],
    'enquiry': ['get', 'edit', 'del', 'audit', 'print'],
    'buyer_order': ['get', 'edit', 'del', 'audit', 'print'],
    'purchase': ['get', 'edit', 'del', 'audit', 'print'],
}


def setup(identity):
    # 配置角色身份
    identity.provides.add(RoleNeed('采购'))

    for section, actions in role_purchaser_section_action.items():
        # 配置模块身份（用于模块显示）
        setup_section(identity, section)
        # 配置模块通用操作身份（用户动作权限）
        setup_section_action(identity, section, *actions)

    for section, actions in role_purchaser_section_item_action.items():
        # 渠道
        if section == 'supplier':
            supplier_rows_condition = {
                'owner_uid': current_user.id
            }
            supplier_rows = get_supplier_rows(**supplier_rows_condition)
            for supplier_row in supplier_rows:
                # 配置模块明细操作身份（用于资源权限）
                setup_section_item_action(identity, section, six.text_type(supplier_row.id), *actions)
        # 询价
        if section == 'enquiry':
            enquiry_rows_condition = {
                'uid': current_user.id
            }
            enquiry_rows = get_enquiry_rows(**enquiry_rows_condition)
            for enquiry_row in enquiry_rows:
                # 配置模块明细操作身份（用于资源权限）
                setup_section_item_action(identity, section, six.text_type(enquiry_row.id), *actions)
        # 采购订单
        if section == 'buyer_order':
            buyer_order_rows_condition = {
                'uid': current_user.id
            }
            buyer_order_rows = get_buyer_order_rows(**buyer_order_rows_condition)
            for buyer_order_row in buyer_order_rows:
                # 配置模块明细操作身份（用于资源权限）
                setup_section_item_action(identity, section, six.text_type(buyer_order_row.id), *actions)
        # 采购进货
        if section == 'purchase':
            purchase_rows_condition = {
                'uid': current_user.id
            }
            purchase_rows = get_purchase_rows(**purchase_rows_condition)
            for purchase_row in purchase_rows:
                # 配置模块明细操作身份（用于资源权限）
                setup_section_item_action(identity, section, six.text_type(purchase_row.id), *actions)
