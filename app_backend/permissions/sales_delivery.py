#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: sales_delivery.py
@time: 2019-05-12 10:00
"""

from __future__ import unicode_literals

from functools import partial

from app_backend.permissions import SectionNeed, SectionActionNeed, BasePermission

# -------------------------------------------------------------
# 销售出货板块整体权限
DeliverySectionNeed = partial(SectionNeed, 'delivery')
permission_delivery_section = BasePermission(DeliverySectionNeed())

# -------------------------------------------------------------
# 销售出货板块操作权限（创建、查询、统计、导出、详情、编辑、删除、审核、打印）
DeliverySectionActionNeed = partial(SectionActionNeed, 'delivery')
DeliverySectionActionNeed.__doc__ = """A need with the section preset to `"delivery"`."""

permission_delivery_section_add = BasePermission(DeliverySectionActionNeed('add'))
permission_delivery_section_search = BasePermission(DeliverySectionActionNeed('search'))
permission_delivery_section_stats = BasePermission(DeliverySectionActionNeed('stats'))
permission_delivery_section_export = BasePermission(DeliverySectionActionNeed('export'))

permission_delivery_section_get = BasePermission(DeliverySectionActionNeed('get'))
permission_delivery_section_edit = BasePermission(DeliverySectionActionNeed('edit'))
permission_delivery_section_del = BasePermission(DeliverySectionActionNeed('del'))
permission_delivery_section_audit = BasePermission(DeliverySectionActionNeed('audit'))
permission_delivery_section_print = BasePermission(DeliverySectionActionNeed('print'))
