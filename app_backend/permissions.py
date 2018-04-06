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

from flask_principal import Permission, RoleNeed


SectionActionNeed = namedtuple('Need', ['section', 'action'])
SectionActionItemNeed = namedtuple('ItemNeed', ['section', 'action', 'item_id'])

# -------------------------------------------------------------
# 角色类型 0:默认,1:系统,2:销售,3:经理,4:库管,5:财务
roles = [
    '默认',
    '系统',
    '销售',
    '经理',
    '库管',
    '财务',
]

# 角色权限
permission_role_default = Permission(RoleNeed('默认'))
permission_role_administrator = Permission(RoleNeed('系统'))
permission_role_sales = Permission(RoleNeed('销售'))
permission_role_manager = Permission(RoleNeed('经理'))
permission_role_stock_keeper = Permission(RoleNeed('库管'))
permission_role_accountant = Permission(RoleNeed('财务'))


# =============================================================
# 板块基本操作权限（创建、查询、导出、统计）与用户的角色身份相关，需关联
#
# 操作     角色
# ------------
# 创建     销售
# 查询     销售、经理
# 导出     经理
# 统计     销售、经理
#
# =============================================================


# -------------------------------------------------------------
# 客户板块操作权限（创建、查询、导出、统计）
CustomerSectionNeed = partial(SectionActionNeed, 'customer')
CustomerSectionNeed.__doc__ = """A need with the section preset to `"customer"`."""

permission_customer_section_add = Permission(CustomerSectionNeed('add'))
permission_customer_section_search = Permission(CustomerSectionNeed('search'))
permission_customer_section_export = Permission(CustomerSectionNeed('export'))
permission_customer_section_stats = Permission(CustomerSectionNeed('stats'))


# -------------------------------------------------------------
# 用户板块操作权限（创建、查询、导出、统计）
UserSectionNeed = partial(SectionActionNeed, 'user')
UserSectionNeed.__doc__ = """A need with the section preset to `"user"`."""

permission_user_section_add = Permission(UserSectionNeed('add'))
permission_user_section_search = Permission(UserSectionNeed('search'))
permission_user_section_export = Permission(UserSectionNeed('export'))
permission_user_section_stats = Permission(UserSectionNeed('stats'))


# -------------------------------------------------------------
# 产品板块操作权限（创建、查询、导出、统计）
ProductSectionNeed = partial(SectionActionNeed, 'product')
ProductSectionNeed.__doc__ = """A need with the section preset to `"product"`."""

permission_product_section_add = Permission(ProductSectionNeed('add'))
permission_product_section_search = Permission(ProductSectionNeed('search'))
permission_product_section_export = Permission(ProductSectionNeed('export'))
permission_product_section_stats = Permission(ProductSectionNeed('stats'))


# -------------------------------------------------------------
# 仓库板块操作权限（创建、查询、导出、统计）
WarehouseSectionNeed = partial(SectionActionNeed, 'warehouse')
WarehouseSectionNeed.__doc__ = """A need with the section preset to `"warehouse"`."""

permission_warehouse_section_add = Permission(WarehouseSectionNeed('add'))
permission_warehouse_section_search = Permission(WarehouseSectionNeed('search'))
permission_warehouse_section_export = Permission(WarehouseSectionNeed('export'))
permission_warehouse_section_stats = Permission(WarehouseSectionNeed('stats'))


# -------------------------------------------------------------
# 货架板块操作权限（创建、查询、导出、统计）
RackSectionNeed = partial(SectionActionNeed, 'rack')
RackSectionNeed.__doc__ = """A need with the section preset to `"rack"`."""

permission_rack_section_add = Permission(RackSectionNeed('add'))
permission_rack_section_search = Permission(RackSectionNeed('search'))
permission_rack_section_export = Permission(RackSectionNeed('export'))
permission_rack_section_stats = Permission(RackSectionNeed('stats'))


# -------------------------------------------------------------
# 库存板块操作权限（创建、查询、导出、统计）
InventorySectionNeed = partial(SectionActionNeed, 'inventory')
InventorySectionNeed.__doc__ = """A need with the section preset to `"inventory"`."""

permission_inventory_section_add = Permission(InventorySectionNeed('add'))
permission_inventory_section_search = Permission(InventorySectionNeed('search'))
permission_inventory_section_export = Permission(InventorySectionNeed('export'))
permission_inventory_section_stats = Permission(InventorySectionNeed('stats'))


# -------------------------------------------------------------
# 报价板块操作权限（创建、查询、导出、统计）
QuoteSectionNeed = partial(SectionActionNeed, 'quote')
QuoteSectionNeed.__doc__ = """A need with the section preset to `"quote"`."""

permission_quote_section_add = Permission(QuoteSectionNeed('add'))
permission_quote_section_search = Permission(QuoteSectionNeed('search'))
permission_quote_section_export = Permission(QuoteSectionNeed('export'))
permission_quote_section_stats = Permission(QuoteSectionNeed('stats'))


# =============================================================
# 因客户、报价有所有者，明细操作需要校验所有者身份，下面单独配置明细权限
# 用户、产品因其为系统基础资源，应由系统管理角色操作，需单独设置此类权限
# 业务实现：如需新建用户、新建产品，通过邮件提出申请，由管理员来执行操作
# =============================================================


# -------------------------------------------------------------
# 客户明细操作权限(读取、更新、删除、打印)
CustomerItemNeed = partial(SectionActionItemNeed, 'customer')
CustomerItemNeed.__doc__ = """A need with the section preset to `"customer"`."""

CustomerItemGetNeed = partial(CustomerItemNeed, 'get')
CustomerItemEditNeed = partial(CustomerItemNeed, 'edit')
CustomerItemDelNeed = partial(CustomerItemNeed, 'del')
CustomerItemPrintNeed = partial(CustomerItemNeed, 'print')


class CustomerItemGetPermission(Permission):
    def __init__(self, customer_id):
        need = CustomerItemGetNeed(unicode(customer_id))
        super(CustomerItemGetPermission, self).__init__(need)


class CustomerItemEditPermission(Permission):
    def __init__(self, customer_id):
        need = CustomerItemEditNeed(unicode(customer_id))
        super(CustomerItemEditPermission, self).__init__(need)


class CustomerItemDelPermission(Permission):
    def __init__(self, customer_id):
        need = CustomerItemDelNeed(unicode(customer_id))
        super(CustomerItemDelPermission, self).__init__(need)


class CustomerItemPrintPermission(Permission):
    def __init__(self, customer_id):
        need = CustomerItemPrintNeed(unicode(customer_id))
        super(CustomerItemPrintPermission, self).__init__(need)


# -------------------------------------------------------------
# 用户明细操作权限(读取、更新、删除、打印)
UserItemNeed = partial(SectionActionItemNeed, 'user')
UserItemNeed.__doc__ = """A need with the section preset to `"user"`."""

UserItemGetNeed = partial(UserItemNeed, 'get')
UserItemEditNeed = partial(UserItemNeed, 'edit')
UserItemDelNeed = partial(UserItemNeed, 'del')
UserItemPrintNeed = partial(UserItemNeed, 'print')


class UserItemGetPermission(Permission):
    def __init__(self, user_id):
        need = UserItemGetNeed(unicode(user_id))
        super(UserItemGetPermission, self).__init__(need)


class UserItemEditPermission(Permission):
    def __init__(self, user_id):
        need = UserItemEditNeed(unicode(user_id))
        super(UserItemEditPermission, self).__init__(need)


class UserItemDelPermission(Permission):
    def __init__(self, user_id):
        need = UserItemDelNeed(unicode(user_id))
        super(UserItemDelPermission, self).__init__(need)


class UserItemPrintPermission(Permission):
    def __init__(self, user_id):
        need = UserItemPrintNeed(unicode(user_id))
        super(UserItemPrintPermission, self).__init__(need)


# # -------------------------------------------------------------
# # 产品明细操作权限(读取、更新、删除、打印)
# ProductItemNeed = partial(SectionActionItemNeed, 'product')
# ProductItemNeed.__doc__ = """A need with the section preset to `"product"`."""
#
# ProductItemGetNeed = partial(ProductItemNeed, 'get')
# ProductItemEditNeed = partial(ProductItemNeed, 'edit')
# ProductItemDelNeed = partial(ProductItemNeed, 'del')
# ProductItemPrintNeed = partial(ProductItemNeed, 'print')
#
#
# class ProductItemGetPermission(Permission):
#     def __init__(self, product_id):
#         need = ProductItemGetNeed(unicode(product_id))
#         super(ProductItemGetPermission, self).__init__(need)
#
#
# class ProductItemEditPermission(Permission):
#     def __init__(self, product_id):
#         need = ProductItemEditNeed(unicode(product_id))
#         super(ProductItemEditPermission, self).__init__(need)
#
#
# class ProductItemDelPermission(Permission):
#     def __init__(self, product_id):
#         need = ProductItemDelNeed(unicode(product_id))
#         super(ProductItemDelPermission, self).__init__(need)
#
#
# class ProductItemPrintPermission(Permission):
#     def __init__(self, product_id):
#         need = ProductItemPrintNeed(unicode(product_id))
#         super(ProductItemPrintPermission, self).__init__(need)


# -------------------------------------------------------------
# 报价明细操作权限（读取、更新、删除、打印、审核）
QuoteItemNeed = partial(SectionActionItemNeed, 'quote')
QuoteItemNeed.__doc__ = """A need with the section preset to `"quote"`."""

QuoteItemGetNeed = partial(QuoteItemNeed, 'get')
QuoteItemEditNeed = partial(QuoteItemNeed, 'edit')
QuoteItemDelNeed = partial(QuoteItemNeed, 'del')
QuoteItemPrintNeed = partial(QuoteItemNeed, 'print')
QuoteItemAuditNeed = partial(QuoteItemNeed, 'audit')


class QuoteItemGetPermission(Permission):
    def __init__(self, quote_id):
        need = QuoteItemGetNeed(unicode(quote_id))
        super(QuoteItemGetPermission, self).__init__(need)


class QuoteItemEditPermission(Permission):
    def __init__(self, quote_id):
        need = QuoteItemEditNeed(unicode(quote_id))
        super(QuoteItemEditPermission, self).__init__(need)


class QuoteItemDelPermission(Permission):
    def __init__(self, quote_id):
        need = QuoteItemDelNeed(unicode(quote_id))
        super(QuoteItemDelPermission, self).__init__(need)


class QuoteItemPrintPermission(Permission):
    def __init__(self, quote_id):
        need = QuoteItemPrintNeed(unicode(quote_id))
        super(QuoteItemPrintPermission, self).__init__(need)


class QuoteItemAuditPermission(Permission):
    def __init__(self, quote_id):
        need = QuoteItemAuditNeed(unicode(quote_id))
        super(QuoteItemAuditPermission, self).__init__(need)
