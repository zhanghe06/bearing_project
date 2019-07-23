#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: user.py
@time: 2019-05-12 09:57
"""

from __future__ import unicode_literals

from functools import partial

from app_backend.permissions import SectionNeed, SectionActionNeed, BasePermission

# -------------------------------------------------------------
# 用户板块整体权限
UserSectionNeed = partial(SectionNeed, 'user')
permission_user_section = BasePermission(UserSectionNeed())

# -------------------------------------------------------------
# 用户板块操作权限（创建、查询、统计、导出、详情、编辑、删除、审核、打印）
UserSectionActionNeed = partial(SectionActionNeed, 'user')
UserSectionActionNeed.__doc__ = """A need with the section preset to `"user"`."""

permission_user_section_add = BasePermission(UserSectionActionNeed('add'))
permission_user_section_search = BasePermission(UserSectionActionNeed('search'))
permission_user_section_stats = BasePermission(UserSectionActionNeed('stats'))
permission_user_section_export = BasePermission(UserSectionActionNeed('export'))

permission_user_section_get = BasePermission(UserSectionActionNeed('get'))
permission_user_section_edit = BasePermission(UserSectionActionNeed('edit'))
permission_user_section_del = BasePermission(UserSectionActionNeed('del'))
permission_user_section_audit = BasePermission(UserSectionActionNeed('audit'))
permission_user_section_print = BasePermission(UserSectionActionNeed('print'))
