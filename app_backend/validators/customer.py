#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: customer.py
@time: 2019-07-15 21:42
"""


from __future__ import unicode_literals

from flask_babel import lazy_gettext as _
from wtforms.validators import ValidationError

from app_backend.api.customer import get_customer_row
from app_backend.models.bearing_project import Customer


class AddCustomerCompanyNameRepeatValidate(object):
    """
    创建客户公司名称重复校验
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        condition = [
            Customer.company_name == field.data,
        ]
        row = get_customer_row(*condition)
        if row:
            raise ValidationError(self.message or _('Data duplication'))


class EditCustomerCompanyNameRepeatValidate(object):
    """
    编辑客户公司名称重复校验
    (编辑重复校验排除当前用户名称)
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        condition = [
            Customer.company_name == field.data,
            Customer.id != form.id.data,
        ]
        row = get_customer_row(*condition)
        if row:
            raise ValidationError(self.message or _('Data duplication'))
