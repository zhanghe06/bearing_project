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

from app_backend.api.enquiry import get_enquiry_rows
from app_backend.api.supplier import get_supplier_rows
from app_backend.permissions import SectionActionNeed, SectionActionItemNeed


def setup(identity):
    # 赋予整体角色权限
    identity.provides.add(RoleNeed('采购'))
    # 版块基本操作权限（销售）
    # （创建、查询、统计）
    # 渠道-----------------------------------------------------------------------
    # 渠道创建
    identity.provides.add(SectionActionNeed('supplier', 'add'))
    # 渠道查询
    identity.provides.add(SectionActionNeed('supplier', 'search'))
    # 渠道统计
    identity.provides.add(SectionActionNeed('supplier', 'stats'))
    # 询价-----------------------------------------------------------------------
    # 询价创建
    identity.provides.add(SectionActionNeed('enquiry', 'add'))
    # 询价查询
    identity.provides.add(SectionActionNeed('enquiry', 'search'))
    # 询价统计
    identity.provides.add(SectionActionNeed('enquiry', 'stats'))

    # 版块明细操作权限（销售）
    # （读取、编辑、删除、打印）
    # 渠道-----------------------------------------------------------------------
    supplier_rows_condition = {
        'owner_uid': current_user.id
    }
    supplier_rows = get_supplier_rows(**supplier_rows_condition)
    for supplier_row in supplier_rows:
        # 客户读取权限
        identity.provides.add(SectionActionItemNeed('supplier', 'get', six.text_type(supplier_row.id)))
        # 客户编辑权限
        identity.provides.add(SectionActionItemNeed('supplier', 'edit', six.text_type(supplier_row.id)))
        # 客户删除权限
        identity.provides.add(SectionActionItemNeed('supplier', 'del', six.text_type(supplier_row.id)))
        # 客户打印权限
        identity.provides.add(SectionActionItemNeed('supplier', 'print', six.text_type(supplier_row.id)))
    # 询价-----------------------------------------------------------------------
    enquiry_rows_condition = {
        'uid': current_user.id
    }
    enquiry_rows = get_enquiry_rows(**enquiry_rows_condition)
    for enquiry_row in enquiry_rows:
        # 报价读取权限
        identity.provides.add(SectionActionItemNeed('enquiry', 'get', six.text_type(enquiry_row.id)))
        # 报价编辑权限
        identity.provides.add(SectionActionItemNeed('enquiry', 'edit', six.text_type(enquiry_row.id)))
        # 报价删除权限
        identity.provides.add(SectionActionItemNeed('enquiry', 'del', six.text_type(enquiry_row.id)))
        # 报价打印权限
        identity.provides.add(SectionActionItemNeed('enquiry', 'print', six.text_type(enquiry_row.id)))
