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
from app_backend.api.quotation import get_quotation_rows
from app_backend.api.user import get_user_rows
from app_backend.permissions import SectionActionNeed, SectionActionItemNeed


def setup(identity):
    # 赋予整体角色权限
    identity.provides.add(RoleNeed('经理'))
    # 版块基本操作权限（经理）
    # （创建、查询、统计、导出）
    # 客户-----------------------------------------------------------------------
    # 客户创建
    identity.provides.add(SectionActionNeed('customer', 'add'))
    # 客户查询
    identity.provides.add(SectionActionNeed('customer', 'search'))
    # 客户统计
    identity.provides.add(SectionActionNeed('customer', 'stats'))
    # 客户导出
    identity.provides.add(SectionActionNeed('customer', 'export'))
    # 报价-----------------------------------------------------------------------
    # 报价创建
    identity.provides.add(SectionActionNeed('quotation', 'add'))
    # 报价查询
    identity.provides.add(SectionActionNeed('quotation', 'search'))
    # 报价统计
    identity.provides.add(SectionActionNeed('quotation', 'stats'))
    # 报价导出
    identity.provides.add(SectionActionNeed('quotation', 'export'))

    # 版块明细操作权限（经理）
    # （读取、编辑、删除、打印、审核）
    # 客户-----------------------------------------------------------------------
    customer_rows_condition = {
        'owner_uid': current_user.id
    }
    customer_rows = get_customer_rows(**customer_rows_condition)
    for customer_row in customer_rows:
        # 客户读取权限
        identity.provides.add(SectionActionItemNeed('customer', 'get', six.text_type(customer_row.id)))
        # 客户编辑权限
        identity.provides.add(SectionActionItemNeed('customer', 'edit', six.text_type(customer_row.id)))
        # 客户删除权限
        identity.provides.add(SectionActionItemNeed('customer', 'del', six.text_type(customer_row.id)))
        # 客户打印权限
        identity.provides.add(SectionActionItemNeed('customer', 'print', six.text_type(customer_row.id)))
    # 报价-----------------------------------------------------------------------
    quotation_rows_condition = {
        'uid': current_user.id
    }
    quotation_rows = get_quotation_rows(**quotation_rows_condition)
    for quotation_row in quotation_rows:
        # 报价读取权限
        identity.provides.add(SectionActionItemNeed('quotation', 'get', six.text_type(quotation_row.id)))
        # 报价编辑权限
        identity.provides.add(SectionActionItemNeed('quotation', 'edit', six.text_type(quotation_row.id)))
        # 报价删除权限
        identity.provides.add(SectionActionItemNeed('quotation', 'del', six.text_type(quotation_row.id)))
        # 报价打印权限
        identity.provides.add(SectionActionItemNeed('quotation', 'print', six.text_type(quotation_row.id)))
        # 报价审核权限
        identity.provides.add(SectionActionItemNeed('quotation', 'audit', six.text_type(quotation_row.id)))

    # 版块明细操作权限 - 所属销售（经理）
    sales_rows_condition = {
        'parent_id': current_user.id
    }
    sales_rows = get_user_rows(**sales_rows_condition)
    for sales_item in sales_rows:
        # 客户-----------------------------------------------------------------------
        customer_rows_condition = {
            'owner_uid': sales_item.id
        }
        customer_rows = get_customer_rows(**customer_rows_condition)
        for customer_row in customer_rows:
            # 客户读取权限
            identity.provides.add(SectionActionItemNeed('customer', 'get', six.text_type(customer_row.id)))
            # 客户编辑权限
            identity.provides.add(SectionActionItemNeed('customer', 'edit', six.text_type(customer_row.id)))
            # 客户删除权限
            identity.provides.add(SectionActionItemNeed('customer', 'del', six.text_type(customer_row.id)))
            # 客户打印权限
            identity.provides.add(SectionActionItemNeed('customer', 'print', six.text_type(customer_row.id)))
        # 报价-----------------------------------------------------------------------
        quotation_rows_condition = {
            'uid': sales_item.id
        }
        quotation_rows = get_quotation_rows(**quotation_rows_condition)
        for quotation_row in quotation_rows:
            # 报价读取权限
            identity.provides.add(SectionActionItemNeed('quotation', 'get', six.text_type(quotation_row.id)))
            # 报价编辑权限
            identity.provides.add(SectionActionItemNeed('quotation', 'edit', six.text_type(quotation_row.id)))
            # 报价删除权限
            identity.provides.add(SectionActionItemNeed('quotation', 'del', six.text_type(quotation_row.id)))
            # 报价打印权限
            identity.provides.add(SectionActionItemNeed('quotation', 'print', six.text_type(quotation_row.id)))
            # 报价审核权限
            identity.provides.add(SectionActionItemNeed('quotation', 'audit', six.text_type(quotation_row.id)))
