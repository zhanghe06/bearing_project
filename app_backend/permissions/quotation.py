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

import six

from app_backend.permissions import SectionActionNeed, BasePermission, SectionActionItemNeed

# -------------------------------------------------------------
# 报价板块操作权限（创建、查询、导出、统计）
QuotationSectionNeed = partial(SectionActionNeed, 'quotation')
QuotationSectionNeed.__doc__ = """A need with the section preset to `"quotation"`."""

permission_quotation_section_add = BasePermission(QuotationSectionNeed('add'))
permission_quotation_section_search = BasePermission(QuotationSectionNeed('search'))
permission_quotation_section_export = BasePermission(QuotationSectionNeed('export'))
permission_quotation_section_stats = BasePermission(QuotationSectionNeed('stats'))

# -------------------------------------------------------------
# 报价明细操作权限（读取、更新、删除、打印、审核）
QuotationItemNeed = partial(SectionActionItemNeed, 'quotation')
QuotationItemNeed.__doc__ = """A need with the section preset to `"quotation"`."""

QuotationItemGetNeed = partial(QuotationItemNeed, 'get')
QuotationItemEditNeed = partial(QuotationItemNeed, 'edit')
QuotationItemDelNeed = partial(QuotationItemNeed, 'del')
QuotationItemPrintNeed = partial(QuotationItemNeed, 'print')
QuotationItemAuditNeed = partial(QuotationItemNeed, 'audit')


class QuotationItemGetPermission(BasePermission):
    def __init__(self, quotation_id):
        need = QuotationItemGetNeed(six.text_type(quotation_id))
        super(QuotationItemGetPermission, self).__init__(need)


class QuotationItemEditPermission(BasePermission):
    def __init__(self, quotation_id):
        need = QuotationItemEditNeed(six.text_type(quotation_id))
        super(QuotationItemEditPermission, self).__init__(need)


class QuotationItemDelPermission(BasePermission):
    def __init__(self, quotation_id):
        need = QuotationItemDelNeed(six.text_type(quotation_id))
        super(QuotationItemDelPermission, self).__init__(need)


class QuotationItemPrintPermission(BasePermission):
    def __init__(self, quotation_id):
        need = QuotationItemPrintNeed(six.text_type(quotation_id))
        super(QuotationItemPrintPermission, self).__init__(need)


class QuotationItemAuditPermission(BasePermission):
    def __init__(self, quotation_id):
        need = QuotationItemAuditNeed(six.text_type(quotation_id))
        super(QuotationItemAuditPermission, self).__init__(need)
