#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: warehouse.py
@time: 2018-04-06 13:37
"""

from __future__ import unicode_literals

from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import InputRequired, DataRequired

from app_common.maps.default import DEFAULT_SEARCH_CHOICES_INT_OPTION


class WarehouseSearchForm(FlaskForm):
    id = SelectField(
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
    address = StringField(
        _('warehouse address'),
        validators=[],
        default='',
        description=_('warehouse address'),
        render_kw={
            'placeholder': _('warehouse address'),
            'rel': 'tooltip',
            'title': _('warehouse address'),
        }
    )
    linkman = StringField(
        _('warehouse linkman'),
        validators=[],
        default='',
        description=_('warehouse linkman'),
        render_kw={
            'placeholder': _('warehouse linkman'),
            'rel': 'tooltip',
            'title': _('warehouse linkman'),
        }
    )
    tel = StringField(
        _('warehouse tel'),
        validators=[],
        default='',
        description=_('warehouse tel'),
        render_kw={
            'placeholder': _('warehouse tel'),
            'rel': 'tooltip',
            'title': _('warehouse tel'),
        }
    )
    fax = StringField(
        _('warehouse fax'),
        validators=[],
        default='',
        description=_('warehouse fax'),
        render_kw={
            'placeholder': _('warehouse fax'),
            'rel': 'tooltip',
            'title': _('warehouse fax'),
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


class WarehouseAddForm(FlaskForm):
    name = StringField(
        _('warehouse name'),
        validators=[DataRequired()],
        default='',
        description=_('warehouse name'),
        render_kw={
            'placeholder': _('warehouse name'),
            'rel': 'tooltip',
            'title': _('warehouse name'),
        }
    )
    address = StringField(
        _('warehouse address'),
        validators=[],
        default='',
        description=_('warehouse address'),
        render_kw={
            'placeholder': _('warehouse address'),
            'rel': 'tooltip',
            'title': _('warehouse address'),
        }
    )
    linkman = StringField(
        _('warehouse linkman'),
        validators=[],
        default='',
        description=_('warehouse linkman'),
        render_kw={
            'placeholder': _('warehouse linkman'),
            'rel': 'tooltip',
            'title': _('warehouse linkman'),
        }
    )
    tel = StringField(
        _('warehouse tel'),
        validators=[],
        default='',
        description=_('warehouse tel'),
        render_kw={
            'placeholder': _('warehouse tel'),
            'rel': 'tooltip',
            'title': _('warehouse tel'),
        }
    )
    fax = StringField(
        _('warehouse fax'),
        validators=[],
        default='',
        description=_('warehouse fax'),
        render_kw={
            'placeholder': _('warehouse fax'),
            'rel': 'tooltip',
            'title': _('warehouse fax'),
        }
    )


class WarehouseEditForm(WarehouseAddForm):
    pass
