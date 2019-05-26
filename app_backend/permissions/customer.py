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

import six

from app_backend.permissions import SectionActionNeed, BasePermission, SectionActionItemNeed

# -------------------------------------------------------------
# 客户板块操作权限（创建、查询、导出、统计）
CustomerSectionNeed = partial(SectionActionNeed, 'customer')
CustomerSectionNeed.__doc__ = """A need with the section preset to `"customer"`."""

permission_customer_section_add = BasePermission(CustomerSectionNeed('add'))
permission_customer_section_search = BasePermission(CustomerSectionNeed('search'))
permission_customer_section_export = BasePermission(CustomerSectionNeed('export'))
permission_customer_section_stats = BasePermission(CustomerSectionNeed('stats'))


# -------------------------------------------------------------
# 客户明细操作权限(读取、更新、删除、打印)
CustomerItemNeed = partial(SectionActionItemNeed, 'customer')
CustomerItemNeed.__doc__ = """A need with the section preset to `"customer"`."""

CustomerItemGetNeed = partial(CustomerItemNeed, 'get')
CustomerItemEditNeed = partial(CustomerItemNeed, 'edit')
CustomerItemDelNeed = partial(CustomerItemNeed, 'del')
CustomerItemPrintNeed = partial(CustomerItemNeed, 'print')


class CustomerItemGetPermission(BasePermission):
    def __init__(self, customer_id):
        need = CustomerItemGetNeed(six.text_type(customer_id))
        super(CustomerItemGetPermission, self).__init__(need)


class CustomerItemEditPermission(BasePermission):
    def __init__(self, customer_id):
        need = CustomerItemEditNeed(six.text_type(customer_id))
        super(CustomerItemEditPermission, self).__init__(need)


class CustomerItemDelPermission(BasePermission):
    def __init__(self, customer_id):
        need = CustomerItemDelNeed(six.text_type(customer_id))
        super(CustomerItemDelPermission, self).__init__(need)


class CustomerItemPrintPermission(BasePermission):
    def __init__(self, customer_id):
        need = CustomerItemPrintNeed(six.text_type(customer_id))
        super(CustomerItemPrintPermission, self).__init__(need)
