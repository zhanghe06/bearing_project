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

from app_backend.api.user_auth import get_user_auth_row
from app_backend.models.bearing_project import UserAuth


class AddUserAuthKeyRepeatValidate(object):
    """
    创建认证信息重复校验
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        condition = [
            UserAuth.type_auth == form.type_auth.data,
            UserAuth.auth_key == field.data,
        ]
        row = get_user_auth_row(*condition)
        if row:
            raise ValidationError(self.message or _('Data duplication'))


class EditUserAuthKeyRepeatValidate(object):
    """
    编辑认证信息重复校验
    (编辑重复校验排除当前用户认证)
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        condition = [
            UserAuth.type_auth == form.type_auth.data,
            UserAuth.auth_key == field.data,
            UserAuth.id != form.id.data,
        ]
        row = get_user_auth_row(*condition)
        if row:
            raise ValidationError(self.message or _('Data duplication'))
