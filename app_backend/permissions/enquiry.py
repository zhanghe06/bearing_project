#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: enquiry.py
@time: 2019-05-12 09:59
"""

from __future__ import unicode_literals

from functools import partial

from app_backend.permissions import SectionNeed, SectionActionNeed, BasePermission

# -------------------------------------------------------------
# 询价板块整体权限
EnquirySectionNeed = partial(SectionNeed, 'enquiry')
permission_enquiry_section = BasePermission(EnquirySectionNeed())

# -------------------------------------------------------------
# 询价板块操作权限（创建、查询、统计、导出、详情、编辑、删除、审核、打印）
EnquirySectionActionNeed = partial(SectionActionNeed, 'enquiry')
EnquirySectionActionNeed.__doc__ = """A need with the section preset to `"enquiry"`."""

permission_enquiry_section_add = BasePermission(EnquirySectionActionNeed('add'))
permission_enquiry_section_search = BasePermission(EnquirySectionActionNeed('search'))
permission_enquiry_section_stats = BasePermission(EnquirySectionActionNeed('stats'))
permission_enquiry_section_export = BasePermission(EnquirySectionActionNeed('export'))

permission_enquiry_section_get = BasePermission(EnquirySectionActionNeed('get'))
permission_enquiry_section_edit = BasePermission(EnquirySectionActionNeed('edit'))
permission_enquiry_section_del = BasePermission(EnquirySectionActionNeed('del'))
permission_enquiry_section_audit = BasePermission(EnquirySectionActionNeed('audit'))
permission_enquiry_section_print = BasePermission(EnquirySectionActionNeed('print'))
