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
from app_common.maps.default import default_choices_int, default_choice_option_int

from copy import copy


class InventorySearchForm(FlaskForm):
    warehouse_id = SelectField(
        '仓库名称',
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=default_choice_option_int,
        coerce=int,
        description='仓库名称',
        render_kw={
            'rel': "tooltip",
            'title': "仓库名称",
        }
    )
    rack_id = SelectField(
        '货架名称',
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=default_choice_option_int,
        coerce=int,
        description='货架名称',
        render_kw={
            'rel': "tooltip",
            'title': "货架名称",
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
    product_id = IntegerField(
        '产品编号',
        validators=[
            DataRequired(),
        ],
        default='',
        description='产品编号',
        render_kw={
            'placeholder': '产品编号',
            'rel': "tooltip",
            'title': "产品编号",
        }
    )
    warehouse_id = SelectField(
        '仓库名称',
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=default_choice_option_int,
        coerce=int,
        description='仓库名称',
        render_kw={
            'rel': "tooltip",
            'title': "仓库名称",
        }
    )
    rack_id = SelectField(
        '货架名称',
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=default_choice_option_int,
        coerce=int,
        description='货架名称',
        render_kw={
            'rel': "tooltip",
            'title': "货架名称",
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
