#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: customer.py
@time: 2019-05-12 09:56
"""

from __future__ import unicode_literals

from functools import partial

from app_backend.permissions import SectionNeed, SectionActionNeed, BasePermission

# -------------------------------------------------------------
# 客户板块整体权限
CustomerSectionNeed = partial(SectionNeed, 'customer')
permission_customer_section = BasePermission(CustomerSectionNeed())

# -------------------------------------------------------------
# 客户板块操作权限（创建、查询、统计、导出、详情、编辑、删除、审核、打印）
CustomerSectionActionNeed = partial(SectionActionNeed, 'customer')
CustomerSectionActionNeed.__doc__ = """A need with the section preset to `"customer"`."""

permission_customer_section_add = BasePermission(CustomerSectionActionNeed('add'))
permission_customer_section_search = BasePermission(CustomerSectionActionNeed('search'))
permission_customer_section_stats = BasePermission(CustomerSectionActionNeed('stats'))
permission_customer_section_export = BasePermission(CustomerSectionActionNeed('export'))

permission_customer_section_get = BasePermission(CustomerSectionActionNeed('get'))
permission_customer_section_edit = BasePermission(CustomerSectionActionNeed('edit'))
permission_customer_section_del = BasePermission(CustomerSectionActionNeed('del'))
permission_customer_section_audit = BasePermission(CustomerSectionActionNeed('audit'))
permission_customer_section_print = BasePermission(CustomerSectionActionNeed('print'))
