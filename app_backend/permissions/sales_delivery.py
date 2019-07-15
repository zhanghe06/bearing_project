#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: sales_delivery.py
@time: 2019-05-12 10:00
"""

from __future__ import unicode_literals

from functools import partial

import six

from app_backend.permissions import SectionNeed, SectionActionNeed, BasePermission, SectionActionItemNeed

# -------------------------------------------------------------
# 销售出货板块整体权限
DeliverySectionNeed = partial(SectionNeed, 'delivery')
permission_delivery_section = BasePermission(DeliverySectionNeed())

# -------------------------------------------------------------
# 销售出货板块操作权限（创建、查询、导出、统计）
DeliverySectionActionNeed = partial(SectionActionNeed, 'delivery')
DeliverySectionActionNeed.__doc__ = """A need with the section preset to `"delivery"`."""

permission_delivery_section_add = BasePermission(DeliverySectionActionNeed('add'))
permission_delivery_section_search = BasePermission(DeliverySectionActionNeed('search'))
permission_delivery_section_export = BasePermission(DeliverySectionActionNeed('export'))
permission_delivery_section_stats = BasePermission(DeliverySectionActionNeed('stats'))

# -------------------------------------------------------------
# 销售出货明细操作权限（读取、更新、删除、打印、审核）
DeliveryItemNeed = partial(SectionActionItemNeed, 'delivery')
DeliveryItemNeed.__doc__ = """A need with the section preset to `"delivery"`."""

DeliveryItemGetNeed = partial(DeliveryItemNeed, 'get')
DeliveryItemEditNeed = partial(DeliveryItemNeed, 'edit')
DeliveryItemDelNeed = partial(DeliveryItemNeed, 'del')
DeliveryItemPrintNeed = partial(DeliveryItemNeed, 'print')
DeliveryItemAuditNeed = partial(DeliveryItemNeed, 'audit')


class DeliveryItemGetPermission(BasePermission):
    def __init__(self, sales_delivery_id):
        need = DeliveryItemGetNeed(six.text_type(sales_delivery_id))
        super(DeliveryItemGetPermission, self).__init__(need)


class DeliveryItemEditPermission(BasePermission):
    def __init__(self, sales_delivery_id):
        need = DeliveryItemEditNeed(six.text_type(sales_delivery_id))
        super(DeliveryItemEditPermission, self).__init__(need)


class DeliveryItemDelPermission(BasePermission):
    def __init__(self, sales_delivery_id):
        need = DeliveryItemDelNeed(six.text_type(sales_delivery_id))
        super(DeliveryItemDelPermission, self).__init__(need)


class DeliveryItemPrintPermission(BasePermission):
    def __init__(self, sales_delivery_id):
        need = DeliveryItemPrintNeed(six.text_type(sales_delivery_id))
        super(DeliveryItemPrintPermission, self).__init__(need)


class DeliveryItemAuditPermission(BasePermission):
    def __init__(self, sales_delivery_id):
        need = DeliveryItemAuditNeed(six.text_type(sales_delivery_id))
        super(DeliveryItemAuditPermission, self).__init__(need)
