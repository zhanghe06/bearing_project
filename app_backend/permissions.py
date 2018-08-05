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
# 角色类型 0:默认,1:系统,2:销售,3:经理,4:库管,5:财务,6:采购
roles = [
    '默认',
    '系统',
    '销售',
    '经理',
    '库管',
    '财务',
    '采购',
]

# 角色权限
permission_role_default = Permission(RoleNeed('默认'))
permission_role_administrator = Permission(RoleNeed('系统'))
permission_role_sales = Permission(RoleNeed('销售'))
permission_role_manager = Permission(RoleNeed('经理'))
permission_role_stock_keeper = Permission(RoleNeed('库管'))
permission_role_accountant = Permission(RoleNeed('财务'))
permission_role_purchaser = Permission(RoleNeed('采购'))

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
ProductionSectionNeed = partial(SectionActionNeed, 'production')
ProductionSectionNeed.__doc__ = """A need with the section preset to `"production"`."""

permission_production_section_add = Permission(ProductionSectionNeed('add'))
permission_production_section_search = Permission(ProductionSectionNeed('search'))
permission_production_section_export = Permission(ProductionSectionNeed('export'))
permission_production_section_stats = Permission(ProductionSectionNeed('stats'))

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
QuotationSectionNeed = partial(SectionActionNeed, 'quotation')
QuotationSectionNeed.__doc__ = """A need with the section preset to `"quotation"`."""

permission_quotation_section_add = Permission(QuotationSectionNeed('add'))
permission_quotation_section_search = Permission(QuotationSectionNeed('search'))
permission_quotation_section_export = Permission(QuotationSectionNeed('export'))
permission_quotation_section_stats = Permission(QuotationSectionNeed('stats'))

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
# ProductionItemNeed = partial(SectionActionItemNeed, 'production')
# ProductionItemNeed.__doc__ = """A need with the section preset to `"production"`."""
#
# ProductionItemGetNeed = partial(ProductionItemNeed, 'get')
# ProductionItemEditNeed = partial(ProductionItemNeed, 'edit')
# ProductionItemDelNeed = partial(ProductionItemNeed, 'del')
# ProductionItemPrintNeed = partial(ProductionItemNeed, 'print')
#
#
# class ProductionItemGetPermission(Permission):
#     def __init__(self, production_id):
#         need = ProductionItemGetNeed(unicode(production_id))
#         super(ProductionItemGetPermission, self).__init__(need)
#
#
# class ProductionItemEditPermission(Permission):
#     def __init__(self, production_id):
#         need = ProductionItemEditNeed(unicode(production_id))
#         super(ProductionItemEditPermission, self).__init__(need)
#
#
# class ProductionItemDelPermission(Permission):
#     def __init__(self, production_id):
#         need = ProductionItemDelNeed(unicode(production_id))
#         super(ProductionItemDelPermission, self).__init__(need)
#
#
# class ProductionItemPrintPermission(Permission):
#     def __init__(self, production_id):
#         need = ProductionItemPrintNeed(unicode(production_id))
#         super(ProductionItemPrintPermission, self).__init__(need)


# -------------------------------------------------------------
# 报价明细操作权限（读取、更新、删除、打印、审核）
QuotationItemNeed = partial(SectionActionItemNeed, 'quotation')
QuotationItemNeed.__doc__ = """A need with the section preset to `"quotation"`."""

QuotationItemGetNeed = partial(QuotationItemNeed, 'get')
QuotationItemEditNeed = partial(QuotationItemNeed, 'edit')
QuotationItemDelNeed = partial(QuotationItemNeed, 'del')
QuotationItemPrintNeed = partial(QuotationItemNeed, 'print')
QuotationItemAuditNeed = partial(QuotationItemNeed, 'audit')


class QuotationItemGetPermission(Permission):
    def __init__(self, quotation_id):
        need = QuotationItemGetNeed(unicode(quotation_id))
        super(QuotationItemGetPermission, self).__init__(need)


class QuotationItemEditPermission(Permission):
    def __init__(self, quotation_id):
        need = QuotationItemEditNeed(unicode(quotation_id))
        super(QuotationItemEditPermission, self).__init__(need)


class QuotationItemDelPermission(Permission):
    def __init__(self, quotation_id):
        need = QuotationItemDelNeed(unicode(quotation_id))
        super(QuotationItemDelPermission, self).__init__(need)


class QuotationItemPrintPermission(Permission):
    def __init__(self, quotation_id):
        need = QuotationItemPrintNeed(unicode(quotation_id))
        super(QuotationItemPrintPermission, self).__init__(need)


class QuotationItemAuditPermission(Permission):
    def __init__(self, quotation_id):
        need = QuotationItemAuditNeed(unicode(quotation_id))
        super(QuotationItemAuditPermission, self).__init__(need)
