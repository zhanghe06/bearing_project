#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: inventory.py
@time: 2018-04-06 13:38
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


class InventorySearchForm(FlaskForm):
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
    rack_id = SelectField(
        _('rack name'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=default_choice_option_int,
        coerce=int,
        description=_('rack name'),
        render_kw={
            'rel': 'tooltip',
            'title': _('rack name'),
        }
    )
    op = IntegerField(
        _('Option'),
        validators=[],
        default=0,
    )


class InventoryAddForm(FlaskForm):
    product_id = IntegerField(
        _('product id'),
        validators=[
            DataRequired(),
        ],
        default='',
        description=_('product id'),
        render_kw={
            'placeholder': _('product id'),
            'rel': 'tooltip',
            'title': _('product id'),
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
    rack_id = SelectField(
        _('rack name'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=default_choice_option_int,
        coerce=int,
        description=_('rack name'),
        render_kw={
            'rel': 'tooltip',
            'title': _('rack name'),
        }
    )
    note = StringField(
        _('note'),
        validators=[],
        default='',
        description=_('note'),
        render_kw={
            'placeholder': _('note'),
            'rel': 'tooltip',
            'title': _('note'),
        }
    )


class InventoryEditForm(FlaskForm):
    pass
