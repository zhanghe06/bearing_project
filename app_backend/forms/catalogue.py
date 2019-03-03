#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: catalogue.py
@time: 2018-04-16 21:54
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
from app_common.maps.default import default_search_choices_str, default_search_choice_option_str

from copy import deepcopy


class CatalogueSearchForm(FlaskForm):
    product_brand = SelectField(
        _('product brand'),
        validators=[],  # 字符类型，非必填
        default=default_search_choice_option_str,
        description=_('product brand'),
        render_kw={
            'rel': 'tooltip',
            'title': _('product brand'),
        }
    )
    product_model = StringField(
        _('product model'),
        validators=[],
        default='',
        description=_('product model'),
        render_kw={
            'placeholder': _('product model'),
            'rel': 'tooltip',
            'title': _('product model'),
        }
    )
    op = IntegerField(
        _('Option'),
        validators=[],
        default=0,
    )
