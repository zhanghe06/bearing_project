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
from six import iteritems
from datetime import datetime, timedelta

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, DateTimeField, IntegerField, SelectField
from wtforms.validators import InputRequired, DataRequired, Length, NumberRange, EqualTo, Email, ValidationError, IPAddress

from app_common.maps.type_role import TYPE_ROLE_DICT, TYPE_ROLE_MANAGER
from app_backend.api.user import get_user_rows
from app_common.maps.default import default_choices_int, default_choice_option_int

from copy import copy

role_id_choices = copy(default_choices_int)
role_id_choices.extend(iteritems(TYPE_ROLE_DICT))


class QuoteSearchForm(FlaskForm):
    quote_brand = SelectField(
        '产品品牌',
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=default_choice_option_int,
        # coerce=int,
        # choices=quote_brand_choices,
        description='产品品牌',
        render_kw={
            'rel': "tooltip",
            'title': "产品品牌",
        }
    )
    quote_model = StringField(
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
    op = IntegerField(
        '操作',
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=0,
    )


class QuoteAddForm(FlaskForm):
    quote_brand = StringField(
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
    quote_model = StringField(
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


class QuoteEditForm(FlaskForm):
    pass

