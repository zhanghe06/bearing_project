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
import six

from flask_principal import Permission, RoleNeed


class BasePermission(Permission):
    """
    自定义权限控制
    """
    def allows(self, identity):
        return False  # 权限全局开关 (True:禁用权限控制, False:开启权限控制)


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
permission_role_default = BasePermission(RoleNeed('默认'))
permission_role_administrator = BasePermission(RoleNeed('系统'))
permission_role_sales = BasePermission(RoleNeed('销售'))
permission_role_manager = BasePermission(RoleNeed('经理'))
permission_role_stock_keeper = BasePermission(RoleNeed('库管'))
permission_role_accountant = BasePermission(RoleNeed('财务'))
permission_role_purchaser = BasePermission(RoleNeed('采购'))

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

permission_customer_section_add = BasePermission(CustomerSectionNeed('add'))
permission_customer_section_search = BasePermission(CustomerSectionNeed('search'))
permission_customer_section_export = BasePermission(CustomerSectionNeed('export'))
permission_customer_section_stats = BasePermission(CustomerSectionNeed('stats'))

# -------------------------------------------------------------
# 渠道板块操作权限（创建、查询、导出、统计）
SupplierSectionNeed = partial(SectionActionNeed, 'supplier')
SupplierSectionNeed.__doc__ = """A need with the section preset to `"supplier"`."""

permission_supplier_section_add = BasePermission(SupplierSectionNeed('add'))
permission_supplier_section_search = BasePermission(SupplierSectionNeed('search'))
permission_supplier_section_export = BasePermission(SupplierSectionNeed('export'))
permission_supplier_section_stats = BasePermission(SupplierSectionNeed('stats'))

# -------------------------------------------------------------
# 用户板块操作权限（创建、查询、导出、统计）
UserSectionNeed = partial(SectionActionNeed, 'user')
UserSectionNeed.__doc__ = """A need with the section preset to `"user"`."""

permission_user_section_add = BasePermission(UserSectionNeed('add'))
permission_user_section_search = BasePermission(UserSectionNeed('search'))
permission_user_section_export = BasePermission(UserSectionNeed('export'))
permission_user_section_stats = BasePermission(UserSectionNeed('stats'))

# -------------------------------------------------------------
# 产品板块操作权限（创建、查询、导出、统计）
ProductionSectionNeed = partial(SectionActionNeed, 'production')
ProductionSectionNeed.__doc__ = """A need with the section preset to `"production"`."""

permission_production_section_add = BasePermission(ProductionSectionNeed('add'))
permission_production_section_search = BasePermission(ProductionSectionNeed('search'))
permission_production_section_export = BasePermission(ProductionSectionNeed('export'))
permission_production_section_stats = BasePermission(ProductionSectionNeed('stats'))

# -------------------------------------------------------------
# 仓库板块操作权限（创建、查询、导出、统计）
WarehouseSectionNeed = partial(SectionActionNeed, 'warehouse')
WarehouseSectionNeed.__doc__ = """A need with the section preset to `"warehouse"`."""

permission_warehouse_section_add = BasePermission(WarehouseSectionNeed('add'))
permission_warehouse_section_search = BasePermission(WarehouseSectionNeed('search'))
permission_warehouse_section_export = BasePermission(WarehouseSectionNeed('export'))
permission_warehouse_section_stats = BasePermission(WarehouseSectionNeed('stats'))

# -------------------------------------------------------------
# 货架板块操作权限（创建、查询、导出、统计）
RackSectionNeed = partial(SectionActionNeed, 'rack')
RackSectionNeed.__doc__ = """A need with the section preset to `"rack"`."""

permission_rack_section_add = BasePermission(RackSectionNeed('add'))
permission_rack_section_search = BasePermission(RackSectionNeed('search'))
permission_rack_section_export = BasePermission(RackSectionNeed('export'))
permission_rack_section_stats = BasePermission(RackSectionNeed('stats'))

# -------------------------------------------------------------
# 库存板块操作权限（创建、查询、导出、统计）
InventorySectionNeed = partial(SectionActionNeed, 'inventory')
InventorySectionNeed.__doc__ = """A need with the section preset to `"inventory"`."""

permission_inventory_section_add = BasePermission(InventorySectionNeed('add'))
permission_inventory_section_search = BasePermission(InventorySectionNeed('search'))
permission_inventory_section_export = BasePermission(InventorySectionNeed('export'))
permission_inventory_section_stats = BasePermission(InventorySectionNeed('stats'))

# -------------------------------------------------------------
# 报价板块操作权限（创建、查询、导出、统计）
QuotationSectionNeed = partial(SectionActionNeed, 'quotation')
QuotationSectionNeed.__doc__ = """A need with the section preset to `"quotation"`."""

permission_quotation_section_add = BasePermission(QuotationSectionNeed('add'))
permission_quotation_section_search = BasePermission(QuotationSectionNeed('search'))
permission_quotation_section_export = BasePermission(QuotationSectionNeed('export'))
permission_quotation_section_stats = BasePermission(QuotationSectionNeed('stats'))

# -------------------------------------------------------------
# 询价板块操作权限（创建、查询、导出、统计）
EnquirySectionNeed = partial(SectionActionNeed, 'enquiry')
EnquirySectionNeed.__doc__ = """A need with the section preset to `"enquiry"`."""

permission_enquiry_section_add = BasePermission(EnquirySectionNeed('add'))
permission_enquiry_section_search = BasePermission(EnquirySectionNeed('search'))
permission_enquiry_section_export = BasePermission(EnquirySectionNeed('export'))
permission_enquiry_section_stats = BasePermission(EnquirySectionNeed('stats'))

# -------------------------------------------------------------
# 销售订单板块操作权限（创建、查询、导出、统计）
SalesOrdersSectionNeed = partial(SectionActionNeed, 'sales_orders')
SalesOrdersSectionNeed.__doc__ = """A need with the section preset to `"sales_orders"`."""

permission_sales_orders_section_add = BasePermission(SalesOrdersSectionNeed('add'))
permission_sales_orders_section_search = BasePermission(SalesOrdersSectionNeed('search'))
permission_sales_orders_section_export = BasePermission(SalesOrdersSectionNeed('export'))
permission_sales_orders_section_stats = BasePermission(SalesOrdersSectionNeed('stats'))

# -------------------------------------------------------------
# 销售出货板块操作权限（创建、查询、导出、统计）
DeliverySectionNeed = partial(SectionActionNeed, 'delivery')
DeliverySectionNeed.__doc__ = """A need with the section preset to `"delivery"`."""

permission_delivery_section_add = BasePermission(DeliverySectionNeed('add'))
permission_delivery_section_search = BasePermission(DeliverySectionNeed('search'))
permission_delivery_section_export = BasePermission(DeliverySectionNeed('export'))
permission_delivery_section_stats = BasePermission(DeliverySectionNeed('stats'))

# -------------------------------------------------------------
# 采购订单板块操作权限（创建、查询、导出、统计）
BuyerOrdersSectionNeed = partial(SectionActionNeed, 'buyer_orders')
BuyerOrdersSectionNeed.__doc__ = """A need with the section preset to `"buyer_orders"`."""

permission_buyer_orders_section_add = BasePermission(BuyerOrdersSectionNeed('add'))
permission_buyer_orders_section_search = BasePermission(BuyerOrdersSectionNeed('search'))
permission_buyer_orders_section_export = BasePermission(BuyerOrdersSectionNeed('export'))
permission_buyer_orders_section_stats = BasePermission(BuyerOrdersSectionNeed('stats'))

# -------------------------------------------------------------
# 采购进货板块操作权限（创建、查询、导出、统计）
PurchaseSectionNeed = partial(SectionActionNeed, 'purchase')
PurchaseSectionNeed.__doc__ = """A need with the section preset to `"purchase"`."""

permission_purchase_section_add = BasePermission(PurchaseSectionNeed('add'))
permission_purchase_section_search = BasePermission(PurchaseSectionNeed('search'))
permission_purchase_section_export = BasePermission(PurchaseSectionNeed('export'))
permission_purchase_section_stats = BasePermission(PurchaseSectionNeed('stats'))

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


# -------------------------------------------------------------
# 渠道明细操作权限(读取、更新、删除、打印)
SupplierItemNeed = partial(SectionActionItemNeed, 'supplier')
SupplierItemNeed.__doc__ = """A need with the section preset to `"supplier"`."""

SupplierItemGetNeed = partial(SupplierItemNeed, 'get')
SupplierItemEditNeed = partial(SupplierItemNeed, 'edit')
SupplierItemDelNeed = partial(SupplierItemNeed, 'del')
SupplierItemPrintNeed = partial(SupplierItemNeed, 'print')


class SupplierItemGetPermission(BasePermission):
    def __init__(self, supplier_id):
        need = SupplierItemGetNeed(six.text_type(supplier_id))
        super(SupplierItemGetPermission, self).__init__(need)


class SupplierItemEditPermission(BasePermission):
    def __init__(self, supplier_id):
        need = SupplierItemEditNeed(six.text_type(supplier_id))
        super(SupplierItemEditPermission, self).__init__(need)


class SupplierItemDelPermission(BasePermission):
    def __init__(self, supplier_id):
        need = SupplierItemDelNeed(six.text_type(supplier_id))
        super(SupplierItemDelPermission, self).__init__(need)


class SupplierItemPrintPermission(BasePermission):
    def __init__(self, supplier_id):
        need = SupplierItemPrintNeed(six.text_type(supplier_id))
        super(SupplierItemPrintPermission, self).__init__(need)


# -------------------------------------------------------------
# 用户明细操作权限(读取、更新、删除、打印)
UserItemNeed = partial(SectionActionItemNeed, 'user')
UserItemNeed.__doc__ = """A need with the section preset to `"user"`."""

UserItemGetNeed = partial(UserItemNeed, 'get')
UserItemEditNeed = partial(UserItemNeed, 'edit')
UserItemDelNeed = partial(UserItemNeed, 'del')
UserItemPrintNeed = partial(UserItemNeed, 'print')


class UserItemGetPermission(BasePermission):
    def __init__(self, user_id):
        need = UserItemGetNeed(six.text_type(user_id))
        super(UserItemGetPermission, self).__init__(need)


class UserItemEditPermission(BasePermission):
    def __init__(self, user_id):
        need = UserItemEditNeed(six.text_type(user_id))
        super(UserItemEditPermission, self).__init__(need)


class UserItemDelPermission(BasePermission):
    def __init__(self, user_id):
        need = UserItemDelNeed(six.text_type(user_id))
        super(UserItemDelPermission, self).__init__(need)


class UserItemPrintPermission(BasePermission):
    def __init__(self, user_id):
        need = UserItemPrintNeed(six.text_type(user_id))
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
# class ProductionItemGetPermission(BasePermission):
#     def __init__(self, production_id):
#         need = ProductionItemGetNeed(six.text_type(production_id))
#         super(ProductionItemGetPermission, self).__init__(need)
#
#
# class ProductionItemEditPermission(BasePermission):
#     def __init__(self, production_id):
#         need = ProductionItemEditNeed(six.text_type(production_id))
#         super(ProductionItemEditPermission, self).__init__(need)
#
#
# class ProductionItemDelPermission(BasePermission):
#     def __init__(self, production_id):
#         need = ProductionItemDelNeed(six.text_type(production_id))
#         super(ProductionItemDelPermission, self).__init__(need)
#
#
# class ProductionItemPrintPermission(BasePermission):
#     def __init__(self, production_id):
#         need = ProductionItemPrintNeed(six.text_type(production_id))
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


# -------------------------------------------------------------
# 销售订单明细操作权限（读取、更新、删除、打印、审核）
SalesOrdersItemNeed = partial(SectionActionItemNeed, 'sales_orders')
SalesOrdersItemNeed.__doc__ = """A need with the section preset to `"sales_orders"`."""

SalesOrdersItemGetNeed = partial(SalesOrdersItemNeed, 'get')
SalesOrdersItemEditNeed = partial(SalesOrdersItemNeed, 'edit')
SalesOrdersItemDelNeed = partial(SalesOrdersItemNeed, 'del')
SalesOrdersItemPrintNeed = partial(SalesOrdersItemNeed, 'print')
SalesOrdersItemAuditNeed = partial(SalesOrdersItemNeed, 'audit')


class SalesOrdersItemGetPermission(BasePermission):
    def __init__(self, order_id):
        need = SalesOrdersItemGetNeed(six.text_type(order_id))
        super(SalesOrdersItemGetPermission, self).__init__(need)


class SalesOrdersItemEditPermission(BasePermission):
    def __init__(self, order_id):
        need = SalesOrdersItemEditNeed(six.text_type(order_id))
        super(SalesOrdersItemEditPermission, self).__init__(need)


class SalesOrdersItemDelPermission(BasePermission):
    def __init__(self, order_id):
        need = SalesOrdersItemDelNeed(six.text_type(order_id))
        super(SalesOrdersItemDelPermission, self).__init__(need)


class SalesOrdersItemPrintPermission(BasePermission):
    def __init__(self, order_id):
        need = SalesOrdersItemPrintNeed(six.text_type(order_id))
        super(SalesOrdersItemPrintPermission, self).__init__(need)


class SalesOrdersItemAuditPermission(BasePermission):
    def __init__(self, order_id):
        need = SalesOrdersItemAuditNeed(six.text_type(order_id))
        super(SalesOrdersItemAuditPermission, self).__init__(need)


# -------------------------------------------------------------
# 销售出货明细操作权限（读取、更新、删除、打印、审核）
DeliveryItemNeed = partial(SectionActionItemNeed, 'delivery')
DeliveryItemNeed.__doc__ = """A need with the section preset to `"delivery"`."""

DeliveryItemGetNeed = partial(DeliveryItemNeed, 'get')
DeliveryItemEditNeed = partial(DeliveryItemNeed, 'edit')
DeliveryItemDelNeed = partial(DeliveryItemNeed, 'del')
DeliveryItemPrintNeed = partial(DeliveryItemNeed, 'print')
DeliveryItemAuditNeed = partial(DeliveryItemNeed, 'audit')


class DeliveryItemGetPermission(BasePermission):
    def __init__(self, sales_delivery_id):
        need = DeliveryItemGetNeed(six.text_type(sales_delivery_id))
        super(DeliveryItemGetPermission, self).__init__(need)


class DeliveryItemEditPermission(BasePermission):
    def __init__(self, sales_delivery_id):
        need = DeliveryItemEditNeed(six.text_type(sales_delivery_id))
        super(DeliveryItemEditPermission, self).__init__(need)


class DeliveryItemDelPermission(BasePermission):
    def __init__(self, sales_delivery_id):
        need = DeliveryItemDelNeed(six.text_type(sales_delivery_id))
        super(DeliveryItemDelPermission, self).__init__(need)


class DeliveryItemPrintPermission(BasePermission):
    def __init__(self, sales_delivery_id):
        need = DeliveryItemPrintNeed(six.text_type(sales_delivery_id))
        super(DeliveryItemPrintPermission, self).__init__(need)


class DeliveryItemAuditPermission(BasePermission):
    def __init__(self, sales_delivery_id):
        need = DeliveryItemAuditNeed(six.text_type(sales_delivery_id))
        super(DeliveryItemAuditPermission, self).__init__(need)


# -------------------------------------------------------------
# 采购订单明细操作权限（读取、更新、删除、打印、审核）
BuyerOrdersItemNeed = partial(SectionActionItemNeed, 'buyer_orders')
BuyerOrdersItemNeed.__doc__ = """A need with the section preset to `"buyer_orders"`."""

BuyerOrdersItemGetNeed = partial(BuyerOrdersItemNeed, 'get')
BuyerOrdersItemEditNeed = partial(BuyerOrdersItemNeed, 'edit')
BuyerOrdersItemDelNeed = partial(BuyerOrdersItemNeed, 'del')
BuyerOrdersItemPrintNeed = partial(BuyerOrdersItemNeed, 'print')
BuyerOrdersItemAuditNeed = partial(BuyerOrdersItemNeed, 'audit')


class BuyerOrdersItemGetPermission(BasePermission):
    def __init__(self, order_id):
        need = BuyerOrdersItemGetNeed(six.text_type(order_id))
        super(BuyerOrdersItemGetPermission, self).__init__(need)


class BuyerOrdersItemEditPermission(BasePermission):
    def __init__(self, order_id):
        need = BuyerOrdersItemEditNeed(six.text_type(order_id))
        super(BuyerOrdersItemEditPermission, self).__init__(need)


class BuyerOrderItemDelPermission(BasePermission):
    def __init__(self, order_id):
        need = BuyerOrdersItemDelNeed(six.text_type(order_id))
        super(BuyerOrderItemDelPermission, self).__init__(need)


class BuyerOrdersItemPrintPermission(BasePermission):
    def __init__(self, order_id):
        need = BuyerOrdersItemPrintNeed(six.text_type(order_id))
        super(BuyerOrdersItemPrintPermission, self).__init__(need)


class BuyerOrdersItemAuditPermission(BasePermission):
    def __init__(self, order_id):
        need = BuyerOrdersItemAuditNeed(six.text_type(order_id))
        super(BuyerOrdersItemAuditPermission, self).__init__(need)


# -------------------------------------------------------------
# 采购进货明细操作权限（读取、更新、删除、打印、审核）
PurchaseItemNeed = partial(SectionActionItemNeed, 'purchase')
PurchaseItemNeed.__doc__ = """A need with the section preset to `"purchase"`."""

PurchaseItemGetNeed = partial(PurchaseItemNeed, 'get')
PurchaseItemEditNeed = partial(PurchaseItemNeed, 'edit')
PurchaseItemDelNeed = partial(PurchaseItemNeed, 'del')
PurchaseItemPrintNeed = partial(PurchaseItemNeed, 'print')
PurchaseItemAuditNeed = partial(PurchaseItemNeed, 'audit')


class PurchaseItemGetPermission(BasePermission):
    def __init__(self, buyer_purchase_id):
        need = PurchaseItemGetNeed(six.text_type(buyer_purchase_id))
        super(PurchaseItemGetPermission, self).__init__(need)


class PurchaseItemEditPermission(BasePermission):
    def __init__(self, buyer_purchase_id):
        need = PurchaseItemEditNeed(six.text_type(buyer_purchase_id))
        super(PurchaseItemEditPermission, self).__init__(need)


class PurchaseItemDelPermission(BasePermission):
    def __init__(self, buyer_purchase_id):
        need = PurchaseItemDelNeed(six.text_type(buyer_purchase_id))
        super(PurchaseItemDelPermission, self).__init__(need)


class PurchaseItemPrintPermission(BasePermission):
    def __init__(self, buyer_purchase_id):
        need = PurchaseItemPrintNeed(six.text_type(buyer_purchase_id))
        super(PurchaseItemPrintPermission, self).__init__(need)


class PurchaseItemAuditPermission(BasePermission):
    def __init__(self, buyer_purchase_id):
        need = PurchaseItemAuditNeed(six.text_type(buyer_purchase_id))
        super(PurchaseItemAuditPermission, self).__init__(need)
