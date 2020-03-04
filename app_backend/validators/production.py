#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: production.py
@time: 2019-07-15 20:35
"""

from __future__ import unicode_literals

from flask_babel import lazy_gettext as _
from wtforms.validators import ValidationError

from app_backend.api.production import get_production_row
from app_backend.models.model_bearing import Production


class AddProductionModelRepeatValidate(object):
    """
    创建产品型号重复校验
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        condition = [
            Production.production_brand == form.production_brand.data.upper(),
            Production.production_model == field.data.upper(),
        ]
        row = get_production_row(*condition)
        if row:
            raise ValidationError(self.message or _('Data duplication'))


class EditProductionModelRepeatValidate(object):
    """
    编辑产品型号重复校验
    (编辑重复校验排除当前产品型号)
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        condition = [
            Production.production_brand == form.production_brand.data.upper(),
            Production.production_model == field.data.upper(),
            Production.id != form.id.data,
        ]
        row = get_production_row(*condition)
        if row:
            raise ValidationError(self.message or _('Data duplication'))
