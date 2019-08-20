#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: account.py
@time: 2019-08-17 18:31
"""


from __future__ import unicode_literals

from functools import partial

from app_backend.permissions import SectionNeed, SectionActionNeed, BasePermission

# -------------------------------------------------------------
# 账户板块整体权限
AccountSectionNeed = partial(SectionNeed, 'account')
permission_account_section = BasePermission(AccountSectionNeed())

# -------------------------------------------------------------
# 账户板块操作权限（创建、查询、统计、导出、详情、编辑、删除、审核、打印）
AccountSectionActionNeed = partial(SectionActionNeed, 'account')
AccountSectionActionNeed.__doc__ = """A need with the section preset to `"account"`."""

permission_account_section_add = BasePermission(AccountSectionActionNeed('add'))
permission_account_section_search = BasePermission(AccountSectionActionNeed('search'))
permission_account_section_stats = BasePermission(AccountSectionActionNeed('stats'))
permission_account_section_export = BasePermission(AccountSectionActionNeed('export'))

permission_account_section_get = BasePermission(AccountSectionActionNeed('get'))
permission_account_section_edit = BasePermission(AccountSectionActionNeed('edit'))
permission_account_section_del = BasePermission(AccountSectionActionNeed('del'))
permission_account_section_audit = BasePermission(AccountSectionActionNeed('audit'))
permission_account_section_print = BasePermission(AccountSectionActionNeed('print'))

