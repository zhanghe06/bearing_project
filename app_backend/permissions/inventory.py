#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: inventory.py
@time: 2019-05-12 09:58
"""

from __future__ import unicode_literals

from functools import partial

import six

from app_backend.permissions import SectionActionNeed, BasePermission, SectionActionItemNeed

# -------------------------------------------------------------
# 库存板块操作权限（创建、查询、导出、统计）
InventorySectionNeed = partial(SectionActionNeed, 'inventory')
InventorySectionNeed.__doc__ = """A need with the section preset to `"inventory"`."""

permission_inventory_section_add = BasePermission(InventorySectionNeed('add'))
permission_inventory_section_search = BasePermission(InventorySectionNeed('search'))
permission_inventory_section_export = BasePermission(InventorySectionNeed('export'))
permission_inventory_section_stats = BasePermission(InventorySectionNeed('stats'))
