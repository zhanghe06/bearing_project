#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: buyer_order.py
@time: 2019-05-12 10:00
"""

from __future__ import unicode_literals

from functools import partial

from app_backend.permissions import SectionNeed, SectionActionNeed, BasePermission

# -------------------------------------------------------------
# 采购订单板块整体权限
BuyerOrderSectionNeed = partial(SectionNeed, 'buyer_order')
permission_buyer_order_section = BasePermission(BuyerOrderSectionNeed())

# -------------------------------------------------------------
# 采购订单板块操作权限（创建、查询、统计、导出、详情、编辑、删除、审核、打印）
BuyerOrderSectionActionNeed = partial(SectionActionNeed, 'buyer_order')
BuyerOrderSectionActionNeed.__doc__ = """A need with the section preset to `"buyer_order"`."""

permission_buyer_order_section_add = BasePermission(BuyerOrderSectionActionNeed('add'))
permission_buyer_order_section_search = BasePermission(BuyerOrderSectionActionNeed('search'))
permission_buyer_order_section_stats = BasePermission(BuyerOrderSectionActionNeed('stats'))
permission_buyer_order_section_export = BasePermission(BuyerOrderSectionActionNeed('export'))

permission_buyer_order_section_get = BasePermission(BuyerOrderSectionActionNeed('get'))
permission_buyer_order_section_edit = BasePermission(BuyerOrderSectionActionNeed('edit'))
permission_buyer_order_section_del = BasePermission(BuyerOrderSectionActionNeed('del'))
permission_buyer_order_section_audit = BasePermission(BuyerOrderSectionActionNeed('audit'))
permission_buyer_order_section_print = BasePermission(BuyerOrderSectionActionNeed('print'))
