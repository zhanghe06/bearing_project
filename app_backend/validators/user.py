#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: user.py
@time: 2019-07-15 19:00
"""


from __future__ import unicode_literals

from flask_babel import lazy_gettext as _
from wtforms.validators import ValidationError

from app_backend.api.user import get_user_row
from app_backend.models.bearing_project import User


class AddUserNameRepeatValidate(object):
    """
    创建用户名称重复校验
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        condition = [
            User.name == field.data,
        ]
        row = get_user_row(*condition)
        if row:
            raise ValidationError(self.message or _('Data duplication'))


class EditUserNameRepeatValidate(object):
    """
    编辑用户名称重复校验
    (编辑重复校验排除当前用户名称)
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        condition = [
            User.name == field.data,
            User.id != form.id.data,
        ]
        row = get_user_row(*condition)
        if row:
            raise ValidationError(self.message or _('Data duplication'))
