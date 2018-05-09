#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: quote.py
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
        '产品品牌',
        validators=[],
        default='',
        description='产品品牌',
        render_kw={
            'placeholder': '产品品牌',
            'rel': "tooltip",
            'title': "产品品牌",
        }
    )
    product_model = StringField(
        '产品型号',
        validators=[],
        default='',
        description='产品型号',
        render_kw={
            'placeholder': '产品型号',
            'rel': "tooltip",
            'title': "产品型号",
        }
    )
    product_sku = StringField(
        '单位',
        validators=[],
        description='单位',
        render_kw={
            'placeholder': '单位',
            'rel': "tooltip",
            'title': "单位",
        }
    )
    quantity = IntegerField(
        '数量',
        validators=[],
        description='数量',
        render_kw={
            'placeholder': '数量',
            'rel': "tooltip",
            'title': "数量",
        }
    )
    unit_price = DecimalField(
        '单价',
        validators=[],
        description='单价',
        render_kw={
            'placeholder': '单价',
            'rel': "tooltip",
            'title': "单价",
        }
    )
    note = StringField(
        '产品评论',
        validators=[],
        default='',
        description='产品评论',
        render_kw={
            'placeholder': '产品评论',
            'rel': "tooltip",
            'title': "产品评论",
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
    quote_items = FieldList(FormField(QuoteItemForm), label='报价明细', min_entries=1)


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
    quote_items = FieldList(FormField(QuoteItemForm), label='报价明细', min_entries=1)

