#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: supplier_invoice.py
@time: 2018-09-12 15:41
"""


from __future__ import unicode_literals

import time
from datetime import datetime, timedelta
from six import iteritems
from flask_babel import lazy_gettext as _

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, DateTimeField, IntegerField, SelectField, \
    FieldList, FormField
from wtforms.validators import InputRequired, DataRequired, Length, NumberRange, EqualTo, Email, ValidationError, \
    IPAddress


class SupplierInvoiceSearchForm(FlaskForm):
    """
    搜索表单
    """
    supplier_cid = IntegerField(
        _('supplier company id'),
        validators=[
            InputRequired(),
        ],
        default=0,
        description=_('supplier company id'),
        render_kw={
            'rel': 'tooltip',
            'title': _('supplier company id'),
            'placeholder': _('supplier company id'),
            'autocomplete': 'off',
            'type': 'hidden',
        }
    )
    supplier_company_name = StringField(
        _('supplier company name'),
        validators=[],
        description=_('supplier company name'),
        render_kw={
            'placeholder': _('supplier company name'),
            'rel': 'tooltip',
            'title': _('supplier company name'),
        }
    )
    company_tax_id = StringField(
        _('company tax id'),
        validators=[],
        description=_('company tax id'),
        render_kw={
            'placeholder': _('company tax id'),
            'rel': 'tooltip',
            'title': _('company tax id'),
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


class SupplierInvoiceEditForm(FlaskForm):
    """
    编辑表单（字段默认选项需要去除）
    """
    cid = IntegerField(
        _('supplier id'),
        validators=[
            DataRequired(),
        ],
        render_kw={
            'type': 'hidden',
        }
    )
    company_name = StringField(
        _('company name'),
        validators=[
            DataRequired(),
            Length(min=2, max=100),
        ],
        description=_('company name'),
        render_kw={
            'rel': 'tooltip',
            'title': _('company name'),
            'placeholder': _('company name'),
            'autocomplete': 'off',
        }
    )
    company_tax_id = StringField(
        _('company tax id'),
        validators=[
            Length(max=20),
        ],
        description=_('company tax id'),
        render_kw={
            'rel': 'tooltip',
            'title': _('company tax id'),
            'placeholder': _('company tax id'),
            'autocomplete': 'off',
        }
    )
    company_address = StringField(
        _('company address'),
        validators=[
            Length(max=100),
        ],
        description=_('company address'),
        render_kw={
            'rel': 'tooltip',
            'title': _('company address'),
            'placeholder': _('company address'),
            'autocomplete': 'off',
        }
    )
    company_tel = StringField(
        _('company tel'),
        validators=[
            Length(max=100),
        ],
        description=_('company tel'),
        render_kw={
            'rel': 'tooltip',
            'title': _('company tel'),
            'placeholder': _('company tel'),
            'autocomplete': 'off',
        }
    )
    company_bank_name = StringField(
        _('company bank name'),
        validators=[
            Length(max=100),
        ],
        description=_('company bank name'),
        render_kw={
            'rel': 'tooltip',
            'title': _('company bank name'),
            'placeholder': _('company bank name'),
            'autocomplete': 'off',
        }
    )
    company_bank_account = StringField(
        _('company bank account'),
        validators=[
            Length(max=100),
        ],
        description=_('company bank account'),
        render_kw={
            'rel': 'tooltip',
            'title': _('company bank account'),
            'placeholder': _('company bank account'),
            'autocomplete': 'off',
        }
    )
    status_delete = IntegerField(
        _('delete status'),
        validators=[],
        default=0,
        description=_('delete status')
    )
    delete_time = DateField(
        _('delete time'),
        validators=[],
        description=_('delete time')
    )
    create_time = DateField(
        _('create time'),
        validators=[],
        description=_('create time')
    )
    update_time = DateField(
        _('update time'),
        validators=[],
        description=_('update time')
    )
