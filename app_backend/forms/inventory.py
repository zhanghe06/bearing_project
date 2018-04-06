#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: inventory.py
@time: 2018-04-06 13:38
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
from app_common.maps.default import default_choices_int, default_choice_option_str

from copy import copy


class InventorySearchForm(FlaskForm):
    product_brand = SelectField(
        '产品品牌',
        validators=[],  # 字符类型，非必填
        default=default_choice_option_str,
        description='产品品牌',
        render_kw={
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
    op = IntegerField(
        '操作',
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=0,
    )


class InventoryAddForm(FlaskForm):
    inventory_brand = StringField(
        '产品品牌',
        validators=[DataRequired()],
        default='',
        description='产品品牌',
        render_kw={
            'placeholder': '产品品牌',
            'rel': "tooltip",
            'title': "产品品牌",
        }
    )
    inventory_model = StringField(
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


class InventoryEditForm(FlaskForm):
    pass
