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

from flask import session
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError


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
        description=_(
            'Type email, click the login button, then enter mailbox, click the authentication link to sign in'),
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
