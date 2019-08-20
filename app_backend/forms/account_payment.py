#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: account_payment.py
@time: 2019-08-20 17:03
"""

from __future__ import unicode_literals

from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, InputRequired


class AccountPaymentSearchForm(FlaskForm):
    """
    搜索表单
    """
    customer_cid = IntegerField(
        _('customer company id'),
        validators=[
            InputRequired(),
        ],
        default=0,
        description=_('customer company id'),
        render_kw={
            'rel': 'tooltip',
            'title': _('customer company id'),
            'placeholder': _('customer company id'),
            'autocomplete': 'off',
            'type': 'hidden',
        }
    )
    customer_company_name = StringField(
        _('customer company name'),
        validators=[],
        description=_('customer company name'),
        render_kw={
            'placeholder': _('customer company name'),
            'rel': 'tooltip',
            'title': _('customer company name'),
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


class AccountPaymentAddForm(FlaskForm):
    """
    创建表单
    """
    customer_cid = IntegerField(
        _('customer company id'),
        validators=[
            DataRequired(),
        ],
        default=0,
        description=_('customer company id'),
        render_kw={
            'rel': 'tooltip',
            'title': _('customer company id'),
            'placeholder': _('customer company id'),
            'autocomplete': 'off',
            'type': 'hidden',
        }
    )
    customer_company_name = StringField(
        _('customer company name'),
        validators=[],
        description=_('customer company name'),
        render_kw={
            'placeholder': _('customer company name'),
            'rel': 'tooltip',
            'title': _('customer company name'),
            'autocomplete': 'off',
        }
    )
    note = StringField(
        _('production note'),
        validators=[],
        default='',
        description='产品备注（例如：最小起订量12个）',
        render_kw={
            'placeholder': _('production note'),
            'rel': 'tooltip',
            'title': _('production note'),
            'autocomplete': 'off',
        }
    )
