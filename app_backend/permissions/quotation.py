#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: quotation.py
@time: 2019-05-12 09:59
"""

from __future__ import unicode_literals

from functools import partial

from app_backend.permissions import SectionNeed, SectionActionNeed, BasePermission

# -------------------------------------------------------------
# 报价板块整体权限
QuotationSectionNeed = partial(SectionNeed, 'quotation')
permission_quotation_section = BasePermission(QuotationSectionNeed())

# -------------------------------------------------------------
# 报价板块操作权限（创建、查询、统计、导出、详情、编辑、删除、审核、打印）
QuotationSectionActionNeed = partial(SectionActionNeed, 'quotation')
QuotationSectionActionNeed.__doc__ = """A need with the section preset to `"quotation"`."""

permission_quotation_section_add = BasePermission(QuotationSectionActionNeed('add'))
permission_quotation_section_search = BasePermission(QuotationSectionActionNeed('search'))
permission_quotation_section_stats = BasePermission(QuotationSectionActionNeed('stats'))
permission_quotation_section_export = BasePermission(QuotationSectionActionNeed('export'))

permission_quotation_section_get = BasePermission(QuotationSectionActionNeed('get'))
permission_quotation_section_edit = BasePermission(QuotationSectionActionNeed('edit'))
permission_quotation_section_del = BasePermission(QuotationSectionActionNeed('del'))
permission_quotation_section_audit = BasePermission(QuotationSectionActionNeed('audit'))
permission_quotation_section_print = BasePermission(QuotationSectionActionNeed('print'))
