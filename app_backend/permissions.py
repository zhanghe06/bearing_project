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

from flask_principal import Need, Permission, RoleNeed, TypeNeed, ActionNeed


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

# 版块权限(读取、创建、更新、删除)
permission_section_product = Permission(SectionNeed('产品'))
permission_section_customer = Permission(SectionNeed('客户'))
permission_section_quote = Permission(SectionNeed('报价'))
permission_section_stats = Permission(SectionNeed('统计'))
permission_section_user = Permission(SectionNeed('用户'))
permission_section_role = Permission(SectionNeed('角色'))
permission_section_sys = Permission(SectionNeed('系统'))


# -------------------------------------------------------------
# 操作类型
actions = [
    '读取',
    '修改',
    '删除',
    '导出',
    '打印',
]

# 操作权限
permission_action_read = Permission(ActionNeed('读取'))
permission_action_write = Permission(ActionNeed('修改'))
permission_action_delete = Permission(ActionNeed('删除'))
permission_action_export = Permission(ActionNeed('导出'))
permission_action_print = Permission(ActionNeed('打印'))


# =============================================================
# 因客户、报价有所有者，修改操作需要校验所有者身份，下面单独配置修改权限
# =============================================================


# -------------------------------------------------------------
# 客户修改权限(更新、删除)
CustomerNeed = namedtuple('customer', ['method', 'value'])
EditCustomerNeed = partial(CustomerNeed, 'edit')


class EditCustomerPermission(Permission):
    def __init__(self, customer_id):
        need = EditCustomerNeed(unicode(customer_id))
        super(EditCustomerPermission, self).__init__(need)


# -------------------------------------------------------------
# 报价修改权限(更新、删除)
QuoteNeed = namedtuple('quote', ['method', 'value'])
EditQuoteNeed = partial(QuoteNeed, 'edit')


class EditQuotePermission(Permission):
    def __init__(self, quote_id):
        need = EditQuoteNeed(unicode(quote_id))
        super(EditQuotePermission, self).__init__(need)


# =============================================================
# 因报价涉及到公司运营层面，需要管理者根据情况授权，下面单独配置授权权限
# =============================================================


# -------------------------------------------------------------
# 报价审核权限(审核针对下属销售)
AuditQuoteNeed = partial(QuoteNeed, 'audit')


class AuditQuotePermission(Permission):
    def __init__(self, sales_id):
        need = AuditQuoteNeed(unicode(sales_id))
        super(AuditQuotePermission, self).__init__(need)
