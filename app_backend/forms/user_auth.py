#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: user_auth.py
@time: 2018-03-17 21:27
"""

from __future__ import unicode_literals

import re
import time
from flask import session

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, EqualTo, Email, ValidationError, IPAddress


class CaptchaValidate(object):
    """
    图形验证码校验
    """
    def __init__(self, message=None):
        self.message = message

        self._reg = re.compile(r'^\w{4}$')

    def __call__(self, form, field):
        data = field.data
        if not self._reg.match(data):
            raise ValidationError(self.message or '图形验证码格式错误')

        code_key = '%s:%s' % ('code_str', 'login')
        code_str = session.pop(code_key, '')
        if not code_str:
            raise ValidationError(self.message or '图形验证码过期失效')
        if code_str.upper() != data.upper():
            raise ValidationError(self.message or '图形验证码校验错误')


class UserAuthForm(FlaskForm):
    """
    表单(用户登录认证)
    """
    auth_key = StringField(
        '登录账号',
        validators=[
            DataRequired('登录账号不能为空'),
            Length(min=2, max=20, message='登录账号长度不符'),
        ],
        description='登录账号，2-20个字符',
        render_kw={
            'placeholder': '登录账号，2-20个字符',
            'minlength': 2,
            'maxlength': 20,
        }
    )
    auth_secret = PasswordField(
        '登录密码',
        validators=[
            DataRequired('登录密码不能为空'),
            Length(min=6, max=20, message='登录密码长度不符'),
        ],
        description='登录密码，6-20个字符',
        render_kw={
            'placeholder': '登录密码，6-20个字符',
            'minlength': 6,
            'maxlength': 20,
        }
    )
    captcha = StringField(
        '图形验证码',
        validators=[
            DataRequired('图形验证码不能为空'),
            Length(min=4, max=4, message='图形验证码长度不符'),
            CaptchaValidate()
        ],
        description='图形验证码，4个字符',
        render_kw={
            'placeholder': '图形验证码，4个字符',
            'minlength': 4,
            'maxlength': 4,
        }
    )
    remember = BooleanField('记住登录状态', default=False)


class UserAuthAddForm(FlaskForm):
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


class UserAuthEditForm(FlaskForm):
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
