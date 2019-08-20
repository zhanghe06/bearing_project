#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: bank_account.py
@time: 2019-08-17 17:35
"""

from __future__ import unicode_literals

from copy import deepcopy

from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SelectField, \
    DecimalField
from wtforms.validators import InputRequired, NumberRange, Optional

from app_backend.api.bank import (
    get_bank_choices,
    # bank_current_stats,
    # bank_former_stats,
)
from app_common.maps.default import DEFAULT_SEARCH_CHOICES_INT, DEFAULT_SEARCH_CHOICES_INT_OPTION
from app_common.maps.type_account import TYPE_ACCOUNT_SEARCH_CHOICES, TYPE_ACCOUNT_SELECT_CHOICES
from app_common.maps.type_current import TYPE_CURRENT_SEARCH_CHOICES, TYPE_CURRENT_SELECT_CHOICES



class BankAccountSearchForm(FlaskForm):
    bank_id = SelectField(
        _('bank account name'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=DEFAULT_SEARCH_CHOICES_INT_OPTION,
        coerce=int,
        description=_('bank account name'),
        render_kw={
            'rel': 'tooltip',
            'title': _('bank account name'),
        }
    )
    type_current = SelectField(
        _('current type'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=DEFAULT_SEARCH_CHOICES_INT_OPTION,
        coerce=int,
        choices=TYPE_CURRENT_SEARCH_CHOICES,
        description=_('current type'),
        render_kw={
            'rel': 'tooltip',
            'title': _('current type'),
        }
    )
    type_account = SelectField(
        _('account type'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=DEFAULT_SEARCH_CHOICES_INT_OPTION,
        coerce=int,
        choices=TYPE_ACCOUNT_SEARCH_CHOICES,
        description=_('account type'),
        render_kw={
            'rel': 'tooltip',
            'title': _('account type'),
        }
    )
    start_record_date = DateField(
        _('start date'),
        validators=[Optional()],
        # default=datetime.utcnow() - timedelta(days=365),
        description=_('start date'),
        render_kw={
            'placeholder': _('start date'),
            'type': 'date',
            'rel': 'tooltip',
            'title': _('start date'),
        }
    )
    end_record_date = DateField(
        _('end date'),
        validators=[Optional()],
        # default=datetime.utcnow() + timedelta(days=1),
        description=_('end date'),
        render_kw={
            'placeholder': _('end date'),
            'type': 'date',
            'rel': 'tooltip',
            'title': _('end date'),
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


class BankAccountAddForm(FlaskForm):
    bank_id = SelectField(
        _('user role'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=DEFAULT_SEARCH_CHOICES_INT_OPTION,
        coerce=int,
        choices=get_bank_choices('create'),
        description=_('user role'),
        render_kw={
            'rel': 'tooltip',
            'title': _('user role'),
        }
    )
    type_current = SelectField(
        _('current type'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=DEFAULT_SEARCH_CHOICES_INT_OPTION,
        coerce=int,
        choices=TYPE_CURRENT_SELECT_CHOICES,
        description=_('current type'),
        render_kw={
            'rel': 'tooltip',
            'title': _('current type'),
        }
    )
    type_account = SelectField(
        _('account type'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=DEFAULT_SEARCH_CHOICES_INT_OPTION,
        coerce=int,
        choices=TYPE_ACCOUNT_SELECT_CHOICES,
        description=_('account type'),
        render_kw={
            'rel': 'tooltip',
            'title': _('account type'),
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
    amount = DecimalField(
        _('amount'),
        validators=[
            NumberRange(
                min=0.00,
                max=99999999.99
            )
        ],
        default=0.00,
        description=_('amount'),
        render_kw={
            'placeholder': _('amount'),
            'rel': 'tooltip',
            'title': _('amount'),
            'type': 'number',
            'step': 0.01,
            'min': 0.00,
            'max': 99999999.99,
        }
    )
    record_date = DateField(
        _('record date'),
        validators=[Optional()],
        description=_('record date'),
        render_kw={
            'placeholder': _('record date'),
            'type': 'date',
            'rel': 'tooltip',
            'title': _('record date'),
        }
    )


class BankAccountEditForm(BankAccountAddForm):
    pass
