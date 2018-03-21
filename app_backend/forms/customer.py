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

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, EqualTo, Email, ValidationError, IPAddress


class CustomerSearchForm(FlaskForm):
    """
    搜索表单
    """
    company_name = StringField(
        '公司名称',
        validators=[Length(max=100)],
        description='公司名称，最大长度100字符',
        render_kw={
            'placeholder': '公司名称',
        }
    )
    company_type = IntegerField(
        '公司类型',
        validators=[],
        default=0,
        description='公司类型',
        render_kw={
            'placeholder': '公司类型',
        }
    )
    owner_uid = IntegerField(
        '所属销售',
        validators=[],
        default=0,
        description='所属销售',
        render_kw={
            'placeholder': '所属销售',
        }
    )
    start_create_time = DateField(
        '开始时间',
        validators=[],
        description='创建开始时间',
        render_kw={
            'placeholder': '创建开始时间',
        }
    )
    end_create_time = DateField(
        '结束时间',
        validators=[],
        description='创建结束时间',
        render_kw={
            'placeholder': '创建结束时间',
        }
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
