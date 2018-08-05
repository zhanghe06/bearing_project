#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: rack.py
@time: 2018-04-06 18:22
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
    IPAddress

from app_common.maps.type_role import TYPE_ROLE_DICT, TYPE_ROLE_MANAGER
from app_backend.api.user import get_user_rows
from app_common.maps.default import default_choices_int, default_choice_option_int, default_choices_str, \
    default_choice_option_str

from copy import copy


class RackSearchForm(FlaskForm):
    warehouse_id = SelectField(
        _('warehouse name'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=default_choice_option_int,
        coerce=int,
        description=_('warehouse name'),
        render_kw={
            'rel': 'tooltip',
            'title': _('warehouse name'),
        }
    )
    name = StringField(
        _('rack name'),
        validators=[],
        default='',
        description=_('rack name'),
        render_kw={
            'placeholder': _('rack name'),
            'rel': 'tooltip',
            'title': _('rack name'),
        }
    )
    op = IntegerField(
        _('Option'),
        validators=[],
        default=0,
    )


class RackAddForm(FlaskForm):
    warehouse_id = SelectField(
        _('warehouse name'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=default_choice_option_int,
        coerce=int,
        description=_('warehouse name'),
        render_kw={
            'rel': 'tooltip',
            'title': _('warehouse name'),
        }
    )
    name = StringField(
        _('rack name'),
        validators=[],
        default='',
        description=_('rack name'),
        render_kw={
            'placeholder': _('rack name'),
            'rel': 'tooltip',
            'title': _('rack name'),
        }
    )


class RackEditForm(FlaskForm):
    id = IntegerField(
        _('rack id'),
        validators=[
            DataRequired(),
        ],
        render_kw={
            'type': 'hidden',
        }
    )
    warehouse_id = SelectField(
        _('warehouse name'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=default_choice_option_int,
        coerce=int,
        description=_('warehouse name'),
        render_kw={
            'rel': 'tooltip',
            'title': _('warehouse name'),
        }
    )
    name = StringField(
        _('rack name'),
        validators=[],
        default='',
        description=_('rack name'),
        render_kw={
            'placeholder': _('rack name'),
            'rel': 'tooltip',
            'title': _('rack name'),
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
