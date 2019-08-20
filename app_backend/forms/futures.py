#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: futures.py
@time: 2019-08-13 22:39
"""

from __future__ import unicode_literals

from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, DateField
from wtforms.validators import Optional

from app_common.maps.default import DEFAULT_SEARCH_CHOICES_STR_OPTION


class FuturesSearchForm(FlaskForm):
    production_brand = SelectField(
        _('production brand'),
        validators=[],  # 字符类型，非必填
        default=DEFAULT_SEARCH_CHOICES_STR_OPTION,
        description=_('production brand'),
        render_kw={
            'rel': 'tooltip',
            'title': _('production brand'),
        }
    )
    production_model = StringField(
        _('production model'),
        validators=[],
        description=_('production model'),
        render_kw={
            'placeholder': _('production model'),
            'rel': 'tooltip',
            'title': _('production model'),
            'autocomplete': 'off',
        }
    )
    req_date = DateField(
        _('req date'),
        validators=[Optional()],
        description=_('req date'),
        render_kw={
            'placeholder': _('req date'),
            'type': 'date',
            'rel': 'tooltip',
            'title': _('req date'),
        }
    )
    acc_date = DateField(
        _('acc date'),
        validators=[Optional()],
        description=_('acc date'),
        render_kw={
            'placeholder': _('acc date'),
            'type': 'date',
            'rel': 'tooltip',
            'title': _('acc date'),
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
