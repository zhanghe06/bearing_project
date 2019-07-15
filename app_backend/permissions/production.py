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

from app_backend.permissions import SectionNeed, SectionActionNeed, BasePermission

# -------------------------------------------------------------
# 产品板块整体权限
ProductionSectionNeed = partial(SectionNeed, 'production')
permission_production_section = BasePermission(ProductionSectionNeed())

# -------------------------------------------------------------
# 产品板块操作权限（创建、查询、导出、统计）
ProductionSectionActionNeed = partial(SectionActionNeed, 'production')
ProductionSectionActionNeed.__doc__ = """A need with the section preset to `"production"`."""

permission_production_section_add = BasePermission(ProductionSectionActionNeed('add'))
permission_production_section_search = BasePermission(ProductionSectionActionNeed('search'))
permission_production_section_export = BasePermission(ProductionSectionActionNeed('export'))
permission_production_section_stats = BasePermission(ProductionSectionActionNeed('stats'))
