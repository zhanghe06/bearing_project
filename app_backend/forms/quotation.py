#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: quotation.py
@time: 2018-04-05 22:37
"""


from __future__ import unicode_literals

import re
import time
from flask import session
from flask_babel import lazy_gettext as _
from six import iteritems
from datetime import datetime, timedelta

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, DateTimeField, IntegerField, SelectField, DecimalField
from wtforms.validators import InputRequired, DataRequired, Length, NumberRange, EqualTo, Email, ValidationError, IPAddress
from wtforms.fields import FieldList, FormField

from app_common.maps.type_role import TYPE_ROLE_DICT, TYPE_ROLE_MANAGER
from app_backend.api.user import get_user_rows
from app_common.maps.default import default_choices_int, default_choice_option_int

from copy import copy

role_id_choices = copy(default_choices_int)
role_id_choices.extend(iteritems(TYPE_ROLE_DICT))


class QuoteSearchForm(FlaskForm):
    uid = SelectField(
        _('quote user'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=default_choice_option_int,
        coerce=int,
        # choices=quote_brand_choices,
        description=_('quote user'),
        render_kw={
            'rel': 'tooltip',
            'title': _('quote user'),
        }
    )
    cid = SelectField(
        _('customer company'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=default_choice_option_int,
        coerce=int,
        # choices=quote_brand_choices,
        description=_('customer company'),
        render_kw={
            'rel': 'tooltip',
            'title': _('customer company'),
        }
    )
    start_create_time = DateField(
        _('start time'),
        validators=[],
        default=datetime.utcnow() - timedelta(days=30),
        description=_('start time'),
        render_kw={
            'placeholder': _('start time'),
            'type': 'date',
            'rel': 'tooltip',
            'title': _('start time'),
        }
    )
    end_create_time = DateField(
        _('end time'),
        validators=[],
        default=datetime.utcnow(),
        description=_('end time'),
        render_kw={
            'placeholder': _('end time'),
            'type': 'date',
            'rel': 'tooltip',
            'title': _('end time'),
        }
    )
    op = IntegerField(
        _('operation'),
        validators=[],
        default=0,
    )


class QuoteItemForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False  # disable csrf
        FlaskForm.__init__(self, *args, **kwargs)

    id = IntegerField(
        _('product id'),
        validators=[
            DataRequired(),
        ],
        render_kw={
            'type': 'hidden',
        }
    )
    quote_id = IntegerField(
        _('quote id'),
        validators=[
        ],
        render_kw={
            'placeholder': _('quote id'),
            'rel': "tooltip",
            'title': _('quote id'),
        }
    )
    product_id = IntegerField(
        _('product id'),
        validators=[
            DataRequired(),
        ],
        render_kw={
            'placeholder': _('product id'),
            'rel': "tooltip",
            'title': _('product id'),
        }
    )
    product_brand = StringField(
        _('product brand'),
        validators=[],
        default='',
        description=_('product brand'),
        render_kw={
            'placeholder': _('product brand'),
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
    product_sku = StringField(
        _('product sku'),
        validators=[],
        description=_('product sku'),
        render_kw={
            'placeholder': _('product sku'),
            'rel': 'tooltip',
            'title': _('product sku'),
        }
    )
    quantity = IntegerField(
        _('quantity'),
        validators=[],
        description=_('quantity'),
        render_kw={
            'placeholder': _('quantity'),
            'rel': 'tooltip',
            'title': _('quantity'),
            'type': 'number',
        }
    )
    unit_price = DecimalField(
        _('unit price'),
        validators=[],
        description=_('unit price'),
        render_kw={
            'placeholder': _('unit price'),
            'rel': 'tooltip',
            'title': _('unit price'),
            'type': 'number',
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


class QuoteAddForm(FlaskForm):
    uid = SelectField(
        _('quote user'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        # default=default_choice_option_int,
        coerce=int,
        # choices=quote_brand_choices,
        description=_('quote user'),
        render_kw={
            'rel': 'tooltip',
            'title': _('quote user'),
        }
    )
    cid = SelectField(
        _('customer company'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=default_choice_option_int,
        coerce=int,
        # choices=quote_brand_choices,
        description=_('customer company'),
        render_kw={
            'rel': 'tooltip',
            'title': _('customer company'),
        }
    )
    quote_items = FieldList(
        FormField(QuoteItemForm),
        label='报价明细',
        min_entries=1,
    )


class QuoteEditForm(FlaskForm):
    uid = SelectField(
        _('quote user'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        # default=default_choice_option_int,
        coerce=int,
        # choices=quote_brand_choices,
        description=_('quote user'),
        render_kw={
            'rel': 'tooltip',
            'title': _('quote user'),
        }
    )
    cid = SelectField(
        _('customer company'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=default_choice_option_int,
        coerce=int,
        # choices=quote_brand_choices,
        description=_('customer company'),
        render_kw={
            'rel': 'tooltip',
            'title': _('customer company'),
        }
    )
    data_line_add = IntegerField(
        '数据行新增',
        validators=[],
    )
    data_line_del = IntegerField(
        '数据行删除',
        validators=[],
    )
    quote_items = FieldList(
        FormField(QuoteItemForm),
        label='报价明细',
        min_entries=1,
    )
