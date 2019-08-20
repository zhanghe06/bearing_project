#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: customer_invoice.py
@time: 2018-08-08 13:27
"""

from __future__ import unicode_literals

from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField
from wtforms.validators import InputRequired, DataRequired, Length


class CustomerInvoiceSearchForm(FlaskForm):
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


class CustomerInvoiceEditForm(FlaskForm):
    """
    编辑表单（字段默认选项需要去除）
    """
    cid = IntegerField(
        _('customer id'),
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
