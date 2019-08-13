#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: futures.py
@time: 2019-08-13 22:56
"""


from __future__ import unicode_literals

from functools import partial

from app_backend.permissions import SectionNeed, SectionActionNeed, BasePermission

# -------------------------------------------------------------
# 期货板块整体权限
FuturesSectionNeed = partial(SectionNeed, 'futures')
permission_futures_section = BasePermission(FuturesSectionNeed())

# -------------------------------------------------------------
# 期货板块操作权限（创建、查询、统计、导出、详情、编辑、删除、审核、打印）
FuturesSectionActionNeed = partial(SectionActionNeed, 'futures')
FuturesSectionActionNeed.__doc__ = """A need with the section preset to `"futures"`."""

permission_futures_section_add = BasePermission(FuturesSectionActionNeed('add'))
permission_futures_section_search = BasePermission(FuturesSectionActionNeed('search'))
permission_futures_section_stats = BasePermission(FuturesSectionActionNeed('stats'))
permission_futures_section_export = BasePermission(FuturesSectionActionNeed('export'))

permission_futures_section_get = BasePermission(FuturesSectionActionNeed('get'))
permission_futures_section_edit = BasePermission(FuturesSectionActionNeed('edit'))
permission_futures_section_del = BasePermission(FuturesSectionActionNeed('del'))
permission_futures_section_audit = BasePermission(FuturesSectionActionNeed('audit'))
permission_futures_section_print = BasePermission(FuturesSectionActionNeed('print'))
