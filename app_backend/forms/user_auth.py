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
from flask_babel import lazy_gettext as _
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
            raise ValidationError(self.message or _('Captcha Format Error'))

        code_key = '%s:%s' % ('code_str', 'login')
        code_str = session.pop(code_key, '')
        if not code_str:
            # 注意：validators 执行会渲染html元素，与页面同步加载，所以无法确认 session弹出 先后顺序
            # 如果 validators 先执行，session再弹出，则会出现session验证码为空的情况
            # 所以，表单校验之后，重新加载页面，验证码的刷新动作，应该在页面加载完成之后由js控制刷新
            raise ValidationError(self.message or _('Captcha Expired'))
        if code_str.upper() != data.upper():
            raise ValidationError(self.message or _('Captcha Value Failure'))


class UserAuthForm(FlaskForm):
    """
    表单(用户登录认证)
    """
    auth_key = StringField(
        _('Username'),
        validators=[
            DataRequired(_('This field is required.')),
            Length(
                min=2,
                max=20,
                message=_('Field must be between %(min)s and %(max)s characters long.', min=2, max=20)
            ),
        ],
        description=_('Username'),
        render_kw={
            'placeholder': _('Username'),
            'minlength': 2,
            'maxlength': 20,
        }
    )
    auth_secret = PasswordField(
        _('Password'),
        validators=[
            DataRequired(_('This field is required.')),
            Length(
                min=6,
                max=20,
                message=_('Field must be between %(min)s and %(max)s characters long.', min=6, max=20)
            ),
        ],
        description=_('Password'),
        render_kw={
            'placeholder': _('Password'),
            'minlength': 6,
            'maxlength': 20,
        }
    )
    captcha = StringField(
        _('Captcha'),
        validators=[
            DataRequired(_('This field is required.')),
            Length(
                min=4,
                max=4,
                message=_('Field must be %(length)s characters long.', length=4)
            ),
            CaptchaValidate()
        ],
        description=_('Captcha'),
        render_kw={
            'placeholder': _('Captcha'),
            'minlength': 4,
            'maxlength': 4,
            'autocomplete': 'off',
        }
    )
    remember = BooleanField(_('Remember me'), default=False)


class UserAuthEmailForm(FlaskForm):
    """
    表单(用户邮箱登录)
    """
    auth_key = StringField(
        _('Email'),
        validators=[
            DataRequired(_('This field is required.')),
            Email(),
        ],
        description=_('Type email, click the login button, then enter mailbox, click the authentication link to sign in'),
        render_kw={
            'placeholder': _('Email'),
            'type': 'email',
        }
    )


class UserAuthChangePasswordForm(FlaskForm):
    """
    修改密码
    """
    password_current = PasswordField(
        _('Current Password'),
        validators=[
            DataRequired(_('This field is required.')),
            Length(
                min=6,
                max=20,
                message=_('Field must be between %(min)s and %(max)s characters long.', min=6, max=20)
            ),
        ],
        description='6-20个字符',
        render_kw={
            'placeholder': _('Current Password'),
            'minlength': 6,
            'maxlength': 20,
        }
    )
    password_new = PasswordField(
        _('New Password'),
        validators=[
            DataRequired(_('This field is required.')),
            Length(
                min=6,
                max=20,
                message=_('Field must be between %(min)s and %(max)s characters long.', min=6, max=20)
            ),
        ],
        description='6-20个字符',
        render_kw={
            'placeholder': _('New Password'),
            'minlength': 6,
            'maxlength': 20,
        }
    )
    password_confirm = PasswordField(
        _('Confirm Password'),
        validators=[
            DataRequired(_('This field is required.')),
            Length(
                min=6,
                max=20,
                message=_('Field must be between %(min)s and %(max)s characters long.', min=6, max=20)
            ),
            EqualTo(
                'password_new',
                message='两次输入的密码不一致',
            )
        ],
        description='6-20个字符',
        render_kw={
            'placeholder': _('Confirm Password'),
            'minlength': 6,
            'maxlength': 20,
        }
    )


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
