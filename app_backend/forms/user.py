#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: user.py
@time: 2018-03-22 21:30
"""

from __future__ import unicode_literals

from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SelectField
from wtforms.validators import InputRequired, DataRequired, Length, Optional

from app_backend.validators.user import AddUserNameRepeatValidate, EditUserNameRepeatValidate, \
    EditUserRolePermissionValidate
from app_common.maps.default import DEFAULT_SEARCH_CHOICES_INT_OPTION, DEFAULT_SELECT_CHOICES_INT_OPTION
from app_common.maps.operations import OPERATION_SEARCH
from app_common.maps.type_role import TYPE_ROLE_SELECT_CHOICES, TYPE_ROLE_SEARCH_CHOICES


class UserSearchForm(FlaskForm):
    """
    搜索表单
    """
    name = StringField(
        _('user name'),
        validators=[],
        default='',
        description=_('user name'),
        render_kw={
            'placeholder': _('user name'),
            'rel': 'tooltip',
            'title': _('user name'),
        }
    )
    role_id = SelectField(
        _('user role'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=DEFAULT_SEARCH_CHOICES_INT_OPTION,
        coerce=int,
        choices=TYPE_ROLE_SEARCH_CHOICES,
        description=_('user role'),
        render_kw={
            'rel': 'tooltip',
            'title': _('user role'),
        }
    )
    start_create_time = DateField(
        _('start time'),
        validators=[Optional()],
        description=_('start time'),
        render_kw={
            'placeholder': _('start time'),
            'type': 'date',
            'rel': 'tooltip',
            'title': _('start time'),
        }
    )
    end_create_time = DateField(
        _('end time'),
        validators=[Optional()],
        description=_('end time'),
        render_kw={
            'placeholder': _('end time'),
            'type': 'date',
            'rel': 'tooltip',
            'title': _('end time'),
        }
    )
    op = IntegerField(
        _('Option'),
        validators=[],
        default=OPERATION_SEARCH,
    )
    page = IntegerField(
        _('page'),
        validators=[],
        default=1,
    )


class UserAddForm(FlaskForm):
    """
    创建表单
    """
    name = StringField(
        _('user name'),
        validators=[
            DataRequired(),
            Length(min=2, max=20),
            AddUserNameRepeatValidate(),
        ],
        description=_('user name'),
        render_kw={
            'placeholder': _('user name'),
            'rel': 'tooltip',
            'title': _('user name'),
        }
    )
    salutation = StringField(
        _('salutation'),
        validators=[],
        description=_('salutation'),
        render_kw={
            'placeholder': _('salutation'),
            'rel': 'tooltip',
            'title': _('salutation'),
        }
    )
    mobile = StringField(
        _('mobile'),
        validators=[],
        description=_('mobile'),
        render_kw={
            'placeholder': _('mobile'),
            'rel': 'tooltip',
            'title': _('mobile'),
        }
    )
    tel = StringField(
        _('tel'),
        validators=[],
        description=_('tel'),
        render_kw={
            'placeholder': _('tel'),
            'rel': 'tooltip',
            'title': _('tel'),
        }
    )
    fax = StringField(
        _('fax'),
        validators=[],
        description=_('fax'),
        render_kw={
            'placeholder': _('fax'),
            'rel': 'tooltip',
            'title': _('fax'),
        }
    )
    email = StringField(
        _('email'),
        validators=[],
        description=_('email'),
        render_kw={
            'placeholder': _('email'),
            'rel': 'tooltip',
            'title': _('email'),
        }
    )
    role_id = SelectField(
        _('user role'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=DEFAULT_SELECT_CHOICES_INT_OPTION,
        coerce=int,
        choices=TYPE_ROLE_SELECT_CHOICES,
        description=_('user role'),
        render_kw={
            'rel': 'tooltip',
            'title': _('user role'),
        }
    )


class UserEditForm(UserAddForm):
    """
    编辑表单（字段默认选项需要去除）
    """
    id = IntegerField(
        _('user id'),
        validators=[
            DataRequired(),
        ],
        render_kw={
            'type': 'hidden',
        }
    )
    name = StringField(
        _('user name'),
        validators=[
            DataRequired(),
            Length(min=2, max=20),
            EditUserNameRepeatValidate(),
        ],
        description=_('user name'),
        render_kw={
            'placeholder': _('user name'),
            'rel': 'tooltip',
            'title': _('user name'),
        }
    )
    role_id = SelectField(
        _('user role'),
        validators=[
            InputRequired(),  # 可以为0
            EditUserRolePermissionValidate(),
        ],
        default=DEFAULT_SELECT_CHOICES_INT_OPTION,
        coerce=int,
        choices=TYPE_ROLE_SELECT_CHOICES,
        description=_('user role'),
        render_kw={
            'rel': 'tooltip',
            'title': _('user role'),
        }
    )
    create_time = DateField(
        _('create time'),
        validators=[],
        description=_('create time')
    )
    update_time = DateField(
        _('update time'),
        validators=[],
        description=_('update time')
    )
