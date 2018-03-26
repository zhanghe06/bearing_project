#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: user.py
@time: 2018-03-22 21:30
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
from app_common.maps.default import default_choices, default_choice_option

from copy import copy

role_id_choices = copy(default_choices)
role_id_choices.extend(iteritems(TYPE_ROLE_DICT))


class UserSearchForm(FlaskForm):
    """
    搜索表单
    """

    name = StringField(
        '用户名称',
        validators=[],
        default='',
        description='用户名称',
        render_kw={
            'placeholder': '用户名称',
            'rel': "tooltip",
            'title': "用户名称",
        }
    )
    role_id = SelectField(
        '用户角色',
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=default_choice_option,
        coerce=int,
        choices=role_id_choices,
        description='用户角色',
        render_kw={
            'rel': "tooltip",
            'title': "用户角色",
        }
    )
    parent_id = SelectField(
        '所属上级',
        default=default_choice_option,
        # validators=[],
        coerce=int,
        description='所属上级',
        render_kw={
            'rel': "tooltip",
            'title': "所属上级",
        }
    )
    start_create_time = DateField(
        '开始时间',
        validators=[],
        default=datetime.utcnow() - timedelta(days=30),
        description='创建开始时间',
        render_kw={
            'placeholder': '创建开始时间',
            'type': 'date',
            'rel': "tooltip",
            'title': "创建开始时间",
        }
    )
    end_create_time = DateField(
        '结束时间',
        validators=[],
        default=datetime.utcnow(),
        description='创建结束时间',
        render_kw={
            'placeholder': '创建结束时间',
            'type': 'date',
            'rel': "tooltip",
            'title': "创建结束时间",
        }
    )
    op = IntegerField(
        '操作',
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=0,
    )


class UserAddForm(FlaskForm):
    """
    创建表单（字段一般带有默认选项）
    """
    pass


class UserEditForm(FlaskForm):
    """
    编辑表单（字段默认选项需要去除）
    """
    pass
