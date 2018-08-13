#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: customer_contact.py
@time: 2018-08-08 13:27
"""


from __future__ import unicode_literals

import time
from datetime import datetime, timedelta
from six import iteritems
from flask_babel import lazy_gettext as _

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, DateTimeField, IntegerField, SelectField, \
    FieldList, FormField
from wtforms.validators import InputRequired, DataRequired, Length, NumberRange, EqualTo, Email, ValidationError, \
    IPAddress
from app_common.maps.default import default_choices_int, default_choice_option_int
from app_common.maps.type_company import TYPE_COMPANY_DICT

from copy import copy

company_type_choices = copy(default_choices_int)
company_type_choices.extend(iteritems(TYPE_COMPANY_DICT))


class DefaultStatusValidate(object):
    """
    默认状态校验
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        # 获取默认状态数量
        default_status_count = 0

        for customer_contact_item in form.customer_contact_items.entries:
            default_status_count += int(customer_contact_item.form.status_default.data)

        # 数量 < 1
        if default_status_count < 1:
            # 必须指定一个默认联系方式
            for customer_contact_item in form.customer_contact_items.entries:
                customer_contact_item.form.status_default.errors = ['必须指定一个默认联系方式']
            # raise ValidationError(self.message or _('Must specify a default customer contact'))

        # 数量 > 1
        if default_status_count > 1:
            # 仅能指定一个默认联系方式
            for customer_contact_item in form.customer_contact_items.entries:
                customer_contact_item.form.status_default.errors = ['仅能指定一个默认联系方式']
            # raise ValidationError(self.message or _('Only specify one default customer contact'))


class CustomerContactSearchForm(FlaskForm):
    """
    搜索表单
    """
    cid = IntegerField(
        _('customer id'),
        validators=[
            InputRequired(),
        ],
        default=0,
        description=_('customer id'),
        render_kw={
            'rel': 'tooltip',
            'title': _('customer id'),
            'placeholder': _('customer id'),
            'autocomplete': 'off',
            'type': 'hidden',
        }
    )
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
    contact_name = StringField(
        _('contact name'),
        validators=[],
        description=_('contact name'),
        render_kw={
            'placeholder': _('contact name'),
            'rel': 'tooltip',
            'title': _('contact name'),
            'autocomplete': 'off',
        }
    )
    address = StringField(
        _('address'),
        validators=[],
        description=_('address'),
        render_kw={
            'placeholder': _('address'),
            'rel': 'tooltip',
            'title': _('address'),
            'autocomplete': 'off',
        }
    )
    mobile = StringField(
        _('mobile'),
        validators=[],
        description=_('mobile'),
        render_kw={
            'placeholder': _('mobile'),
            'rel': 'tooltip',
            'title': _('mobile'),
            'autocomplete': 'off',
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


# class CustomerContactItemAddForm(FlaskForm):
#     def __init__(self, *args, **kwargs):
#         kwargs['csrf_enabled'] = False  # disable csrf
#         FlaskForm.__init__(self, *args, **kwargs)
#
#     contact_name = StringField(
#         _('contact name'),
#         validators=[
#             DataRequired(),
#             Length(min=1, max=20),
#         ],
#         description=_('contact name'),
#         render_kw={
#             'rel': 'tooltip',
#             'title': _('contact name'),
#             'placeholder': _('contact name'),
#             'autocomplete': 'off',
#         }
#     )
#     salutation = StringField(
#         _('salutation'),
#         validators=[
#             Length(max=20),
#         ],
#         description=_('salutation'),
#         render_kw={
#             'rel': 'tooltip',
#             'title': _('salutation'),
#             'placeholder': _('salutation'),
#             'autocomplete': 'off',
#         }
#     )
#     mobile = StringField(
#         _('mobile'),
#         validators=[
#             Length(max=20),
#         ],
#         description=_('mobile'),
#         render_kw={
#             'rel': 'tooltip',
#             'title': _('mobile'),
#             'placeholder': _('mobile'),
#             'autocomplete': 'off',
#         }
#     )
#     tel = StringField(
#         _('tel'),
#         validators=[
#             Length(max=20),
#         ],
#         description=_('tel'),
#         render_kw={
#             'rel': 'tooltip',
#             'title': _('tel'),
#             'placeholder': _('tel'),
#             'autocomplete': 'off',
#         }
#     )
#     fax = StringField(
#         _('fax'),
#         validators=[
#             Length(max=20),
#         ],
#         description=_('fax'),
#         render_kw={
#             'rel': 'tooltip',
#             'title': _('fax'),
#             'placeholder': _('fax'),
#             'autocomplete': 'off',
#         }
#     )
#     address = StringField(
#         _('address'),
#         validators=[
#             DataRequired(),
#             Length(max=100),
#         ],
#         description=_('address'),
#         render_kw={
#             'rel': 'tooltip',
#             'title': _('address'),
#             'placeholder': _('address'),
#             'autocomplete': 'off',
#         }
#     )
#     note = StringField(
#         _('note'),
#         validators=[
#             Length(max=256),
#         ],
#         description=_('note'),
#         render_kw={
#             'rel': 'tooltip',
#             'title': _('note'),
#             'placeholder': _('note'),
#             'autocomplete': 'off',
#         }
#     )
#     status_default = BooleanField(_('default status'), default=False)
#
#
# class CustomerContactAddForm(FlaskForm):
#     """
#     创建表单（字段一般带有默认选项）
#     """
#     cid = IntegerField(
#         _('customer id'),
#         validators=[
#             DataRequired(),
#         ],
#         render_kw={
#             'type': 'hidden',
#         }
#     )
#     company_name = StringField(
#         _('company name'),
#         validators=[],
#         description=_('company name'),
#         render_kw={
#             'placeholder': _('company name'),
#             'rel': 'tooltip',
#             'title': _('company name'),
#         }
#     )
#     data_line_add = IntegerField(
#         '数据行新增',
#         validators=[],
#     )
#     data_line_del = IntegerField(
#         '数据行删除',
#         validators=[],
#     )
#     customer_contact_items = FieldList(
#         FormField(CustomerContactItemAddForm),
#         label='联系方式明细',
#         min_entries=1,
#     )


class CustomerContactItemEditForm(FlaskForm):
    """
    编辑表单（字段默认选项需要去除）
    """
    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False  # disable csrf
        FlaskForm.__init__(self, *args, **kwargs)

    id = IntegerField(
        _('customer contact id'),
        validators=[],
        default=0,
        render_kw={
            'type': 'hidden',
        }
    )
    cid = IntegerField(
        _('customer id'),
        validators=[],
        default=0,
        render_kw={
            'type': 'hidden',
        }
    )
    company_name = StringField(
        _('company name'),
        validators=[],
        description=_('company name'),
        render_kw={
            'placeholder': _('company name'),
            'rel': 'tooltip',
            'title': _('company name'),
        }
    )
    contact_name = StringField(
        _('contact name'),
        validators=[
            DataRequired(),
            Length(min=1, max=20),
        ],
        description=_('contact name'),
        render_kw={
            'rel': 'tooltip',
            'title': _('contact name'),
            'placeholder': _('contact name'),
            'autocomplete': 'off',
        }
    )
    salutation = StringField(
        _('salutation'),
        validators=[
            Length(max=20),
        ],
        description=_('salutation'),
        render_kw={
            'rel': 'tooltip',
            'title': _('salutation'),
            'placeholder': _('salutation'),
            'autocomplete': 'off',
        }
    )
    mobile = StringField(
        _('mobile'),
        validators=[
            Length(max=20),
        ],
        description=_('mobile'),
        render_kw={
            'rel': 'tooltip',
            'title': _('mobile'),
            'placeholder': _('mobile'),
            'autocomplete': 'off',
        }
    )
    tel = StringField(
        _('tel'),
        validators=[
            Length(max=20),
        ],
        description=_('tel'),
        render_kw={
            'rel': 'tooltip',
            'title': _('tel'),
            'placeholder': _('tel'),
            'autocomplete': 'off',
        }
    )
    fax = StringField(
        _('fax'),
        validators=[
            Length(max=20),
        ],
        description=_('fax'),
        render_kw={
            'rel': 'tooltip',
            'title': _('fax'),
            'placeholder': _('fax'),
            'autocomplete': 'off',
        }
    )
    address = StringField(
        _('address'),
        validators=[
            Length(max=100),
        ],
        description=_('address'),
        render_kw={
            'rel': 'tooltip',
            'title': _('address'),
            'placeholder': _('address'),
            'autocomplete': 'off',
        }
    )
    note = StringField(
        _('note'),
        validators=[
            Length(max=256),
        ],
        description=_('note'),
        render_kw={
            'rel': 'tooltip',
            'title': _('note'),
            'placeholder': _('note'),
            'autocomplete': 'off',
        }
    )
    status_default = BooleanField(
        _('default status'),
        default=False,
        validators=[],
        render_kw={
            'rel': 'tooltip',
            'title': _('default status'),
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


class CustomerContactEditForm(FlaskForm):
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
        validators=[],
        description=_('company name'),
        render_kw={
            'placeholder': _('company name'),
            'rel': 'tooltip',
            'title': _('company name'),
        }
    )
    data_line_add = IntegerField(
        '数据行新增',
        validators=[],
    )
    data_line_del = IntegerField(
        '数据行删除',
        validators=[],
    )
    customer_contact_items = FieldList(
        FormField(CustomerContactItemEditForm),
        label='联系方式明细',
        min_entries=1,
        validators=[DefaultStatusValidate()],

    )
