#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: identity_role_sales.py
@time: 2019-06-27 00:52
"""

from __future__ import unicode_literals

import six
from flask_login import current_user
from flask_principal import RoleNeed

from app_backend.api.customer import get_customer_rows
from app_backend.api.delivery import get_delivery_rows
from app_backend.api.quotation import get_quotation_rows
from app_backend.api.sales_order import get_sales_order_rows
from app_backend.identities import setup_section_action, setup_section, setup_section_item_action


# 模块通用操作
role_sales_section_action = {
    # 基础模块
    'production': ['add', 'search', 'stats'],
    'inventory': ['add', 'search', 'stats'],
    'warehouse': ['add', 'search', 'stats'],
    'rack': ['add', 'search', 'stats'],
    # 资源模块
    'customer': ['add', 'search', 'stats'],
    'quotation': ['add', 'search', 'stats'],
    'sales_order': ['add', 'search', 'stats'],
    'delivery': ['add', 'search', 'stats'],
}

# 模块明细操作
role_sales_section_item_action = {
    'customer': ['get', 'edit', 'del', 'audit', 'print'],
    'quotation': ['get', 'edit', 'del', 'audit', 'print'],
    'sales_order': ['get', 'edit', 'del', 'audit', 'print'],
    'delivery': ['get', 'edit', 'del', 'audit', 'print'],
}


def setup(identity):
    # 配置角色身份
    identity.provides.add(RoleNeed('销售'))

    for section, actions in role_sales_section_action.items():
        # 配置模块身份（用于模块显示）
        setup_section(identity, section)
        # 配置模块通用操作身份（用户动作权限）
        setup_section_action(identity, section, *actions)

    for section, actions in role_sales_section_item_action.items():
        # 客户
        if section == 'customer':
            customer_rows_condition = {
                'owner_uid': current_user.id
            }
            customer_rows = get_customer_rows(**customer_rows_condition)
            for customer_row in customer_rows:
                # 配置模块明细操作身份（用于资源权限）
                setup_section_item_action(identity, section, six.text_type(customer_row.id), *actions)
        # 报价
        if section == 'quotation':
            quotation_rows_condition = {
                'uid': current_user.id
            }
            quotation_rows = get_quotation_rows(**quotation_rows_condition)
            for quotation_row in quotation_rows:
                # 配置模块明细操作身份（用于资源权限）
                setup_section_item_action(identity, section, six.text_type(quotation_row.id), *actions)
        # 销售订单
        if section == 'sales_order':
            sales_order_rows_condition = {
                'uid': current_user.id
            }
            sales_order_rows = get_sales_order_rows(**sales_order_rows_condition)
            for sales_order_row in sales_order_rows:
                # 配置模块明细操作身份（用于资源权限）
                setup_section_item_action(identity, section, six.text_type(sales_order_row.id), *actions)
        # 销售出货
        if section == 'delivery':
            delivery_rows_condition = {
                'uid': current_user.id
            }
            delivery_rows = get_delivery_rows(**delivery_rows_condition)
            for delivery_row in delivery_rows:
                # 配置模块明细操作身份（用于资源权限）
                setup_section_item_action(identity, section, six.text_type(delivery_row.id), *actions)
