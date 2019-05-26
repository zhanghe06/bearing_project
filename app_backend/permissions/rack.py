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

import six

from app_backend.permissions import SectionActionNeed, BasePermission, SectionActionItemNeed

# -------------------------------------------------------------
# 货架板块操作权限（创建、查询、导出、统计）
RackSectionNeed = partial(SectionActionNeed, 'rack')
RackSectionNeed.__doc__ = """A need with the section preset to `"rack"`."""

permission_rack_section_add = BasePermission(RackSectionNeed('add'))
permission_rack_section_search = BasePermission(RackSectionNeed('search'))
permission_rack_section_export = BasePermission(RackSectionNeed('export'))
permission_rack_section_stats = BasePermission(RackSectionNeed('stats'))
