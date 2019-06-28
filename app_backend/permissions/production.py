#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: production.py
@time: 2019-05-12 09:57
"""

from __future__ import unicode_literals

from functools import partial

from app_backend.permissions import SectionActionNeed, BasePermission, SectionActionItemNeed

# -------------------------------------------------------------
# 产品板块操作权限（创建、查询、导出、统计）
ProductionSectionNeed = partial(SectionActionNeed, 'production')
ProductionSectionNeed.__doc__ = """A need with the section preset to `"production"`."""

permission_production_section_add = BasePermission(ProductionSectionNeed('add'))
permission_production_section_search = BasePermission(ProductionSectionNeed('search'))
permission_production_section_export = BasePermission(ProductionSectionNeed('export'))
permission_production_section_stats = BasePermission(ProductionSectionNeed('stats'))
