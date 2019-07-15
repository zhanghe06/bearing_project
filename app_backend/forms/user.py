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
from flask_babel import lazy_gettext as _

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, DateTimeField, IntegerField, SelectField
from wtforms.validators import InputRequired, DataRequired, Length, NumberRange, EqualTo, Email, ValidationError, \
    IPAddress, Optional

from app_backend.validators.user import AddUserNameRepeatValidate, EditUserNameRepeatValidate
from app_common.maps.type_role import TYPE_ROLE_DICT, TYPE_ROLE_MANAGER
from app_backend.api.user import get_user_rows
from app_common.maps.default import default_search_choices_int, default_search_choice_option_int

from copy import deepcopy

role_id_choices = deepcopy(default_search_choices_int)
role_id_choices.extend(iteritems(TYPE_ROLE_DICT))


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
        default=default_search_choice_option_int,
        coerce=int,
        choices=role_id_choices,
        description=_('user role'),
        render_kw={
            'rel': 'tooltip',
            'title': _('user role'),
        }
    )
    parent_id = SelectField(
        _('user leader'),
        validators=[],
        default=default_search_choice_option_int,
        coerce=int,
        description=_('user leader'),
        render_kw={
            'rel': 'tooltip',
            'title': _('user leader'),
        }
    )
    start_create_time = DateField(
        _('start time'),
        validators=[Optional()],
        # default=datetime.utcnow() - timedelta(days=365),
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
        # default=datetime.utcnow() + timedelta(days=1),
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
        default=0,
    )
    page = IntegerField(
        _('page'),
        validators=[],
        default=1,
    )


class UserAddForm(FlaskForm):
    """
    创建表单（字段一般带有默认选项）
    """
    name = StringField(
        _('user name'),
        validators=[
            DataRequired(),
            Length(min=2, max=20),
            AddUserNameRepeatValidate(),
        ],
        default='',
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
        default='',
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
        default='',
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
        default='',
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
        default='',
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
        default='',
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
        default=default_search_choice_option_int,
        coerce=int,
        choices=role_id_choices,
        description=_('user role'),
        render_kw={
            'rel': 'tooltip',
            'title': _('user role'),
        }
    )
    parent_id = SelectField(
        _('user leader'),
        validators=[],
        default=default_search_choice_option_int,
        coerce=int,
        description=_('user leader'),
        render_kw={
            'rel': 'tooltip',
            'title': _('user leader'),
        }
    )


class UserEditForm(FlaskForm):
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
        default='',
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
        default='',
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
        default='',
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
        default='',
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
        default='',
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
        default='',
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
        default=default_search_choice_option_int,
        coerce=int,
        choices=role_id_choices,
        description=_('user role'),
        render_kw={
            'rel': 'tooltip',
            'title': _('user role'),
        }
    )
    parent_id = SelectField(
        _('user leader'),
        validators=[],
        default=default_search_choice_option_int,
        coerce=int,
        description=_('user leader'),
        render_kw={
            'rel': 'tooltip',
            'title': _('user leader'),
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
