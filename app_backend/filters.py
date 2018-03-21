#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: filters.py
@time: 2018-03-06 00:18
"""

from __future__ import unicode_literals

from app_backend import app
from app_backend.api.user import get_user_row_by_id
from app_common.maps.type_auth import TYPE_AUTH_DICT
from app_common.maps.type_company import TYPE_COMPANY_DICT
from app_common.maps.type_role import TYPE_ROLE_DICT


@app.template_filter('user_name')
def filter_user_name(user_id):
    """
    用户姓名
    :param user_id:
    :return:
    """
    user_info = get_user_row_by_id(user_id)
    return user_info.name if user_info else '不明身份'


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
