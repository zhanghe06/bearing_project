#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: cash.py
@time: 2019-08-17 17:35
"""

from __future__ import unicode_literals

from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, \
    DecimalField
from wtforms.validators import InputRequired, DataRequired

from app_common.maps.default import DEFAULT_SEARCH_CHOICES_INT_OPTION


class CashSearchForm(FlaskForm):
    id = SelectField(
        _('cash name'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=DEFAULT_SEARCH_CHOICES_INT_OPTION,
        coerce=int,
        description=_('cash name'),
        render_kw={
            'rel': 'tooltip',
            'title': _('cash name'),
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


class CashAddForm(FlaskForm):
    cash_name = StringField(
        _('cash name'),
        validators=[DataRequired()],
        default='',
        description=_('cash name'),
        render_kw={
            'placeholder': _('cash name'),
            'rel': 'tooltip',
            'title': _('cash name'),
        }
    )
    initial_balance = DecimalField(
        _('initial balance'),
        validators=[],
        default=0.00,
        description=_('initial balance'),
        render_kw={
            'placeholder': _('initial balance'),
            'rel': 'tooltip',
            'title': _('initial balance'),
            'type': 'number',
            'step': 0.01,
            'min': 0.00,
            'max': 99999999.99,
        }
    )
    closing_balance = DecimalField(
        _('closing balance'),
        validators=[],
        default=0.00,
        description=_('closing balance'),
        render_kw={
            'placeholder': _('closing balance'),
            'rel': 'tooltip',
            'title': _('closing balance'),
            'type': 'number',
            'step': 0.01,
            'min': 0.00,
            'max': 99999999.99,
        }
    )
    note = StringField(
        _('cash note'),
        validators=[],
        default='',
        description=_('cash note'),
        render_kw={
            'placeholder': _('cash note'),
            'rel': 'tooltip',
            'title': _('cash note'),
        }
    )


class CashEditForm(CashAddForm):
    pass
