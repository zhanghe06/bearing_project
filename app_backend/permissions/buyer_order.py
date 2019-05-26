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

import six

from app_backend.permissions import SectionActionNeed, BasePermission, SectionActionItemNeed

# -------------------------------------------------------------
# 采购订单板块操作权限（创建、查询、导出、统计）
BuyerOrderSectionNeed = partial(SectionActionNeed, 'buyer_order')
BuyerOrderSectionNeed.__doc__ = """A need with the section preset to `"buyer_order"`."""

permission_buyer_order_section_add = BasePermission(BuyerOrderSectionNeed('add'))
permission_buyer_order_section_search = BasePermission(BuyerOrderSectionNeed('search'))
permission_buyer_order_section_export = BasePermission(BuyerOrderSectionNeed('export'))
permission_buyer_order_section_stats = BasePermission(BuyerOrderSectionNeed('stats'))

# -------------------------------------------------------------
# 采购订单明细操作权限（读取、更新、删除、打印、审核）
BuyerOrderItemNeed = partial(SectionActionItemNeed, 'buyer_order')
BuyerOrderItemNeed.__doc__ = """A need with the section preset to `"buyer_order"`."""

BuyerOrderItemGetNeed = partial(BuyerOrderItemNeed, 'get')
BuyerOrderItemEditNeed = partial(BuyerOrderItemNeed, 'edit')
BuyerOrderItemDelNeed = partial(BuyerOrderItemNeed, 'del')
BuyerOrderItemPrintNeed = partial(BuyerOrderItemNeed, 'print')
BuyerOrderItemAuditNeed = partial(BuyerOrderItemNeed, 'audit')


class BuyerOrderItemGetPermission(BasePermission):
    def __init__(self, order_id):
        need = BuyerOrderItemGetNeed(six.text_type(order_id))
        super(BuyerOrderItemGetPermission, self).__init__(need)


class BuyerOrderItemEditPermission(BasePermission):
    def __init__(self, order_id):
        need = BuyerOrderItemEditNeed(six.text_type(order_id))
        super(BuyerOrderItemEditPermission, self).__init__(need)


class BuyerOrderItemDelPermission(BasePermission):
    def __init__(self, order_id):
        need = BuyerOrderItemDelNeed(six.text_type(order_id))
        super(BuyerOrderItemDelPermission, self).__init__(need)


class BuyerOrderItemPrintPermission(BasePermission):
    def __init__(self, order_id):
        need = BuyerOrderItemPrintNeed(six.text_type(order_id))
        super(BuyerOrderItemPrintPermission, self).__init__(need)


class BuyerOrderItemAuditPermission(BasePermission):
    def __init__(self, order_id):
        need = BuyerOrderItemAuditNeed(six.text_type(order_id))
        super(BuyerOrderItemAuditPermission, self).__init__(need)
