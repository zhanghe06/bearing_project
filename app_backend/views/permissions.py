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

bp_permissions = Blueprint('permissions', __name__, )


# 上下文处理,可以在jinja2判断是否有执行权限
@bp_permissions.app_context_processor
def context():
    return dict(
        permission_role_default=IdentityContext(permission_role_default),
        permission_role_administrator=IdentityContext(permission_role_administrator),
        permission_role_sales=IdentityContext(permission_role_sales),
        permission_role_manager=IdentityContext(permission_role_manager),
        permission_role_stock_keeper=IdentityContext(permission_role_stock_keeper),
        permission_role_accountant=IdentityContext(permission_role_accountant),
        permission_role_purchaser=IdentityContext(permission_role_purchaser),
    )
