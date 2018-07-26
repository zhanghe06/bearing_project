#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: production.py
@time: 2018-04-05 00:54
"""

from __future__ import unicode_literals

from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError

from app_backend.api.production import get_production_row
from app_backend.models.bearing_project import Production
from app_common.maps.default import default_choice_option_str


class AddProductionModelRepeatValidate(object):
    """
    创建产品型号重复校验
    """
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        condition = [
            Production.production_brand == form.production_brand.data,
            Production.production_model == field.data,
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
            Production.production_brand == form.production_brand.data,
            Production.production_model == field.data,
        ]
        row = get_production_row(*condition)
        if row and row.id != form.id.data:
            raise ValidationError(self.message or _('Data duplication'))


class ProductionSearchForm(FlaskForm):
    """
    搜索表单
    """
    production_brand = SelectField(
        _('production brand'),
        validators=[],  # 字符类型，非必填
        default=default_choice_option_str,
        description=_('production brand'),
        render_kw={
            'rel': 'tooltip',
            'title': _('production brand'),
        }
    )
    production_model = StringField(
        _('production model'),
        validators=[],
        default='',
        description=_('production model'),
        render_kw={
            'placeholder': _('production model'),
            'rel': 'tooltip',
            'title': _('production model'),
        }
    )
    op = IntegerField(
        _('operation'),
        validators=[],
        default=0,
    )


class ProductionAddForm(FlaskForm):
    """
    创建表单
    """
    production_brand = StringField(
        _('production brand'),
        validators=[
            DataRequired(),
        ],
        default='',
        description='产品品牌（例如：SKF、FAG、NSK...）',
        render_kw={
            'placeholder': _('production brand'),
            'rel': 'tooltip',
            'title': _('production brand'),
        }
    )
    production_model = StringField(
        _('production model'),
        validators=[
            DataRequired(),
            AddProductionModelRepeatValidate(),
        ],
        default='',
        description='产品型号（例如：7008CEGA/HCP4A）',
        render_kw={
            'placeholder': _('production model'),
            'rel': 'tooltip',
            'title': _('production model'),
        }
    )
    note = StringField(
        _('production note'),
        validators=[],
        default='',
        description='产品备注（例如：最小起订量12个）',
        render_kw={
            'placeholder': _('production note'),
            'rel': 'tooltip',
            'title': _('production note'),
        }
    )


class ProductionEditForm(FlaskForm):
    """
    编辑表单
    """
    id = IntegerField(
        _('production id'),
        validators=[
            DataRequired(),
        ],
        render_kw={
            'type': 'hidden',
        }
    )
    production_brand = StringField(
        _('production brand'),
        validators=[
            DataRequired(),
        ],
        description='产品品牌（例如：SKF、FAG、NSK...）',
        render_kw={
            'placeholder': _('production brand'),
            'rel': 'tooltip',
            'title': _('production brand'),
        }
    )
    production_model = StringField(
        _('production model'),
        validators=[
            DataRequired(),
            EditProductionModelRepeatValidate(),
        ],
        description='产品型号（例如：7008CEGA/HCP4A）',
        render_kw={
            'placeholder': _('production model'),
            'rel': 'tooltip',
            'title': _('production model'),
        }
    )
    note = StringField(
        _('production note'),
        validators=[],
        description='产品备注（例如：最小起订量12个）',
        render_kw={
            'placeholder': _('production note'),
            'rel': 'tooltip',
            'title': _('production note'),
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
