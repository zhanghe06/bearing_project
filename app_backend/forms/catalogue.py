#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: catalogue.py
@time: 2018-04-16 21:54
"""


from __future__ import unicode_literals

import re
import time
from flask import session
from six import iteritems
from datetime import datetime, timedelta

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, DateTimeField, IntegerField, SelectField
from wtforms.validators import InputRequired, DataRequired, Length, NumberRange, EqualTo, Email, ValidationError, IPAddress

from app_common.maps.type_role import TYPE_ROLE_DICT, TYPE_ROLE_MANAGER
from app_backend.api.user import get_user_rows
from app_common.maps.default import default_choices_str, default_choice_option_str

from copy import copy


class CatalogueSearchForm(FlaskForm):
    product_brand = SelectField(
        '产品品牌',
        validators=[],  # 字符类型，非必填
        default=default_choice_option_str,
        description='产品品牌',
        render_kw={
            'rel': "tooltip",
            'title': "产品品牌",
        }
    )
    product_model = StringField(
        '产品型号',
        validators=[],
        default='',
        description='产品型号',
        render_kw={
            'placeholder': '产品型号',
            'rel': "tooltip",
            'title': "产品型号",
        }
    )
    op = IntegerField(
        '操作',
        validators=[],
        default=0,
    )

