#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: rack.py
@time: 2019-05-12 09:58
"""

from __future__ import unicode_literals

from functools import partial

from app_backend.permissions import SectionNeed, SectionActionNeed, BasePermission

# -------------------------------------------------------------
# 货架板块整体权限
RackSectionNeed = partial(SectionNeed, 'rack')
permission_rack_section = BasePermission(RackSectionNeed())

# -------------------------------------------------------------
# 货架板块操作权限（创建、查询、导出、统计）
RackSectionActionNeed = partial(SectionActionNeed, 'rack')
RackSectionActionNeed.__doc__ = """A need with the section preset to `"rack"`."""

permission_rack_section_add = BasePermission(RackSectionActionNeed('add'))
permission_rack_section_search = BasePermission(RackSectionActionNeed('search'))
permission_rack_section_export = BasePermission(RackSectionActionNeed('export'))
permission_rack_section_stats = BasePermission(RackSectionActionNeed('stats'))
