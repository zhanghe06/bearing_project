#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: product.py
@time: 2018-04-05 00:54
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
from app_common.maps.default import default_choices_str, default_choice_option_str

from copy import copy


class ProductSearchForm(FlaskForm):
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


class ProductAddForm(FlaskForm):
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


class ProductEditForm(FlaskForm):
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
    create_time = DateField(
        '创建时间',
        validators=[DataRequired()],
        description='创建时间'
    )
    update_time = DateField(
        '更新时间',
        validators=[DataRequired()],
        description='更新时间'
    )
