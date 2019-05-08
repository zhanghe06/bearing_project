#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: price.py
@time: 2018-08-30 19:47
"""


from __future__ import unicode_literals

import time
from datetime import datetime, timedelta
from six import iteritems
from flask_babel import lazy_gettext as _

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, DateTimeField, IntegerField, SelectField
from wtforms.validators import InputRequired, DataRequired, Length, NumberRange, EqualTo, Email, ValidationError, \
    IPAddress, Optional
from app_common.maps.default import default_search_choices_int, default_search_choice_option_int, default_search_choice_option_str
from app_common.maps.type_company import TYPE_COMPANY_DICT

from copy import copy

company_type_choices = copy(default_search_choices_int)
company_type_choices.extend(iteritems(TYPE_COMPANY_DICT))


class PriceSearchForm(FlaskForm):
    """
    搜索表单
    """
    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = True  # enable csrf
        FlaskForm.__init__(self, *args, **kwargs)

    cid = IntegerField(
        _('customer id'),
        validators=[
            InputRequired(),
        ],
        default=0,
        description=_('customer id'),
        render_kw={
            'rel': 'tooltip',
            'title': _('customer id'),
            'placeholder': _('customer id'),
            'autocomplete': 'off',
            'type': 'hidden',
        }
    )
    company_name = StringField(
        _('company name'),
        validators=[],
        description=_('company name'),
        render_kw={
            'placeholder': _('company name'),
            'rel': 'tooltip',
            'title': _('company name'),
        }
    )
    production_model = StringField(
        _('production model'),
        validators=[],
        default='',
        description=_('production model'),
        render_kw={
            'placeholder': _('production model'),
            'rel': 'tooltip',
            'title': _('production model'),
            'autocomplete': 'off',
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
        _('operation'),
        validators=[],
        default=0,
    )
    page = IntegerField(
        _('page'),
        validators=[],
        default=1,
    )
