#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: supplier.py
@time: 2019-05-12 09:57
"""

from __future__ import unicode_literals

from functools import partial

import six

from app_backend.permissions import SectionActionNeed, BasePermission, SectionActionItemNeed

# -------------------------------------------------------------
# 渠道板块操作权限（创建、查询、导出、统计）
SupplierSectionNeed = partial(SectionActionNeed, 'supplier')
SupplierSectionNeed.__doc__ = """A need with the section preset to `"supplier"`."""

permission_supplier_section_add = BasePermission(SupplierSectionNeed('add'))
permission_supplier_section_search = BasePermission(SupplierSectionNeed('search'))
permission_supplier_section_export = BasePermission(SupplierSectionNeed('export'))
permission_supplier_section_stats = BasePermission(SupplierSectionNeed('stats'))


# -------------------------------------------------------------
# 渠道明细操作权限(读取、更新、删除、打印)
SupplierItemNeed = partial(SectionActionItemNeed, 'supplier')
SupplierItemNeed.__doc__ = """A need with the section preset to `"supplier"`."""

SupplierItemGetNeed = partial(SupplierItemNeed, 'get')
SupplierItemEditNeed = partial(SupplierItemNeed, 'edit')
SupplierItemDelNeed = partial(SupplierItemNeed, 'del')
SupplierItemPrintNeed = partial(SupplierItemNeed, 'print')


class SupplierItemGetPermission(BasePermission):
    def __init__(self, supplier_id):
        need = SupplierItemGetNeed(six.text_type(supplier_id))
        super(SupplierItemGetPermission, self).__init__(need)


class SupplierItemEditPermission(BasePermission):
    def __init__(self, supplier_id):
        need = SupplierItemEditNeed(six.text_type(supplier_id))
        super(SupplierItemEditPermission, self).__init__(need)


class SupplierItemDelPermission(BasePermission):
    def __init__(self, supplier_id):
        need = SupplierItemDelNeed(six.text_type(supplier_id))
        super(SupplierItemDelPermission, self).__init__(need)


class SupplierItemPrintPermission(BasePermission):
    def __init__(self, supplier_id):
        need = SupplierItemPrintNeed(six.text_type(supplier_id))
        super(SupplierItemPrintPermission, self).__init__(need)
