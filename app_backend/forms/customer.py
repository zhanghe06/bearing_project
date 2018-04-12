#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: customer.py
@time: 2018-03-16 14:41
"""

from __future__ import unicode_literals

import time
from datetime import datetime, timedelta
from six import iteritems

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, DateTimeField, IntegerField, SelectField
from wtforms.validators import InputRequired, DataRequired, Length, NumberRange, EqualTo, Email, ValidationError, IPAddress
from app_common.maps.default import default_choices_int, default_choice_option_int
from app_common.maps.type_company import TYPE_COMPANY_DICT

from copy import copy

company_type_choices = copy(default_choices_int)
company_type_choices.extend(iteritems(TYPE_COMPANY_DICT))


class CustomerSearchForm(FlaskForm):
    """
    搜索表单
    """
    company_name = StringField(
        '公司名称',
        validators=[],
        description='公司类型',
        render_kw={
            'placeholder': '公司名称',
            'rel': "tooltip",
            'title': "公司名称",
        }
    )
    company_type = SelectField(
        '公司类型',
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=default_choice_option_int,
        coerce=int,
        choices=company_type_choices,
        description='公司类型',
        render_kw={
            'rel': "tooltip",
            'title': "公司类型",
        }
    )
    owner_uid = SelectField(
        '所属销售',
        default=default_choice_option_int,
        # validators=[],
        coerce=int,
        description='所属销售',
        render_kw={
            'rel': "tooltip",
            'title': "所属销售",
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
        validators=[],
        default=0,
    )


class CustomerAddForm(FlaskForm):
    """
    创建表单（字段一般带有默认选项）
    """
    company_name = StringField(
        '公司名称',
        validators=[DataRequired(), Length(max=100)],
        description='公司名称，最大长度100字符'
    )
    company_address = StringField(
        '公司地址',
        validators=[DataRequired(), Length(max=100)],
        description='公司地址，最大长度100字符'
    )
    company_site = StringField(
        '公司官网',
        validators=[DataRequired(), Length(max=100)],
        description='公司官网，最大长度100字符'
    )
    company_tel = StringField(
        '公司电话',
        validators=[DataRequired(), Length(max=100)],
        description='公司电话，最大长度100字符'
    )
    company_fax = StringField(
        '公司传真',
        validators=[DataRequired(), Length(max=100)],
        description='公司传真，最大长度100字符'
    )
    company_type = IntegerField(
        '公司类型',
        validators=[DataRequired()],
        default=0,
        description='公司类型'
    )
    owner_uid = IntegerField(
        '所属销售',
        validators=[DataRequired()],
        default=0,
        description='所属销售'
    )
    status_delete = IntegerField(
        '删除状态',
        validators=[DataRequired()],
        default=0,
        description='删除状态'
    )
    delete_time = DateField(
        '删除时间',
        validators=[DataRequired()],
        description='删除时间'
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


class CustomerEditForm(FlaskForm):
    """
    编辑表单（字段默认选项需要去除）
    """
    company_name = StringField(
        '公司名称',
        validators=[DataRequired(), Length(max=100)],
        description='公司名称，最大长度100字符'
    )
    company_address = StringField(
        '公司地址',
        validators=[DataRequired(), Length(max=100)],
        description='公司地址，最大长度100字符'
    )
    company_site = StringField(
        '公司官网',
        validators=[DataRequired(), Length(max=100)],
        description='公司官网，最大长度100字符'
    )
    company_tel = StringField(
        '公司电话',
        validators=[DataRequired(), Length(max=100)],
        description='公司电话，最大长度100字符'
    )
    company_fax = StringField(
        '公司传真',
        validators=[DataRequired(), Length(max=100)],
        description='公司传真，最大长度100字符'
    )
    company_type = IntegerField(
        '公司类型',
        validators=[DataRequired()],
        default=0,
        description='公司类型'
    )
    owner_uid = IntegerField(
        '所属销售',
        validators=[DataRequired()],
        default=0,
        description='所属销售'
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
