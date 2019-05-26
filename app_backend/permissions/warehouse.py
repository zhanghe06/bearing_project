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

import six

from app_backend.permissions import SectionActionNeed, BasePermission, SectionActionItemNeed

# -------------------------------------------------------------
# 仓库板块操作权限（创建、查询、导出、统计）
WarehouseSectionNeed = partial(SectionActionNeed, 'warehouse')
WarehouseSectionNeed.__doc__ = """A need with the section preset to `"warehouse"`."""

permission_warehouse_section_add = BasePermission(WarehouseSectionNeed('add'))
permission_warehouse_section_search = BasePermission(WarehouseSectionNeed('search'))
permission_warehouse_section_export = BasePermission(WarehouseSectionNeed('export'))
permission_warehouse_section_stats = BasePermission(WarehouseSectionNeed('stats'))
