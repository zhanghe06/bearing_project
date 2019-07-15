#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: supplier.py
@time: 2018-09-12 15:40
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

from app_backend.validators.supplier import AddSupplierCompanyNameRepeatValidate, EditSupplierCompanyNameRepeatValidate
from app_common.maps.default import default_search_choices_int, default_search_choice_option_int
from app_common.maps.type_company import TYPE_COMPANY_DICT

from copy import copy

company_type_choices = copy(default_search_choices_int)
company_type_choices.extend(iteritems(TYPE_COMPANY_DICT))


class SupplierSearchForm(FlaskForm):
    """
    搜索表单
    """
    company_name = StringField(
        _('company name'),
        validators=[],
        description=_('company name'),
        render_kw={
            'placeholder': _('company name'),
            'rel': 'tooltip',
            'title': _('company name'),
            'autocomplete': 'off',
        }
    )
    company_type = SelectField(
        _('company type'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=default_search_choice_option_int,
        coerce=int,
        choices=company_type_choices,
        description=_('company type'),
        render_kw={
            'rel': 'tooltip',
            'title': _('company type'),
        }
    )
    owner_uid = SelectField(
        _('owner uid'),
        default=default_search_choice_option_int,
        # validators=[],
        coerce=int,
        description=_('owner uid'),
        render_kw={
            'rel': 'tooltip',
            'title': _('owner uid'),
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
        _('Option'),
        validators=[],
        default=0,
    )
    page = IntegerField(
        _('page'),
        validators=[],
        default=1,
    )


class SupplierAddForm(FlaskForm):
    """
    创建表单（字段一般带有默认选项）
    """
    company_name = StringField(
        _('company name'),
        validators=[
            DataRequired(),
            Length(min=2, max=100),
            AddSupplierCompanyNameRepeatValidate(),
        ],
        description=_('company name'),
        render_kw={
            'rel': 'tooltip',
            'title': _('company name'),
            'placeholder': _('company name'),
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
    company_site = StringField(
        _('company site'),
        validators=[
            Length(max=100),
        ],
        description=_('company site'),
        render_kw={
            'rel': 'tooltip',
            'title': _('company site'),
            'placeholder': _('company site'),
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
    company_fax = StringField(
        _('company fax'),
        validators=[
            Length(max=100),
        ],
        description=_('company fax'),
        render_kw={
            'rel': 'tooltip',
            'title': _('company fax'),
            'placeholder': _('company fax'),
            'autocomplete': 'off',
        }
    )
    company_email = StringField(
        _('company email'),
        validators=[
            Length(max=100),
        ],
        description=_('company email'),
        render_kw={
            'rel': 'tooltip',
            'title': _('company email'),
            'placeholder': _('company email'),
            'autocomplete': 'off',
        }
    )
    company_type = SelectField(
        _('company type'),
        validators=[
            InputRequired(),
        ],
        default=default_search_choice_option_int,
        coerce=int,
        description=_('company type'),
        render_kw={
            'rel': 'tooltip',
            'title': _('company type'),
            'autocomplete': 'off',
        }
    )
    owner_uid = SelectField(
        _('owner uid'),
        validators=[
            InputRequired(),
        ],
        default=default_search_choice_option_int,
        coerce=int,
        description=_('owner uid'),
        render_kw={
            'rel': 'tooltip',
            'title': _('owner uid'),
            'autocomplete': 'off',
        }
    )


class SupplierEditForm(FlaskForm):
    """
    编辑表单（字段默认选项需要去除）
    """
    id = IntegerField(
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
            EditSupplierCompanyNameRepeatValidate(),
        ],
        description=_('company name'),
        render_kw={
            'rel': 'tooltip',
            'title': _('company name'),
            'placeholder': _('company name'),
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
    company_site = StringField(
        _('company site'),
        validators=[
            Length(max=100),
        ],
        description=_('company site'),
        render_kw={
            'rel': 'tooltip',
            'title': _('company site'),
            'placeholder': _('company site'),
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
    company_fax = StringField(
        _('company fax'),
        validators=[
            Length(max=100),
        ],
        description=_('company fax'),
        render_kw={
            'rel': 'tooltip',
            'title': _('company fax'),
            'placeholder': _('company fax'),
            'autocomplete': 'off',
        }
    )
    company_email = StringField(
        _('company email'),
        validators=[
            Length(max=100),
        ],
        description=_('company email'),
        render_kw={
            'rel': 'tooltip',
            'title': _('company email'),
            'placeholder': _('company email'),
            'autocomplete': 'off',
        }
    )
    company_type = SelectField(
        _('company type'),
        validators=[
            InputRequired(),
        ],
        default=default_search_choice_option_int,
        coerce=int,
        description=_('company type'),
        render_kw={
            'rel': 'tooltip',
            'title': _('company type'),
            'autocomplete': 'off',
        }
    )
    owner_uid = SelectField(
        _('owner uid'),
        validators=[
            InputRequired(),
        ],
        default=default_search_choice_option_int,
        coerce=int,
        description=_('owner uid'),
        render_kw={
            'rel': 'tooltip',
            'title': _('owner uid'),
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
