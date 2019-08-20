#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: bank.py
@time: 2019-08-17 17:35
"""

from __future__ import unicode_literals

from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, \
    DecimalField
from wtforms.validators import InputRequired, DataRequired

from app_common.maps.default import DEFAULT_SEARCH_CHOICES_INT_OPTION
from app_common.maps.type_bank import TYPE_BANK_SEARCH_CHOICES, TYPE_BANK_SELECT_CHOICES


class BankSearchForm(FlaskForm):
    id = SelectField(
        _('bank name'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=DEFAULT_SEARCH_CHOICES_INT_OPTION,
        coerce=int,
        description=_('bank name'),
        render_kw={
            'rel': 'tooltip',
            'title': _('bank name'),
        }
    )
    type_bank = SelectField(
        _('bank type'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=DEFAULT_SEARCH_CHOICES_INT_OPTION,
        coerce=int,
        choices=TYPE_BANK_SEARCH_CHOICES,
        description=_('bank type'),
        render_kw={
            'rel': 'tooltip',
            'title': _('bank type'),
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


class BankAddForm(FlaskForm):
    bank_name = StringField(
        _('bank name'),
        validators=[DataRequired()],
        default='',
        description=_('bank name'),
        render_kw={
            'placeholder': _('bank name'),
            'rel': 'tooltip',
            'title': _('bank name'),
        }
    )
    type_bank = SelectField(
        _('bank type'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=DEFAULT_SEARCH_CHOICES_INT_OPTION,
        coerce=int,
        choices=TYPE_BANK_SELECT_CHOICES,
        description=_('bank type'),
        render_kw={
            'rel': 'tooltip',
            'title': _('bank type'),
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
        _('bank note'),
        validators=[],
        default='',
        description=_('bank note'),
        render_kw={
            'placeholder': _('bank note'),
            'rel': 'tooltip',
            'title': _('bank note'),
        }
    )


class BankEditForm(BankAddForm):
    pass
