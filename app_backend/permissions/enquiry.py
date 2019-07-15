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

import six

from app_backend.permissions import SectionNeed, SectionActionNeed, BasePermission, SectionActionItemNeed

# -------------------------------------------------------------
# 询价板块整体权限
EnquirySectionNeed = partial(SectionNeed, 'enquiry')
permission_enquiry_section = BasePermission(EnquirySectionNeed())

# -------------------------------------------------------------
# 询价板块操作权限（创建、查询、导出、统计）
EnquirySectionActionNeed = partial(SectionActionNeed, 'enquiry')
EnquirySectionActionNeed.__doc__ = """A need with the section preset to `"enquiry"`."""

permission_enquiry_section_add = BasePermission(EnquirySectionActionNeed('add'))
permission_enquiry_section_search = BasePermission(EnquirySectionActionNeed('search'))
permission_enquiry_section_export = BasePermission(EnquirySectionActionNeed('export'))
permission_enquiry_section_stats = BasePermission(EnquirySectionActionNeed('stats'))

# -------------------------------------------------------------
# 询价明细操作权限（读取、更新、删除、打印、审核）
EnquiryItemNeed = partial(SectionActionItemNeed, 'enquiry')
EnquiryItemNeed.__doc__ = """A need with the section preset to `"enquiry"`."""

EnquiryItemGetNeed = partial(EnquiryItemNeed, 'get')
EnquiryItemEditNeed = partial(EnquiryItemNeed, 'edit')
EnquiryItemDelNeed = partial(EnquiryItemNeed, 'del')
EnquiryItemPrintNeed = partial(EnquiryItemNeed, 'print')
EnquiryItemAuditNeed = partial(EnquiryItemNeed, 'audit')


class EnquiryItemGetPermission(BasePermission):
    def __init__(self, enquiry_id):
        need = EnquiryItemGetNeed(six.text_type(enquiry_id))
        super(EnquiryItemGetPermission, self).__init__(need)


class EnquiryItemEditPermission(BasePermission):
    def __init__(self, enquiry_id):
        need = EnquiryItemEditNeed(six.text_type(enquiry_id))
        super(EnquiryItemEditPermission, self).__init__(need)


class EnquiryItemDelPermission(BasePermission):
    def __init__(self, enquiry_id):
        need = EnquiryItemDelNeed(six.text_type(enquiry_id))
        super(EnquiryItemDelPermission, self).__init__(need)


class EnquiryItemPrintPermission(BasePermission):
    def __init__(self, enquiry_id):
        need = EnquiryItemPrintNeed(six.text_type(enquiry_id))
        super(EnquiryItemPrintPermission, self).__init__(need)


class EnquiryItemAuditPermission(BasePermission):
    def __init__(self, enquiry_id):
        need = EnquiryItemAuditNeed(six.text_type(enquiry_id))
        super(EnquiryItemAuditPermission, self).__init__(need)
