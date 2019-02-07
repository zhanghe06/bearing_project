#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: enquiry_items.py
@time: 2018-09-12 22:18
"""


from __future__ import unicode_literals


# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')


from flask_babel import lazy_gettext as _
from six import iteritems
from datetime import datetime, timedelta

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, DateTimeField, IntegerField, SelectField, \
    DecimalField
from wtforms.validators import InputRequired, DataRequired, Length, NumberRange, EqualTo, Email, ValidationError, \
    IPAddress, Optional
from wtforms.fields import FieldList, FormField

from app_backend.forms import SelectBS, CheckBoxBS
from app_common.maps.type_role import TYPE_ROLE_DICT, TYPE_ROLE_MANAGER
# from app_backend.api.user import get_user_rows
from app_common.maps.default import default_choices_int, default_choice_option_int

from copy import deepcopy

from app_common.maps.type_tax import TYPE_TAX_CHOICES

role_id_choices = deepcopy(default_choices_int)
role_id_choices.extend(iteritems(TYPE_ROLE_DICT))


class EnquiryItemsSearchForm(FlaskForm):
    # uid = SelectField(
    #     _('enquiry user'),
    #     validators=[
    #         InputRequired(),  # 可以为0
    #     ],
    #     default=default_choice_option_int,
    #     coerce=int,
    #     # choices=enquiry_brand_choices,
    #     description=_('enquiry user'),
    #     render_kw={
    #         'rel': 'tooltip',
    #         'title': _('enquiry user'),
    #     }
    # )
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
