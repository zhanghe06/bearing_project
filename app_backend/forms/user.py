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
from wtforms.validators import InputRequired, DataRequired, Length, NumberRange, EqualTo, Email, ValidationError, IPAddress

from app_common.maps.type_role import TYPE_ROLE_DICT, TYPE_ROLE_MANAGER
from app_backend.api.user import get_user_rows
from app_common.maps.default import default_choices_int, default_choice_option_int

from copy import copy

role_id_choices = copy(default_choices_int)
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
        default=default_choice_option_int,
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
        default=default_choice_option_int,
        coerce=int,
        description=_('user leader'),
        render_kw={
            'rel': 'tooltip',
            'title': _('user leader'),
        }
    )
    start_create_time = DateField(
        _('start time'),
        validators=[],
        default=datetime.utcnow() - timedelta(days=30),
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
        validators=[],
        default=datetime.utcnow(),
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


class UserAddForm(FlaskForm):
    """
    创建表单（字段一般带有默认选项）
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
        default=default_choice_option_int,
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
        default=default_choice_option_int,
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
        default=default_choice_option_int,
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
        default=default_choice_option_int,
        coerce=int,
        description=_('user leader'),
        render_kw={
            'rel': 'tooltip',
            'title': _('user leader'),
        }
    )
    create_time = DateField(
        _('create time'),
        validators=[DataRequired()],
        description=_('create time')
    )
    update_time = DateField(
        _('update time'),
        validators=[DataRequired()],
        description=_('update time')
    )
