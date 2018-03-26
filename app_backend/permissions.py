#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: permissions.py
@time: 2018-03-06 00:19
"""

from __future__ import unicode_literals

from collections import namedtuple
from functools import partial

from flask_principal import Need, ItemNeed, Permission, RoleNeed, TypeNeed, ActionNeed


# 自定义版块 need
SectionNeed = partial(Need, 'section')
SectionNeed.__doc__ = """A need with the method preset to `"section"`."""


# 参考 http://blog.csdn.net/jmilk/article/details/53542686

# -------------------------------------------------------------
# 角色类型 默认,销售,经理,系统
roles = [
    '默认',
    '销售',
    '经理',
    '系统',
]

# 角色权限
permission_role_default = Permission(RoleNeed('默认'))
permission_role_sales = Permission(RoleNeed('销售'))
permission_role_manager = Permission(RoleNeed('经理'))
permission_role_administrator = Permission(RoleNeed('系统'))


# -------------------------------------------------------------
# 版块类型 产品,客户,报价,统计,用户,角色,系统
sections = [
    '产品',
    '客户',
    '报价',
    '统计',
    '用户',
    '角色',
    '系统',
]

# 版块权限（默认查询权限）
permission_section_product = Permission(SectionNeed('产品'))
permission_section_customer = Permission(SectionNeed('客户'))
permission_section_quote = Permission(SectionNeed('报价'))
permission_section_stats = Permission(SectionNeed('统计'))
permission_section_user = Permission(SectionNeed('用户'))
permission_section_role = Permission(SectionNeed('角色'))
permission_section_sys = Permission(SectionNeed('系统'))


# =============================================================
# 板块基本操作权限（创建、查询、导出、统计、审核）与用户身份相关，需关联
#
# 操作     角色
# ------------
# 创建     销售
# 查询     销售、经理
# 导出     经理
# 统计     销售、经理
# 审核     经理
#
# 销售能够查看所属自己的内容，经理能够查看所属自己销售的内容
# =============================================================


# -------------------------------------------------------------
# 客户板块操作权限（创建、查询、导出、统计、审核）
CustomerSectionNeed = namedtuple('CustomerSection', ['action', 'uid'])

AddCustomerSectionNeed = partial(CustomerSectionNeed, 'add')
SearchCustomerSectionNeed = partial(CustomerSectionNeed, 'search')
ExportCustomerSectionNeed = partial(CustomerSectionNeed, 'export')
StatsCustomerSectionNeed = partial(CustomerSectionNeed, 'stats')
AuditCustomerSectionNeed = partial(CustomerSectionNeed, 'audit')


class AddCustomerSectionPermission(Permission):
    def __init__(self, uid):
        need = AddCustomerSectionNeed(unicode(uid))
        super(AddCustomerSectionPermission, self).__init__(need)


class SearchCustomerSectionPermission(Permission):
    def __init__(self, uid):
        need = SearchCustomerSectionNeed(unicode(uid))
        super(SearchCustomerSectionPermission, self).__init__(need)


class ExportCustomerSectionPermission(Permission):
    def __init__(self, uid):
        need = ExportCustomerSectionNeed(unicode(uid))
        super(ExportCustomerSectionPermission, self).__init__(need)


class StatsCustomerSectionPermission(Permission):
    def __init__(self, uid):
        need = StatsCustomerSectionNeed(unicode(uid))
        super(StatsCustomerSectionPermission, self).__init__(need)


class AuditCustomerSectionPermission(Permission):
    def __init__(self, uid):
        need = AuditCustomerSectionNeed(unicode(uid))
        super(AuditCustomerSectionPermission, self).__init__(need)


# -------------------------------------------------------------
# 报价板块操作权限（创建、查询、导出、统计、审核）
QuoteSectionNeed = namedtuple('QuoteSection', ['action', 'uid'])

AddQuoteSectionNeed = partial(QuoteSectionNeed, 'add')
SearchQuoteSectionNeed = partial(QuoteSectionNeed, 'search')
ExportQuoteSectionNeed = partial(QuoteSectionNeed, 'export')
StatsQuoteSectionNeed = partial(QuoteSectionNeed, 'stats')
AuditQuoteSectionNeed = partial(QuoteSectionNeed, 'audit')


class AddQuoteSectionPermission(Permission):
    def __init__(self, uid):
        need = AddQuoteSectionNeed(unicode(uid))
        super(AddQuoteSectionPermission, self).__init__(need)


class SearchQuoteSectionPermission(Permission):
    def __init__(self, uid):
        need = SearchQuoteSectionNeed(unicode(uid))
        super(SearchQuoteSectionPermission, self).__init__(need)


class ExportQuoteSectionPermission(Permission):
    def __init__(self, uid):
        need = ExportQuoteSectionNeed(unicode(uid))
        super(ExportQuoteSectionPermission, self).__init__(need)


class StatsQuoteSectionPermission(Permission):
    def __init__(self, uid):
        need = StatsQuoteSectionNeed(unicode(uid))
        super(StatsQuoteSectionPermission, self).__init__(need)


class AuditQuoteSectionPermission(Permission):
    def __init__(self, uid):
        need = AuditQuoteSectionNeed(unicode(uid))
        super(AuditQuoteSectionPermission, self).__init__(need)


# =============================================================
# 因客户、报价有所有者，明细操作需要校验所有者身份，下面单独配置明细权限
# =============================================================


# -------------------------------------------------------------
# 客户明细操作权限(读取、更新、删除、打印)
CustomerItemNeed = namedtuple('CustomerItem', ['action', 'item_id'])

GetCustomerItemNeed = partial(CustomerItemNeed, 'get')
EditCustomerItemNeed = partial(CustomerItemNeed, 'edit')
DelCustomerItemNeed = partial(CustomerItemNeed, 'del')
PrintCustomerItemNeed = partial(CustomerItemNeed, 'print')


class GetCustomerItemPermission(Permission):
    def __init__(self, customer_id):
        need = GetCustomerItemNeed(unicode(customer_id))
        super(GetCustomerItemPermission, self).__init__(need)


class EditCustomerItemPermission(Permission):
    def __init__(self, customer_id):
        need = EditCustomerItemNeed(unicode(customer_id))
        super(EditCustomerItemPermission, self).__init__(need)


class DelCustomerItemPermission(Permission):
    def __init__(self, customer_id):
        need = DelCustomerItemNeed(unicode(customer_id))
        super(DelCustomerItemPermission, self).__init__(need)


class PrintCustomerItemPermission(Permission):
    def __init__(self, customer_id):
        need = PrintCustomerItemNeed(unicode(customer_id))
        super(PrintCustomerItemPermission, self).__init__(need)


# -------------------------------------------------------------
# 报价明细操作权限（读取、更新、删除、打印）
QuoteItemNeed = namedtuple('QuoteItem', ['action', 'item_id'])

GetQuoteItemNeed = partial(QuoteItemNeed, 'get')
EditQuoteItemNeed = partial(QuoteItemNeed, 'edit')
DelQuoteItemNeed = partial(QuoteItemNeed, 'del')
PrintQuoteItemNeed = partial(QuoteItemNeed, 'print')


class GetQuoteItemPermission(Permission):
    def __init__(self, quote_id):
        need = GetQuoteItemNeed(unicode(quote_id))
        super(GetQuoteItemPermission, self).__init__(need)


class EditQuoteItemPermission(Permission):
    def __init__(self, quote_id):
        need = EditQuoteItemNeed(unicode(quote_id))
        super(EditQuoteItemPermission, self).__init__(need)


class DelQuoteItemPermission(Permission):
    def __init__(self, quote_id):
        need = DelQuoteItemNeed(unicode(quote_id))
        super(DelQuoteItemPermission, self).__init__(need)


class PrintQuoteItemPermission(Permission):
    def __init__(self, quote_id):
        need = PrintQuoteItemNeed(unicode(quote_id))
        super(PrintQuoteItemPermission, self).__init__(need)
