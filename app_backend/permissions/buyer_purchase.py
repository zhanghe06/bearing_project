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

from app_backend.permissions import SectionNeed, SectionActionNeed, BasePermission

# -------------------------------------------------------------
# 采购进货板块整体权限
PurchaseSectionNeed = partial(SectionNeed, 'purchase')
permission_purchase_section = BasePermission(PurchaseSectionNeed())

# -------------------------------------------------------------
# 采购进货板块操作权限（创建、查询、统计、导出、详情、编辑、删除、审核、打印）
PurchaseSectionActionNeed = partial(SectionActionNeed, 'purchase')
PurchaseSectionActionNeed.__doc__ = """A need with the section preset to `"purchase"`."""

permission_purchase_section_add = BasePermission(PurchaseSectionActionNeed('add'))
permission_purchase_section_search = BasePermission(PurchaseSectionActionNeed('search'))
permission_purchase_section_stats = BasePermission(PurchaseSectionActionNeed('stats'))
permission_purchase_section_export = BasePermission(PurchaseSectionActionNeed('export'))

permission_purchase_section_get = BasePermission(PurchaseSectionActionNeed('get'))
permission_purchase_section_edit = BasePermission(PurchaseSectionActionNeed('edit'))
permission_purchase_section_del = BasePermission(PurchaseSectionActionNeed('del'))
permission_purchase_section_audit = BasePermission(PurchaseSectionActionNeed('audit'))
permission_purchase_section_print = BasePermission(PurchaseSectionActionNeed('print'))
