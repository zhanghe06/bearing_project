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

import six

from app_backend.permissions import SectionNeed, SectionActionNeed, BasePermission, SectionActionItemNeed

# -------------------------------------------------------------
# 销售订单板块整体权限
SalesOrderSectionNeed = partial(SectionNeed, 'sales_order')
permission_sales_order_section = BasePermission(SalesOrderSectionNeed())

# -------------------------------------------------------------
# 销售订单板块操作权限（创建、查询、导出、统计）
SalesOrderSectionActionNeed = partial(SectionActionNeed, 'sales_order')
SalesOrderSectionActionNeed.__doc__ = """A need with the section preset to `"sales_order"`."""

permission_sales_order_section_add = BasePermission(SalesOrderSectionActionNeed('add'))
permission_sales_order_section_search = BasePermission(SalesOrderSectionActionNeed('search'))
permission_sales_order_section_export = BasePermission(SalesOrderSectionActionNeed('export'))
permission_sales_order_section_stats = BasePermission(SalesOrderSectionActionNeed('stats'))

# -------------------------------------------------------------
# 销售订单明细操作权限（读取、更新、删除、打印、审核）
SalesOrderItemNeed = partial(SectionActionItemNeed, 'sales_order')
SalesOrderItemNeed.__doc__ = """A need with the section preset to `"sales_order"`."""

SalesOrderItemGetNeed = partial(SalesOrderItemNeed, 'get')
SalesOrderItemEditNeed = partial(SalesOrderItemNeed, 'edit')
SalesOrderItemDelNeed = partial(SalesOrderItemNeed, 'del')
SalesOrderItemPrintNeed = partial(SalesOrderItemNeed, 'print')
SalesOrderItemAuditNeed = partial(SalesOrderItemNeed, 'audit')


class SalesOrderItemGetPermission(BasePermission):
    def __init__(self, order_id):
        need = SalesOrderItemGetNeed(six.text_type(order_id))
        super(SalesOrderItemGetPermission, self).__init__(need)


class SalesOrderItemEditPermission(BasePermission):
    def __init__(self, order_id):
        need = SalesOrderItemEditNeed(six.text_type(order_id))
        super(SalesOrderItemEditPermission, self).__init__(need)


class SalesOrderItemDelPermission(BasePermission):
    def __init__(self, order_id):
        need = SalesOrderItemDelNeed(six.text_type(order_id))
        super(SalesOrderItemDelPermission, self).__init__(need)


class SalesOrderItemPrintPermission(BasePermission):
    def __init__(self, order_id):
        need = SalesOrderItemPrintNeed(six.text_type(order_id))
        super(SalesOrderItemPrintPermission, self).__init__(need)


class SalesOrderItemAuditPermission(BasePermission):
    def __init__(self, order_id):
        need = SalesOrderItemAuditNeed(six.text_type(order_id))
        super(SalesOrderItemAuditPermission, self).__init__(need)
