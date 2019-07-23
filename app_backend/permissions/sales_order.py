#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: sales_order.py
@time: 2019-05-12 10:00
"""

from __future__ import unicode_literals

from functools import partial

from app_backend.permissions import SectionNeed, SectionActionNeed, BasePermission

# -------------------------------------------------------------
# 销售订单板块整体权限
SalesOrderSectionNeed = partial(SectionNeed, 'sales_order')
permission_sales_order_section = BasePermission(SalesOrderSectionNeed())

# -------------------------------------------------------------
# 销售订单板块操作权限（创建、查询、统计、导出、详情、编辑、删除、审核、打印）
SalesOrderSectionActionNeed = partial(SectionActionNeed, 'sales_order')
SalesOrderSectionActionNeed.__doc__ = """A need with the section preset to `"sales_order"`."""

permission_sales_order_section_add = BasePermission(SalesOrderSectionActionNeed('add'))
permission_sales_order_section_search = BasePermission(SalesOrderSectionActionNeed('search'))
permission_sales_order_section_stats = BasePermission(SalesOrderSectionActionNeed('stats'))
permission_sales_order_section_export = BasePermission(SalesOrderSectionActionNeed('export'))

permission_sales_order_section_get = BasePermission(SalesOrderSectionActionNeed('get'))
permission_sales_order_section_edit = BasePermission(SalesOrderSectionActionNeed('edit'))
permission_sales_order_section_del = BasePermission(SalesOrderSectionActionNeed('del'))
permission_sales_order_section_audit = BasePermission(SalesOrderSectionActionNeed('audit'))
permission_sales_order_section_print = BasePermission(SalesOrderSectionActionNeed('print'))
