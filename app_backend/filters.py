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
from app_backend.api.user import get_user_row_by_id
from app_backend.api.warehouse import get_warehouse_row_by_id
from app_backend.api.rack import get_rack_row_by_id
from app_backend.api.product import get_product_row_by_id
from app_common.maps.type_auth import TYPE_AUTH_DICT
from app_common.maps.type_company import TYPE_COMPANY_DICT
from app_common.maps.type_role import TYPE_ROLE_DICT
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


@app.template_filter('product_brand')
def filter_product_brand(product_id):
    """
    产品品牌
    :param product_id:
    :return:
    """
    product_info = get_product_row_by_id(product_id)
    return product_info.product_brand if product_info else '-'


@app.template_filter('product_model')
def filter_product_model(product_id):
    """
    产品型号
    :param product_id:
    :return:
    """
    product_info = get_product_row_by_id(product_id)
    return product_info.product_model if product_info else '-'


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
