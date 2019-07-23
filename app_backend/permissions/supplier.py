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

from app_backend.permissions import SectionNeed, SectionActionNeed, BasePermission

# -------------------------------------------------------------
# 渠道板块整体权限
SupplierSectionNeed = partial(SectionNeed, 'supplier')
permission_supplier_section = BasePermission(SupplierSectionNeed())

# -------------------------------------------------------------
# 渠道板块操作权限（创建、查询、统计、导出、详情、编辑、删除、审核、打印）
SupplierSectionActionNeed = partial(SectionActionNeed, 'supplier')
SupplierSectionActionNeed.__doc__ = """A need with the section preset to `"supplier"`."""

permission_supplier_section_add = BasePermission(SupplierSectionActionNeed('add'))
permission_supplier_section_search = BasePermission(SupplierSectionActionNeed('search'))
permission_supplier_section_stats = BasePermission(SupplierSectionActionNeed('stats'))
permission_supplier_section_export = BasePermission(SupplierSectionActionNeed('export'))

permission_supplier_section_get = BasePermission(SupplierSectionActionNeed('get'))
permission_supplier_section_edit = BasePermission(SupplierSectionActionNeed('edit'))
permission_supplier_section_del = BasePermission(SupplierSectionActionNeed('del'))
permission_supplier_section_audit = BasePermission(SupplierSectionActionNeed('audit'))
permission_supplier_section_print = BasePermission(SupplierSectionActionNeed('print'))
