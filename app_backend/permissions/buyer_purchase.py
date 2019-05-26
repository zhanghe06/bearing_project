#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: buyer_purchase.py
@time: 2019-05-12 10:01
"""

from __future__ import unicode_literals

from functools import partial

import six

from app_backend.permissions import SectionActionNeed, BasePermission, SectionActionItemNeed

# -------------------------------------------------------------
# 采购进货板块操作权限（创建、查询、导出、统计）
PurchaseSectionNeed = partial(SectionActionNeed, 'purchase')
PurchaseSectionNeed.__doc__ = """A need with the section preset to `"purchase"`."""

permission_purchase_section_add = BasePermission(PurchaseSectionNeed('add'))
permission_purchase_section_search = BasePermission(PurchaseSectionNeed('search'))
permission_purchase_section_export = BasePermission(PurchaseSectionNeed('export'))
permission_purchase_section_stats = BasePermission(PurchaseSectionNeed('stats'))

# -------------------------------------------------------------
# 采购进货明细操作权限（读取、更新、删除、打印、审核）
PurchaseItemNeed = partial(SectionActionItemNeed, 'purchase')
PurchaseItemNeed.__doc__ = """A need with the section preset to `"purchase"`."""

PurchaseItemGetNeed = partial(PurchaseItemNeed, 'get')
PurchaseItemEditNeed = partial(PurchaseItemNeed, 'edit')
PurchaseItemDelNeed = partial(PurchaseItemNeed, 'del')
PurchaseItemPrintNeed = partial(PurchaseItemNeed, 'print')
PurchaseItemAuditNeed = partial(PurchaseItemNeed, 'audit')


class PurchaseItemGetPermission(BasePermission):
    def __init__(self, buyer_purchase_id):
        need = PurchaseItemGetNeed(six.text_type(buyer_purchase_id))
        super(PurchaseItemGetPermission, self).__init__(need)


class PurchaseItemEditPermission(BasePermission):
    def __init__(self, buyer_purchase_id):
        need = PurchaseItemEditNeed(six.text_type(buyer_purchase_id))
        super(PurchaseItemEditPermission, self).__init__(need)


class PurchaseItemDelPermission(BasePermission):
    def __init__(self, buyer_purchase_id):
        need = PurchaseItemDelNeed(six.text_type(buyer_purchase_id))
        super(PurchaseItemDelPermission, self).__init__(need)


class PurchaseItemPrintPermission(BasePermission):
    def __init__(self, buyer_purchase_id):
        need = PurchaseItemPrintNeed(six.text_type(buyer_purchase_id))
        super(PurchaseItemPrintPermission, self).__init__(need)


class PurchaseItemAuditPermission(BasePermission):
    def __init__(self, buyer_purchase_id):
        need = PurchaseItemAuditNeed(six.text_type(buyer_purchase_id))
        super(PurchaseItemAuditPermission, self).__init__(need)
