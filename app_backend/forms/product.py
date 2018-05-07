#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: product.py
@time: 2018-04-05 00:54
"""

from __future__ import unicode_literals

from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError

from app_backend.api.product import get_product_row
from app_backend.models.bearing_project import Product
from app_common.maps.default import default_choice_option_str


class AddProductModelRepeatValidate(object):
    """
    创建产品型号重复校验
    """
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        condition = [
            Product.product_brand == form.product_brand.data,
            Product.product_model == field.data,
        ]
        row = get_product_row(*condition)
        if row:
            raise ValidationError(self.message or _('Data duplication'))


class EditProductModelRepeatValidate(object):
    """
    编辑产品型号重复校验
    (编辑重复校验排除当前产品型号)
    """
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        condition = [
            Product.product_brand == form.product_brand.data,
            Product.product_model == field.data,
        ]
        row = get_product_row(*condition)
        if row and row.id != form.id.data:
            raise ValidationError(self.message or _('Data duplication'))


class ProductSearchForm(FlaskForm):
    """
    搜索表单
    """
    product_brand = SelectField(
        _('product brand'),
        validators=[],  # 字符类型，非必填
        default=default_choice_option_str,
        description=_('product brand'),
        render_kw={
            'rel': 'tooltip',
            'title': _('product brand'),
        }
    )
    product_model = StringField(
        _('product model'),
        validators=[],
        default='',
        description=_('product model'),
        render_kw={
            'placeholder': _('product model'),
            'rel': 'tooltip',
            'title': _('product model'),
        }
    )
    op = IntegerField(
        _('operation'),
        validators=[],
        default=0,
    )


class ProductAddForm(FlaskForm):
    """
    创建表单
    """
    product_brand = StringField(
        _('product brand'),
        validators=[
            DataRequired(),
        ],
        default='',
        description='产品品牌（例如：SKF、FAG、NSK...）',
        render_kw={
            'placeholder': _('product brand'),
            'rel': 'tooltip',
            'title': _('product brand'),
        }
    )
    product_model = StringField(
        _('product model'),
        validators=[
            DataRequired(),
            AddProductModelRepeatValidate(),
        ],
        default='',
        description='产品型号（例如：7008CEGA/HCP4A）',
        render_kw={
            'placeholder': _('product model'),
            'rel': 'tooltip',
            'title': _('product model'),
        }
    )
    note = StringField(
        _('product note'),
        validators=[],
        default='',
        description='产品备注（例如：最小起订量12个）',
        render_kw={
            'placeholder': _('product note'),
            'rel': 'tooltip',
            'title': _('product note'),
        }
    )


class ProductEditForm(FlaskForm):
    """
    编辑表单
    """
    id = IntegerField(
        _('product id'),
        validators=[
            DataRequired(),
        ],
        render_kw={
            'type': 'hidden',
        }
    )
    product_brand = StringField(
        _('product brand'),
        validators=[
            DataRequired(),
        ],
        description='产品品牌（例如：SKF、FAG、NSK...）',
        render_kw={
            'placeholder': _('product brand'),
            'rel': 'tooltip',
            'title': _('product brand'),
        }
    )
    product_model = StringField(
        _('product model'),
        validators=[
            DataRequired(),
            EditProductModelRepeatValidate(),
        ],
        description='产品型号（例如：7008CEGA/HCP4A）',
        render_kw={
            'placeholder': _('product model'),
            'rel': 'tooltip',
            'title': _('product model'),
        }
    )
    note = StringField(
        _('product note'),
        validators=[],
        description='产品备注（例如：最小起订量12个）',
        render_kw={
            'placeholder': _('product note'),
            'rel': 'tooltip',
            'title': _('product note'),
        }
    )
    create_time = DateField(
        _('create time'),
        validators=[],
        description=_('create time'),
    )
    update_time = DateField(
        _('update time'),
        validators=[],
        description=_('update time'),
    )
