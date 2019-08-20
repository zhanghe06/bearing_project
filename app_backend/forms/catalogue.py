#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: catalogue.py
@time: 2018-04-16 21:54
"""

from __future__ import unicode_literals

from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField

from app_common.maps.default import DEFAULT_SEARCH_CHOICES_STR_OPTION


class CatalogueSearchForm(FlaskForm):
    product_brand = SelectField(
        _('product brand'),
        validators=[],  # 字符类型，非必填
        default=DEFAULT_SEARCH_CHOICES_STR_OPTION,
        description=_('product brand'),
        render_kw={
            'rel': 'tooltip',
            'title': _('product brand'),
        }
    )
    product_model = StringField(
        _('product model'),
        validators=[],
        default='',
        description=_('product model'),
        render_kw={
            'placeholder': _('product model'),
            'rel': 'tooltip',
            'title': _('product model'),
        }
    )
    op = IntegerField(
        _('Option'),
        validators=[],
        default=0,
    )
