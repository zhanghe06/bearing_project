#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: inventory.py
@time: 2018-04-06 13:38
"""

from __future__ import unicode_literals

from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, \
    HiddenField
from wtforms.validators import InputRequired, DataRequired, Length

from app_backend.api.inventory import get_distinct_inventory_brand
from app_common.maps.default import DEFAULT_SEARCH_CHOICES_INT_OPTION, \
    DEFAULT_SEARCH_CHOICES_STR_OPTION, DEFAULT_SEARCH_CHOICES_STR
from app_common.maps.status_delete import STATUS_DEL_NO

inventory_brand_choices = [(brand, brand) for brand in get_distinct_inventory_brand(status_delete=STATUS_DEL_NO) if
                           brand != '']

INVENTORY_BRAND_SEARCH_CHOICES = DEFAULT_SEARCH_CHOICES_STR + inventory_brand_choices


class InventorySearchForm(FlaskForm):
    warehouse_id = SelectField(
        _('warehouse name'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=DEFAULT_SEARCH_CHOICES_INT_OPTION,
        coerce=int,
        description=_('warehouse name'),
        render_kw={
            'rel': 'tooltip',
            'title': _('warehouse name'),
        }
    )
    rack_id = SelectField(
        _('rack name'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=DEFAULT_SEARCH_CHOICES_INT_OPTION,
        coerce=int,
        description=_('rack name'),
        render_kw={
            'rel': 'tooltip',
            'title': _('rack name'),
        }
    )
    production_brand = SelectField(
        _('production brand'),
        validators=[],  # 字符类型，非必填
        default=DEFAULT_SEARCH_CHOICES_STR_OPTION,
        choices=INVENTORY_BRAND_SEARCH_CHOICES,
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
        _('Option'),
        validators=[],
        default=0,
    )
    page = IntegerField(
        _('page'),
        validators=[],
        default=1,
    )


class InventoryAddForm(FlaskForm):
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
    warehouse_id = SelectField(
        _('warehouse name'),
        validators=[
            DataRequired(),
        ],
        default=0,
        coerce=int,
        description=_('warehouse name'),
        render_kw={
            'rel': 'tooltip',
            'title': _('warehouse name'),
        }
    )
    rack_id = SelectField(
        _('rack name'),
        validators=[
            DataRequired(),
        ],
        default=0,
        coerce=int,
        description=_('rack name'),
        render_kw={
            'rel': 'tooltip',
            'title': _('rack name'),
        }
    )
    stock_qty = IntegerField(
        _('stock quantity'),
        validators=[
            DataRequired(),
        ],
        default=1,
        description=_('stock quantity'),
        render_kw={
            'placeholder': _('stock quantity'),
            'rel': 'tooltip',
            'title': _('stock quantity'),
            'type': 'number',
            'step': 1,
            'min': 1,
            'max': 10000,
        }
    )
    note = StringField(
        _('note'),
        validators=[],
        default='',
        description=_('note'),
        render_kw={
            'placeholder': _('note'),
            'rel': 'tooltip',
            'title': _('note'),
        }
    )
    warehouse_changed = HiddenField(
        _('warehouse changed'),
        default='',
    )


class InventoryEditForm(InventoryAddForm):
    pass


class InventoryTransferForm(InventoryAddForm):
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
            'readonly': 'readonly',
        }
    )
    warehouse_name_from = StringField(
        _('original warehouse'),
        validators=[
            DataRequired(),
        ],
        description=_('original warehouse'),
        render_kw={
            'rel': 'tooltip',
            'title': _('original warehouse'),
            'readonly': 'readonly',
        }
    )
    rack_name_from = StringField(
        _('original rack'),
        validators=[
            DataRequired(),
        ],
        description=_('original rack'),
        render_kw={
            'rel': 'tooltip',
            'title': _('original rack'),
            'readonly': 'readonly',
        }
    )
