#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: system.py
@time: 2018-04-12 10:32
"""

from __future__ import unicode_literals

import re
import time
from flask import session
from six import iteritems
from datetime import datetime, timedelta
from flask_babel import lazy_gettext as _

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, DateTimeField, IntegerField, SelectField, \
    FileField
from wtforms.validators import InputRequired, DataRequired, Length, NumberRange, EqualTo, Email, ValidationError, \
    IPAddress

from app_common.maps.type_role import TYPE_ROLE_DICT, TYPE_ROLE_MANAGER
from app_backend.api.user import get_user_rows
from app_common.maps.default import default_search_choices_int, default_search_choice_option_int, default_search_choices_str, \
    default_search_choice_option_str

from copy import copy


class CatalogueUploadForm(FlaskForm):
    file = FileField(
        _('catalogue'),
        validators=[],
        description=_('catalogue'),
        render_kw={
            'rel': 'tooltip',
            'title': _('catalogue'),
        }
    )


class ProductionUploadForm(FlaskForm):
    file = FileField(
        _('production'),
        validators=[],
        description=_('production'),
        render_kw={
            'rel': 'tooltip',
            'title': _('production'),
        }
    )


class QuotationUploadForm(FlaskForm):
    file = FileField(
        _('quotation'),
        validators=[],
        description=_('quotation'),
        render_kw={
            'rel': 'tooltip',
            'title': _('quotation'),
        }
    )
