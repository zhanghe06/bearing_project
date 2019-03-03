#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: warehouse.py
@time: 2018-04-06 13:37
"""

from __future__ import unicode_literals

import re
import time
from flask import session
from six import iteritems
from datetime import datetime, timedelta
from flask_babel import lazy_gettext as _

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, DateTimeField, IntegerField, SelectField
from wtforms.validators import InputRequired, DataRequired, Length, NumberRange, EqualTo, Email, ValidationError, \
    IPAddress

from app_common.maps.type_role import TYPE_ROLE_DICT, TYPE_ROLE_MANAGER
from app_backend.api.user import get_user_rows
from app_common.maps.default import default_search_choices_int, default_search_choice_option_int

from copy import copy


class WarehouseSearchForm(FlaskForm):
    id = SelectField(
        _('warehouse name'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=default_search_choice_option_int,
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
        '仓库名称',
        validators=[DataRequired()],
        default='',
        description='仓库名称',
        render_kw={
            'placeholder': '仓库名称',
            'rel': "tooltip",
            'title': "仓库名称",
        }
    )
    address = StringField(
        '仓库地址',
        validators=[],
        default='',
        description='仓库地址',
        render_kw={
            'placeholder': '仓库地址',
            'rel': "tooltip",
            'title': "仓库地址",
        }
    )
    linkman = StringField(
        '仓管人员',
        validators=[],
        default='',
        description='仓管人员',
        render_kw={
            'placeholder': '仓管人员',
            'rel': "tooltip",
            'title': "仓管人员",
        }
    )
    tel = StringField(
        '仓库电话',
        validators=[],
        default='',
        description='仓库电话',
        render_kw={
            'placeholder': '仓库电话',
            'rel': "tooltip",
            'title': "仓库电话",
        }
    )
    fax = StringField(
        '仓库传真',
        validators=[],
        default='',
        description='仓库传真',
        render_kw={
            'placeholder': '仓库传真',
            'rel': "tooltip",
            'title': "仓库传真",
        }
    )


class WarehouseEditForm(FlaskForm):
    id = IntegerField(
        '仓库编号',
        validators=[
            DataRequired(),
        ],
        render_kw={
            'type': 'hidden',
        }
    )
    name = StringField(
        '仓库名称',
        validators=[DataRequired()],
        default='',
        description='仓库名称',
        render_kw={
            'placeholder': '仓库名称',
            'rel': "tooltip",
            'title': "仓库名称",
        }
    )
    address = StringField(
        '仓库地址',
        validators=[],
        default='',
        description='仓库地址',
        render_kw={
            'placeholder': '仓库地址',
            'rel': "tooltip",
            'title': "仓库地址",
        }
    )
    linkman = StringField(
        '仓管人员',
        validators=[],
        default='',
        description='仓管人员',
        render_kw={
            'placeholder': '仓管人员',
            'rel': "tooltip",
            'title': "仓管人员",
        }
    )
    tel = StringField(
        '仓库电话',
        validators=[],
        default='',
        description='仓库电话',
        render_kw={
            'placeholder': '仓库电话',
            'rel': "tooltip",
            'title': "仓库电话",
        }
    )
    fax = StringField(
        '仓库传真',
        validators=[],
        default='',
        description='仓库传真',
        render_kw={
            'placeholder': '仓库传真',
            'rel': "tooltip",
            'title': "仓库传真",
        }
    )
    create_time = DateField(
        '创建时间',
        validators=[DataRequired()],
        description='创建时间'
    )
    update_time = DateField(
        '更新时间',
        validators=[DataRequired()],
        description='更新时间'
    )
