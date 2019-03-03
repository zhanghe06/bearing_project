#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: production_sensitive.py
@time: 2018-08-14 16:34
"""


from __future__ import unicode_literals

from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError, Length, InputRequired

from wtforms.widgets import HTMLString
from wtforms.compat import text_type, iteritems
from wtforms.widgets import html_params

from app_backend.api.production import get_production_row
from app_backend.models.bearing_project import Production
from app_common.maps.default import default_search_choice_option_str, default_search_choice_option_int


class ProductionSensitiveSearchForm(FlaskForm):
    """
    搜索表单
    """
    customer_cid = IntegerField(
        _('customer company id'),
        validators=[
            InputRequired(),
        ],
        default=0,
        description=_('customer company id'),
        render_kw={
            'rel': 'tooltip',
            'title': _('customer company id'),
            'placeholder': _('customer company id'),
            'autocomplete': 'off',
            'type': 'hidden',
        }
    )
    customer_company_name = StringField(
        _('customer company name'),
        validators=[],
        description=_('customer company name'),
        render_kw={
            'placeholder': _('customer company name'),
            'rel': 'tooltip',
            'title': _('customer company name'),
        }
    )
    production_brand = SelectField(
        _('production brand'),
        validators=[],  # 字符类型，非必填
        default=default_search_choice_option_str,
        description=_('production brand'),
        render_kw={
            'rel': 'tooltip',
            'title': _('production brand'),
        }
    )
    production_model = StringField(
        _('production model'),
        validators=[],
        description=_('production model'),
        render_kw={
            'placeholder': _('production model'),
            'rel': 'tooltip',
            'title': _('production model'),
            'autocomplete': 'off',
        }
    )
    op = IntegerField(
        _('operation'),
        validators=[],
        default=0,
    )
    page = IntegerField(
        _('page'),
        validators=[],
        default=1,
    )


class ProductionSensitiveAddForm(FlaskForm):
    """
    创建表单
    """
    customer_cid = IntegerField(
        _('customer company id'),
        validators=[
            DataRequired(),
        ],
        default=0,
        description=_('customer company id'),
        render_kw={
            'rel': 'tooltip',
            'title': _('customer company id'),
            'placeholder': _('customer company id'),
            'autocomplete': 'off',
            'type': 'hidden',
        }
    )
    customer_company_name = StringField(
        _('customer company name'),
        validators=[],
        description=_('customer company name'),
        render_kw={
            'placeholder': _('customer company name'),
            'rel': 'tooltip',
            'title': _('customer company name'),
            'autocomplete': 'off',
        }
    )
    production_id = IntegerField(
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
        default='',
        description='产品品牌（例如：SKF、FAG、NSK...）',
        render_kw={
            'placeholder': _('production brand'),
            'rel': 'tooltip',
            'title': _('production brand'),
            'autocomplete': 'off',
            'readonly': 'readonly',
        }
    )
    production_model = StringField(
        _('production model'),
        validators=[
            DataRequired(),
        ],
        default='',
        description='产品型号（例如：7008CEGA/HCP4A）',
        render_kw={
            'placeholder': _('production model'),
            'rel': 'tooltip',
            'title': _('production model'),
            'autocomplete': 'off',
        }
    )
    production_sku = StringField(
        _('production sku'),
        validators=[
            DataRequired(),
            Length(min=2, max=16),
        ],
        description='单位（Pcs:个,Pair:对,Set:组）',
        render_kw={
            'placeholder': _('production sku'),
            'rel': 'tooltip',
            'title': _('production sku'),
            'autocomplete': 'off',
            'readonly': 'readonly',
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
            'autocomplete': 'off',
        }
    )


class ProductionSensitiveEditForm(ProductionSensitiveAddForm):
    """
    编辑表单
    """
    id = IntegerField(
        _('production sensitive id'),
        validators=[
            DataRequired(),
        ],
        render_kw={
            'type': 'hidden',
        }
    )
    create_time = DateField(
        _('create time'),
        validators=[],
        description=_('create time')
    )
    update_time = DateField(
        _('update time'),
        validators=[],
        description=_('update time')
    )
