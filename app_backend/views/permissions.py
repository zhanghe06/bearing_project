#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: permissions.py
@time: 2019-03-29 01:12
"""

from flask import Blueprint
from flask_principal import IdentityContext

from app_backend.permissions import (
    permission_role_administrator,
    permission_role_default,
    permission_role_sales,
    permission_role_manager,
    permission_role_stock_keeper,
    permission_role_accountant,
    permission_role_purchaser,
)

from app_backend.permissions.production import (
    permission_production_section,
    permission_production_section_add,
    permission_production_section_search,
    permission_production_section_stats,
    permission_production_section_export,
    permission_production_section_get,
    permission_production_section_edit,
    permission_production_section_del,
    permission_production_section_audit,
    permission_production_section_print,
)

from app_backend.permissions.user import (
    permission_user_section,
    permission_user_section_add,
    permission_user_section_search,
    permission_user_section_stats,
    permission_user_section_export,
    permission_user_section_get,
    permission_user_section_edit,
    permission_user_section_del,
    permission_user_section_audit,
    permission_user_section_print,
)

from app_backend.permissions.warehouse import (
    permission_warehouse_section,
    permission_warehouse_section_add,
    permission_warehouse_section_search,
    permission_warehouse_section_stats,
    permission_warehouse_section_export,
    permission_warehouse_section_get,
    permission_warehouse_section_edit,
    permission_warehouse_section_del,
    permission_warehouse_section_audit,
    permission_warehouse_section_print,
)

from app_backend.permissions.rack import (
    permission_rack_section,
    permission_rack_section_add,
    permission_rack_section_search,
    permission_rack_section_stats,
    permission_rack_section_export,
    permission_rack_section_get,
    permission_rack_section_edit,
    permission_rack_section_del,
    permission_rack_section_audit,
    permission_rack_section_print,
)

from app_backend.permissions.futures import (
    permission_futures_section,
    permission_futures_section_add,
    permission_futures_section_search,
    permission_futures_section_stats,
    permission_futures_section_export,
    permission_futures_section_get,
    permission_futures_section_edit,
    permission_futures_section_del,
    permission_futures_section_audit,
    permission_futures_section_print,
)

from app_backend.permissions.inventory import (
    permission_inventory_section,
    permission_inventory_section_add,
    permission_inventory_section_search,
    permission_inventory_section_stats,
    permission_inventory_section_export,
    permission_inventory_section_get,
    permission_inventory_section_edit,
    permission_inventory_section_del,
    permission_inventory_section_audit,
    permission_inventory_section_print,
)

from app_backend.permissions.supplier import (
    permission_supplier_section,
    permission_supplier_section_add,
    permission_supplier_section_search,
    permission_supplier_section_stats,
    permission_supplier_section_export,
    permission_supplier_section_get,
    permission_supplier_section_edit,
    permission_supplier_section_del,
    permission_supplier_section_audit,
    permission_supplier_section_print,
)

from app_backend.permissions.customer import (
    permission_customer_section,
    permission_customer_section_add,
    permission_customer_section_search,
    permission_customer_section_stats,
    permission_customer_section_export,
    permission_customer_section_get,
    permission_customer_section_edit,
    permission_customer_section_del,
    permission_customer_section_audit,
    permission_customer_section_print,
)

from app_backend.permissions.enquiry import (
    permission_enquiry_section,
    permission_enquiry_section_add,
    permission_enquiry_section_search,
    permission_enquiry_section_stats,
    permission_enquiry_section_export,
    permission_enquiry_section_get,
    permission_enquiry_section_edit,
    permission_enquiry_section_del,
    permission_enquiry_section_audit,
    permission_enquiry_section_print,
)

from app_backend.permissions.quotation import (
    permission_quotation_section,
    permission_quotation_section_add,
    permission_quotation_section_search,
    permission_quotation_section_stats,
    permission_quotation_section_export,
    permission_quotation_section_get,
    permission_quotation_section_edit,
    permission_quotation_section_del,
    permission_quotation_section_audit,
    permission_quotation_section_print,
)

from app_backend.permissions.buyer_order import (
    permission_buyer_order_section,
    permission_buyer_order_section_add,
    permission_buyer_order_section_search,
    permission_buyer_order_section_stats,
    permission_buyer_order_section_export,
    permission_buyer_order_section_get,
    permission_buyer_order_section_edit,
    permission_buyer_order_section_del,
    permission_buyer_order_section_audit,
    permission_buyer_order_section_print,
)

from app_backend.permissions.sales_order import (
    permission_sales_order_section,
    permission_sales_order_section_add,
    permission_sales_order_section_search,
    permission_sales_order_section_stats,
    permission_sales_order_section_export,
    permission_sales_order_section_get,
    permission_sales_order_section_edit,
    permission_sales_order_section_del,
    permission_sales_order_section_audit,
    permission_sales_order_section_print,
)

from app_backend.permissions.buyer_purchase import (
    permission_purchase_section,
    permission_purchase_section_add,
    permission_purchase_section_search,
    permission_purchase_section_stats,
    permission_purchase_section_export,
    permission_purchase_section_get,
    permission_purchase_section_edit,
    permission_purchase_section_del,
    permission_purchase_section_audit,
    permission_purchase_section_print,
)

from app_backend.permissions.sales_delivery import (
    permission_delivery_section,
    permission_delivery_section_add,
    permission_delivery_section_search,
    permission_delivery_section_stats,
    permission_delivery_section_export,
    permission_delivery_section_get,
    permission_delivery_section_edit,
    permission_delivery_section_del,
    permission_delivery_section_audit,
    permission_delivery_section_print,
)

bp_permissions = Blueprint('permissions', __name__, )


# 上下文处理,可以在jinja2判断是否有执行权限
@bp_permissions.app_context_processor
def context():
    return dict(
        # 角色
        permission_role_default=IdentityContext(permission_role_default),
        permission_role_administrator=IdentityContext(permission_role_administrator),
        permission_role_sales=IdentityContext(permission_role_sales),
        permission_role_manager=IdentityContext(permission_role_manager),
        permission_role_stock_keeper=IdentityContext(permission_role_stock_keeper),
        permission_role_accountant=IdentityContext(permission_role_accountant),
        permission_role_purchaser=IdentityContext(permission_role_purchaser),

        # 产品
        permission_production_section=IdentityContext(permission_production_section),
        permission_production_section_add=IdentityContext(permission_production_section_add),
        permission_production_section_search=IdentityContext(permission_production_section_search),
        permission_production_section_stats=IdentityContext(permission_production_section_stats),
        permission_production_section_export=IdentityContext(permission_production_section_export),
        permission_production_section_get=IdentityContext(permission_production_section_get),
        permission_production_section_edit=IdentityContext(permission_production_section_edit),
        permission_production_section_del=IdentityContext(permission_production_section_del),
        permission_production_section_audit=IdentityContext(permission_production_section_audit),
        permission_production_section_print=IdentityContext(permission_production_section_print),

        # 用户
        permission_user_section=IdentityContext(permission_user_section),
        permission_user_section_add=IdentityContext(permission_user_section_add),
        permission_user_section_search=IdentityContext(permission_user_section_search),
        permission_user_section_stats=IdentityContext(permission_user_section_stats),
        permission_user_section_export=IdentityContext(permission_user_section_export),
        permission_user_section_get=IdentityContext(permission_user_section_get),
        permission_user_section_edit=IdentityContext(permission_user_section_edit),
        permission_user_section_del=IdentityContext(permission_user_section_del),
        permission_user_section_audit=IdentityContext(permission_user_section_audit),
        permission_user_section_print=IdentityContext(permission_user_section_print),

        # 仓库
        permission_warehouse_section=IdentityContext(permission_warehouse_section),
        permission_warehouse_section_add=IdentityContext(permission_warehouse_section_add),
        permission_warehouse_section_search=IdentityContext(permission_warehouse_section_search),
        permission_warehouse_section_stats=IdentityContext(permission_warehouse_section_stats),
        permission_warehouse_section_export=IdentityContext(permission_warehouse_section_export),
        permission_warehouse_section_get=IdentityContext(permission_warehouse_section_get),
        permission_warehouse_section_edit=IdentityContext(permission_warehouse_section_edit),
        permission_warehouse_section_del=IdentityContext(permission_warehouse_section_del),
        permission_warehouse_section_audit=IdentityContext(permission_warehouse_section_audit),
        permission_warehouse_section_print=IdentityContext(permission_warehouse_section_print),

        # 货架
        permission_rack_section=IdentityContext(permission_rack_section),
        permission_rack_section_add=IdentityContext(permission_rack_section_add),
        permission_rack_section_search=IdentityContext(permission_rack_section_search),
        permission_rack_section_stats=IdentityContext(permission_rack_section_stats),
        permission_rack_section_export=IdentityContext(permission_rack_section_export),
        permission_rack_section_get=IdentityContext(permission_rack_section_get),
        permission_rack_section_edit=IdentityContext(permission_rack_section_edit),
        permission_rack_section_del=IdentityContext(permission_rack_section_del),
        permission_rack_section_audit=IdentityContext(permission_rack_section_audit),
        permission_rack_section_print=IdentityContext(permission_rack_section_print),

        # 期货
        permission_futures_section=IdentityContext(permission_futures_section),
        permission_futures_section_add=IdentityContext(permission_futures_section_add),
        permission_futures_section_search=IdentityContext(permission_futures_section_search),
        permission_futures_section_stats=IdentityContext(permission_futures_section_stats),
        permission_futures_section_export=IdentityContext(permission_futures_section_export),
        permission_futures_section_get=IdentityContext(permission_futures_section_get),
        permission_futures_section_edit=IdentityContext(permission_futures_section_edit),
        permission_futures_section_del=IdentityContext(permission_futures_section_del),
        permission_futures_section_audit=IdentityContext(permission_futures_section_audit),
        permission_futures_section_print=IdentityContext(permission_futures_section_print),

        # 库存
        permission_inventory_section=IdentityContext(permission_inventory_section),
        permission_inventory_section_add=IdentityContext(permission_inventory_section_add),
        permission_inventory_section_search=IdentityContext(permission_inventory_section_search),
        permission_inventory_section_stats=IdentityContext(permission_inventory_section_stats),
        permission_inventory_section_export=IdentityContext(permission_inventory_section_export),
        permission_inventory_section_get=IdentityContext(permission_inventory_section_get),
        permission_inventory_section_edit=IdentityContext(permission_inventory_section_edit),
        permission_inventory_section_del=IdentityContext(permission_inventory_section_del),
        permission_inventory_section_audit=IdentityContext(permission_inventory_section_audit),
        permission_inventory_section_print=IdentityContext(permission_inventory_section_print),

        # 渠道
        permission_supplier_section=IdentityContext(permission_supplier_section),
        permission_supplier_section_add=IdentityContext(permission_supplier_section_add),
        permission_supplier_section_search=IdentityContext(permission_supplier_section_search),
        permission_supplier_section_stats=IdentityContext(permission_supplier_section_stats),
        permission_supplier_section_export=IdentityContext(permission_supplier_section_export),
        permission_supplier_section_get=IdentityContext(permission_supplier_section_get),
        permission_supplier_section_edit=IdentityContext(permission_supplier_section_edit),
        permission_supplier_section_del=IdentityContext(permission_supplier_section_del),
        permission_supplier_section_audit=IdentityContext(permission_supplier_section_audit),
        permission_supplier_section_print=IdentityContext(permission_supplier_section_print),

        # 客户
        permission_customer_section=IdentityContext(permission_customer_section),
        permission_customer_section_add=IdentityContext(permission_customer_section_add),
        permission_customer_section_search=IdentityContext(permission_customer_section_search),
        permission_customer_section_stats=IdentityContext(permission_customer_section_stats),
        permission_customer_section_export=IdentityContext(permission_customer_section_export),
        permission_customer_section_get=IdentityContext(permission_customer_section_get),
        permission_customer_section_edit=IdentityContext(permission_customer_section_edit),
        permission_customer_section_del=IdentityContext(permission_customer_section_del),
        permission_customer_section_audit=IdentityContext(permission_customer_section_audit),
        permission_customer_section_print=IdentityContext(permission_customer_section_print),

        # 询价
        permission_enquiry_section=IdentityContext(permission_enquiry_section),
        permission_enquiry_section_add=IdentityContext(permission_enquiry_section_add),
        permission_enquiry_section_search=IdentityContext(permission_enquiry_section_search),
        permission_enquiry_section_stats=IdentityContext(permission_enquiry_section_stats),
        permission_enquiry_section_export=IdentityContext(permission_enquiry_section_export),
        permission_enquiry_section_get=IdentityContext(permission_enquiry_section_get),
        permission_enquiry_section_edit=IdentityContext(permission_enquiry_section_edit),
        permission_enquiry_section_del=IdentityContext(permission_enquiry_section_del),
        permission_enquiry_section_audit=IdentityContext(permission_enquiry_section_audit),
        permission_enquiry_section_print=IdentityContext(permission_enquiry_section_print),

        # 报价
        permission_quotation_section=IdentityContext(permission_quotation_section),
        permission_quotation_section_add=IdentityContext(permission_quotation_section_add),
        permission_quotation_section_search=IdentityContext(permission_quotation_section_search),
        permission_quotation_section_stats=IdentityContext(permission_quotation_section_stats),
        permission_quotation_section_export=IdentityContext(permission_quotation_section_export),
        permission_quotation_section_get=IdentityContext(permission_quotation_section_get),
        permission_quotation_section_edit=IdentityContext(permission_quotation_section_edit),
        permission_quotation_section_del=IdentityContext(permission_quotation_section_del),
        permission_quotation_section_audit=IdentityContext(permission_quotation_section_audit),
        permission_quotation_section_print=IdentityContext(permission_quotation_section_print),

        # 采购订单
        permission_buyer_order_section=IdentityContext(permission_buyer_order_section),
        permission_buyer_order_section_add=IdentityContext(permission_buyer_order_section_add),
        permission_buyer_order_section_search=IdentityContext(permission_buyer_order_section_search),
        permission_buyer_order_section_stats=IdentityContext(permission_buyer_order_section_stats),
        permission_buyer_order_section_export=IdentityContext(permission_buyer_order_section_export),
        permission_buyer_order_section_get=IdentityContext(permission_buyer_order_section_get),
        permission_buyer_order_section_edit=IdentityContext(permission_buyer_order_section_edit),
        permission_buyer_order_section_del=IdentityContext(permission_buyer_order_section_del),
        permission_buyer_order_section_audit=IdentityContext(permission_buyer_order_section_audit),
        permission_buyer_order_section_print=IdentityContext(permission_buyer_order_section_print),

        # 销售订单
        permission_sales_order_section=IdentityContext(permission_sales_order_section),
        permission_sales_order_section_add=IdentityContext(permission_sales_order_section_add),
        permission_sales_order_section_search=IdentityContext(permission_sales_order_section_search),
        permission_sales_order_section_stats=IdentityContext(permission_sales_order_section_stats),
        permission_sales_order_section_export=IdentityContext(permission_sales_order_section_export),
        permission_sales_order_section_get=IdentityContext(permission_sales_order_section_get),
        permission_sales_order_section_edit=IdentityContext(permission_sales_order_section_edit),
        permission_sales_order_section_del=IdentityContext(permission_sales_order_section_del),
        permission_sales_order_section_audit=IdentityContext(permission_sales_order_section_audit),
        permission_sales_order_section_print=IdentityContext(permission_sales_order_section_print),

        # 采购进货
        permission_purchase_section=IdentityContext(permission_purchase_section),
        permission_purchase_section_add=IdentityContext(permission_purchase_section_add),
        permission_purchase_section_search=IdentityContext(permission_purchase_section_search),
        permission_purchase_section_stats=IdentityContext(permission_purchase_section_stats),
        permission_purchase_section_export=IdentityContext(permission_purchase_section_export),
        permission_purchase_section_get=IdentityContext(permission_purchase_section_get),
        permission_purchase_section_edit=IdentityContext(permission_purchase_section_edit),
        permission_purchase_section_del=IdentityContext(permission_purchase_section_del),
        permission_purchase_section_audit=IdentityContext(permission_purchase_section_audit),
        permission_purchase_section_print=IdentityContext(permission_purchase_section_print),

        # 销售出货
        permission_delivery_section=IdentityContext(permission_delivery_section),
        permission_delivery_section_add=IdentityContext(permission_delivery_section_add),
        permission_delivery_section_search=IdentityContext(permission_delivery_section_search),
        permission_delivery_section_stats=IdentityContext(permission_delivery_section_stats),
        permission_delivery_section_export=IdentityContext(permission_delivery_section_export),
        permission_delivery_section_get=IdentityContext(permission_delivery_section_get),
        permission_delivery_section_edit=IdentityContext(permission_delivery_section_edit),
        permission_delivery_section_del=IdentityContext(permission_delivery_section_del),
        permission_delivery_section_audit=IdentityContext(permission_delivery_section_audit),
        permission_delivery_section_print=IdentityContext(permission_delivery_section_print),
    )
