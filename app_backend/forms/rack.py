#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: rack.py
@time: 2018-04-06 18:22
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
from app_common.maps.default import default_choices_int, default_choice_option_int, default_choices_str, default_choice_option_str

from copy import copy


class RackSearchForm(FlaskForm):
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
    name = StringField(
        '货架名称',
        validators=[],
        default='',
        description='货架名称',
        render_kw={
            'placeholder': '货架名称',
            'rel': "tooltip",
            'title': "货架名称",
        }
    )
    op = IntegerField(
        '操作',
        validators=[],
        default=0,
    )


class RackAddForm(FlaskForm):
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
    name = StringField(
        '货架名称',
        validators=[],
        default='',
        description='货架名称',
        render_kw={
            'placeholder': '货架名称',
            'rel': "tooltip",
            'title': "货架名称",
        }
    )


class RackEditForm(FlaskForm):
    id = IntegerField(
        '货架编号',
        validators=[
            DataRequired(),
        ],
        render_kw={
            'type': 'hidden',
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
    name = StringField(
        '货架名称',
        validators=[],
        default='',
        description='货架名称',
        render_kw={
            'placeholder': '货架名称',
            'rel': "tooltip",
            'title': "货架名称",
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
