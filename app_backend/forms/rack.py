#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: rack.py
@time: 2018-04-06 18:22
"""

from __future__ import unicode_literals

from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import InputRequired, DataRequired

from app_common.maps.default import DEFAULT_SEARCH_CHOICES_INT_OPTION


class RackSearchForm(FlaskForm):
    warehouse_id = SelectField(
        _('warehouse name'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=DEFAULT_SEARCH_CHOICES_INT_OPTION,
        coerce=int,
        description=_('warehouse name'),
        render_kw={
            'rel': 'tooltip',
            'title': _('warehouse name'),
        }
    )
    name = StringField(
        _('rack name'),
        validators=[],
        default='',
        description=_('rack name'),
        render_kw={
            'placeholder': _('rack name'),
            'rel': 'tooltip',
            'title': _('rack name'),
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


class RackAddForm(FlaskForm):
    warehouse_id = SelectField(
        _('warehouse name'),
        validators=[
            DataRequired(),
        ],
        default=DEFAULT_SEARCH_CHOICES_INT_OPTION,
        coerce=int,
        description=_('warehouse name'),
        render_kw={
            'rel': 'tooltip',
            'title': _('warehouse name'),
        }
    )
    name = StringField(
        _('rack name'),
        validators=[],
        default='',
        description=_('rack name'),
        render_kw={
            'placeholder': _('rack name'),
            'rel': 'tooltip',
            'title': _('rack name'),
        }
    )


class RackEditForm(RackAddForm):
    pass
