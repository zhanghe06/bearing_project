#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: enquiry_items.py
@time: 2018-09-12 22:18
"""

from __future__ import unicode_literals

from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField
from wtforms.validators import InputRequired, Optional

from app_common.maps.operations import OPERATION_SEARCH


class EnquiryItemsSearchForm(FlaskForm):
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
        default=OPERATION_SEARCH,
    )
    page = IntegerField(
        _('page'),
        validators=[],
        default=1,
    )
