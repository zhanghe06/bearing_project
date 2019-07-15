#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: identity_role_manager.py
@time: 2019-06-27 00:53
"""


from __future__ import unicode_literals

import six
from flask_login import current_user
from flask_principal import RoleNeed

from app_backend.api.customer import get_customer_rows
from app_backend.api.delivery import get_delivery_rows
from app_backend.api.quotation import get_quotation_rows
from app_backend.api.sales_order import get_sales_order_rows
from app_backend.api.user import get_user_rows
from app_backend.identities import setup_section_action, setup_section, setup_section_item_action
from app_common.maps.type_role import TYPE_ROLE_SALES
from app_common.maps.status_delete import STATUS_DEL_NO


# 模块通用操作
role_manager_section_action = {
    # 基础模块
    'production': ['add', 'search', 'stats', 'export'],
    'inventory': ['add', 'search', 'stats', 'export'],
    'warehouse': ['add', 'search', 'stats', 'export'],
    'rack': ['add', 'search', 'stats', 'export'],
    # 资源模块
    'customer': ['add', 'search', 'stats', 'export'],
    'quotation': ['add', 'search', 'stats', 'export'],
    'sales_order': ['add', 'search', 'stats', 'export'],
    'delivery': ['add', 'search', 'stats', 'export'],
}

# 模块明细操作
role_manager_section_item_action = {
    'customer': ['get', 'edit', 'del', 'audit', 'print'],
    'quotation': ['get', 'edit', 'del', 'audit', 'print'],
    'sales_order': ['get', 'edit', 'del', 'audit', 'print'],
    'delivery': ['get', 'edit', 'del', 'audit', 'print'],
}

# 模块明细操作 - 下属扩展权限
role_manager_section_item_action_ext = {
    'customer': ['get', 'audit', 'print'],
    'quotation': ['get', 'audit', 'print'],
    'sales_order': ['get', 'audit', 'print'],
    'delivery': ['get', 'audit', 'print'],
}


def _setup_identity_customer(identity, uid, *actions):
    section = 'customer'
    customer_rows_condition = {
        'owner_uid': uid
    }
    customer_rows = get_customer_rows(**customer_rows_condition)
    for customer_row in customer_rows:
        # 配置模块明细操作身份（用于资源权限）
        setup_section_item_action(identity, section, six.text_type(customer_row.id), *actions)


def _setup_identity_quotation(identity, uid, *actions):
    section = 'quotation'
    quotation_rows_condition = {
        'uid': uid
    }
    quotation_rows = get_quotation_rows(**quotation_rows_condition)
    for quotation_row in quotation_rows:
        # 配置模块明细操作身份（用于资源权限）
        setup_section_item_action(identity, section, six.text_type(quotation_row.id), *actions)


def _setup_identity_sales_order(identity, uid, *actions):
    section = 'sales_order'
    sales_order_rows_condition = {
        'uid': uid
    }
    sales_order_rows = get_sales_order_rows(**sales_order_rows_condition)
    for sales_order_row in sales_order_rows:
        # 配置模块明细操作身份（用于资源权限）
        setup_section_item_action(identity, section, six.text_type(sales_order_row.id), *actions)


def _setup_identity_delivery(identity, uid, *actions):
    section = 'delivery'
    delivery_rows_condition = {
        'uid': uid
    }
    delivery_rows = get_delivery_rows(**delivery_rows_condition)
    for delivery_row in delivery_rows:
        # 配置模块明细操作身份（用于资源权限）
        setup_section_item_action(identity, section, six.text_type(delivery_row.id), *actions)


def setup(identity):
    # 配置角色身份
    identity.provides.add(RoleNeed('经理'))

    for section, actions in role_manager_section_action.items():
        # 配置模块身份（用于模块显示）
        setup_section(identity, section)
        # 配置模块通用操作身份（用户动作权限）
        setup_section_action(identity, section, *actions)

    # 自有身份
    for section, actions in role_manager_section_item_action.items():
        uid = current_user.id
        # 客户
        if section == 'customer':
            _setup_identity_customer(identity, uid, *actions)
        # 报价
        if section == 'quotation':
            _setup_identity_quotation(identity, uid, *actions)
        # 销售订单
        if section == 'sales_order':
            _setup_identity_sales_order(identity, uid, *actions)
        # 销售出货
        if section == 'delivery':
            _setup_identity_delivery(identity, uid, *actions)

    # 扩展身份
    for section, actions in role_manager_section_item_action_ext.items():
        sales_rows_condition = {
            'parent_id': current_user.id,
            'role_id': TYPE_ROLE_SALES,
            'status_delete': STATUS_DEL_NO,
        }
        sales_rows = get_user_rows(**sales_rows_condition)
        for sales_item in sales_rows:
            uid = sales_item.id
            # 客户
            if section == 'customer':
                _setup_identity_customer(identity, uid, *actions)
            # 报价
            if section == 'quotation':
                _setup_identity_quotation(identity, uid, *actions)
            # 销售订单
            if section == 'sales_order':
                _setup_identity_sales_order(identity, uid, *actions)
            # 销售出货
            if section == 'delivery':
                _setup_identity_delivery(identity, uid, *actions)
