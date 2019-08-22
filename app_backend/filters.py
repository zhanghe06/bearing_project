#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: filters.py
@time: 2018-03-06 00:18
"""

from __future__ import unicode_literals

import json

from app_backend import app
from app_backend.api.customer import get_customer_row_by_id, count_customer
from app_backend.api.customer_contact import get_customer_contact_row_by_id
from app_backend.api.delivery import get_delivery_row_by_id
from app_backend.api.enquiry import get_enquiry_row_by_id
from app_backend.api.purchase import get_purchase_row_by_id
from app_backend.api.quotation import get_quotation_row_by_id, count_quotation
from app_backend.api.supplier import get_supplier_row_by_id
from app_backend.api.supplier_contact import get_supplier_contact_row_by_id
from app_backend.api.user import get_user_row_by_id
from app_backend.api.warehouse import get_warehouse_row_by_id
from app_backend.api.rack import get_rack_row_by_id
from app_backend.api.production import get_production_row_by_id
from app_backend.api.production_sensitive import get_production_sensitive_row
from app_backend.api.sales_order import count_sales_order
from app_backend.models.bearing_project import Customer, Quotation, SalesOrder
from app_common.maps.status_default import STATUS_DEFAULT_DICT
from app_common.maps.status_delete import STATUS_DEL_NO
from app_common.maps.type_auth import TYPE_AUTH_DICT
from app_common.maps.type_company import TYPE_COMPANY_DICT
from app_common.maps.type_role import TYPE_ROLE_DICT
from app_common.maps.type_tax import TYPE_TAX_DICT, TYPE_TAX_HTML_CLASS_DICT
from app_common.maps.status_audit import STATUS_AUDIT_DICT, STATUS_AUDIT_HTML_CLASS_DICT
from app_common.maps.status_order import STATUS_ORDER_DICT
from app_backend.clients.client_redis import redis_client


@app.template_filter('status_online')
def filter_status_online(user_id):
    """
    在线状态
    :param user_id:
    :return:
    """
    if not user_id:
        return False
    session_keys = redis_client.keys('%s*' % app.config['REDIS_SESSION_PREFIX_BACKEND'])
    if not session_keys:
        return False
    user_ids = [int(json.loads(s_k).get('user_id', 0)) for s_k in redis_client.mget(session_keys)]
    if user_id in user_ids:
        return True
    return False


@app.template_filter('user_name')
def filter_user_name(user_id):
    """
    用户姓名
    :param user_id:
    :return:
    """
    user_info = get_user_row_by_id(user_id)
    return user_info.name if user_info else '-'


@app.template_filter('customer_company_name')
def filter_customer_company_name(customer_id, default='-'):
    """
    客户公司名称
    :param customer_id:
    :param default:
    :return:
    """
    if not customer_id:
        return default
    customer_info = get_customer_row_by_id(customer_id)
    return customer_info.company_name if customer_info else default


@app.template_filter('customer_contact_name')
def filter_customer_contact_name(contact_id, default='-'):
    """
    客户联系人员
    :param contact_id:
    :param default:
    :return:
    """
    if not contact_id:
        return default
    customer_contact_info = get_customer_contact_row_by_id(contact_id)
    return customer_contact_info.name if customer_contact_info else default


@app.template_filter('supplier_company_name')
def filter_supplier_company_name(supplier_id, default='-'):
    """
    渠道公司名称
    :param supplier_id:
    :param default:
    :return:
    """
    if not supplier_id:
        return default
    supplier_info = get_supplier_row_by_id(supplier_id)
    return supplier_info.company_name if supplier_info else default


@app.template_filter('supplier_contact_name')
def filter_supplier_contact_name(contact_id, default='-'):
    """
    渠道联系人员
    :param contact_id:
    :param default:
    :return:
    """
    if not contact_id:
        return default
    supplier_contact_info = get_supplier_contact_row_by_id(contact_id)
    return supplier_contact_info.name if supplier_contact_info else default


@app.template_filter('warehouse_name')
def filter_warehouse_name(warehouse_id):
    """
    仓库名称
    :param warehouse_id:
    :return:
    """
    warehouse_info = get_warehouse_row_by_id(warehouse_id)
    return warehouse_info.name if warehouse_info else '-'


@app.template_filter('rack_name')
def filter_rack_name(rack_id):
    """
    货架名称
    :param rack_id:
    :return:
    """
    rack_info = get_rack_row_by_id(rack_id)
    return rack_info.name if rack_info else '-'


@app.template_filter('production_brand')
def filter_production_brand(production_id):
    """
    产品品牌
    :param production_id:
    :return:
    """
    production_info = get_production_row_by_id(production_id)
    return production_info.production_brand if production_info else '-'


@app.template_filter('production_model')
def filter_production_model(production_id):
    """
    产品型号
    :param production_id:
    :return:
    """
    production_info = get_production_row_by_id(production_id)
    return production_info.production_model if production_info else '-'


@app.template_filter('quotation_create_time')
def filter_quotation_create_time(quotation_id):
    """
    报价创建时间
    :param quotation_id:
    :return:
    """
    quotation_info = get_quotation_row_by_id(quotation_id)
    return quotation_info.create_time if quotation_info else None


@app.template_filter('enquiry_create_time')
def filter_enquiry_create_time(enquiry_id):
    """
    询价创建时间
    :param enquiry_id:
    :return:
    """
    enquiry_info = get_enquiry_row_by_id(enquiry_id)
    return enquiry_info.create_time if enquiry_info else None


@app.template_filter('delivery_create_time')
def filter_delivery_create_time(delivery_id):
    """
    销货创建时间
    :param delivery_id:
    :return:
    """
    delivery_info = get_delivery_row_by_id(delivery_id)
    return delivery_info.create_time if delivery_info else None


@app.template_filter('purchase_create_time')
def filter_purchase_create_time(purchase_id):
    """
    询价创建时间
    :param purchase_id:
    :return:
    """
    purchase_info = get_purchase_row_by_id(purchase_id)
    return purchase_info.create_time if purchase_info else None


@app.template_filter('type_auth')
def filter_type_auth(type_auth_id):
    """
    认证类型
    :param type_auth_id:
    :return:
    """
    return TYPE_AUTH_DICT.get(type_auth_id, '')


@app.template_filter('type_company')
def filter_type_company(type_company_id):
    """
    公司类型
    :param type_company_id:
    :return:
    """
    return TYPE_COMPANY_DICT.get(type_company_id, '')


@app.template_filter('type_role')
def filter_type_role(role_id):
    """
    角色类型
    :param role_id:
    :return:
    """
    return TYPE_ROLE_DICT.get(role_id, '')


@app.template_filter('type_tax')
def filter_type_tax(type_tax_id):
    """
    含税类型
    :param type_tax_id:
    :return:
    """
    return TYPE_TAX_DICT.get(type_tax_id, '')


@app.template_filter('type_tax_html_class')
def filter_type_tax_html_class(type_tax_id):
    """
    含税类型 - HTML显示
    :param type_tax_id:
    :return:
    """
    return TYPE_TAX_HTML_CLASS_DICT.get(type_tax_id, '')


@app.template_filter('status_audit')
def filter_status_audit(status_audit_id):
    """
    审核状态
    :param status_audit_id:
    :return:
    """
    return STATUS_AUDIT_DICT.get(status_audit_id, '')


@app.template_filter('status_audit_html_class')
def filter_status_audit_html_class(status_audit_id):
    """
    审核状态
    :param status_audit_id:
    :return:
    """
    return STATUS_AUDIT_HTML_CLASS_DICT.get(status_audit_id, '')


@app.template_filter('status_order')
def filter_status_order(status_order_id):
    """
    订单状态
    :param status_order_id:
    :return:
    """
    return STATUS_ORDER_DICT.get(status_order_id, '')


@app.template_filter('status_default')
def filter_status_default(status_default_id):
    """
    默认状态
    :param status_default_id:
    :return:
    """
    return STATUS_DEFAULT_DICT.get(status_default_id, '')


@app.template_filter('count_customer')
def filter_count_customer(user_id=None):
    """
    客户计数
    :param user_id:
    :return:
    """
    if not user_id:
        return 0
    count = count_customer(Customer.owner_uid == user_id)
    return count


@app.template_filter('count_quotation')
def filter_count_quotation(user_id=None):
    """
    报价计数
    :param user_id:
    :return:
    """
    if not user_id:
        return 0
    count = count_quotation(Quotation.uid == user_id)
    return count


@app.template_filter('count_transaction')
def filter_count_transaction(user_id=None):
    """
    成交计数
    :param user_id:
    :return:
    """
    if not user_id:
        return 0
    count = count_sales_order(SalesOrder.uid == user_id)
    return count


@app.template_filter('status_sensitive')
def filter_status_sensitive(production_id):
    """
    敏感状态
    :param production_id:
    :return:
    """
    if not production_id:
        return False
    condition = {
        'production_id': production_id,
        'status_delete': STATUS_DEL_NO
    }
    production_sensitive_info = get_production_sensitive_row(**condition)
    return True if production_sensitive_info else False
