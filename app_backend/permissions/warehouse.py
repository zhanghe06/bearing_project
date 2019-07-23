#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: warehouse.py
@time: 2019-05-12 09:58
"""

from __future__ import unicode_literals

from functools import partial

from app_backend.permissions import SectionNeed, SectionActionNeed, BasePermission

# -------------------------------------------------------------
# 仓库板块整体权限
WarehouseSectionNeed = partial(SectionNeed, 'warehouse')
permission_warehouse_section = BasePermission(WarehouseSectionNeed())

# -------------------------------------------------------------
# 仓库板块操作权限（创建、查询、统计、导出、详情、编辑、删除、审核、打印）
WarehouseSectionActionNeed = partial(SectionActionNeed, 'warehouse')
WarehouseSectionActionNeed.__doc__ = """A need with the section preset to `"warehouse"`."""

permission_warehouse_section_add = BasePermission(WarehouseSectionActionNeed('add'))
permission_warehouse_section_search = BasePermission(WarehouseSectionActionNeed('search'))
permission_warehouse_section_stats = BasePermission(WarehouseSectionActionNeed('stats'))
permission_warehouse_section_export = BasePermission(WarehouseSectionActionNeed('export'))

permission_warehouse_section_get = BasePermission(WarehouseSectionActionNeed('get'))
permission_warehouse_section_edit = BasePermission(WarehouseSectionActionNeed('edit'))
permission_warehouse_section_del = BasePermission(WarehouseSectionActionNeed('del'))
permission_warehouse_section_audit = BasePermission(WarehouseSectionActionNeed('audit'))
permission_warehouse_section_print = BasePermission(WarehouseSectionActionNeed('print'))
