#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: enquiry.py
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
from wtforms.fields import FieldList, FormField, HiddenField

from app_backend.forms import SelectBS, CheckBoxBS
from app_common.maps.type_role import TYPE_ROLE_DICT, TYPE_ROLE_MANAGER
# from app_backend.api.user import get_user_rows
from app_common.maps.default import default_search_choices_int, default_search_choice_option_int

from copy import deepcopy

from app_common.maps.type_tax import TYPE_TAX_CHOICES

role_id_choices = deepcopy(default_search_choices_int)
role_id_choices.extend(iteritems(TYPE_ROLE_DICT))


class AmountEnquiryValidate(object):
    """
    报价总金额校验（总金额小于1亿）
    报价数量 1-10000
    报价单价 0.00-1000000.00
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        amount_enquiry = 0

        for enquiry_item in form.enquiry_items.entries:
            amount_enquiry += (enquiry_item.form.quantity.data or 0) * (enquiry_item.form.unit_price.data or 0)

        if amount_enquiry >= 100000000:
            # raise ValidationError(self.message or _('Data limit exceeded'))
            # TODO why? 使用翻译报错 unicode l'' 这是什么类型
            raise ValidationError(self.message or '数据超出限制')


class EnquirySearchForm(FlaskForm):
    uid = SelectField(
        _('enquiry user'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=default_search_choice_option_int,
        coerce=int,
        # choices=enquiry_brand_choices,
        description=_('enquiry user'),
        render_kw={
            'rel': 'tooltip',
            'title': _('enquiry user'),
        }
    )
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


class EnquiryItemAddForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False  # disable csrf
        FlaskForm.__init__(self, *args, **kwargs)

    enquiry_id = IntegerField(
        _('enquiry id'),
        validators=[
        ],
        render_kw={
            'placeholder': _('enquiry id'),
            'rel': "tooltip",
            'title': _('enquiry id'),
        }
    )
    enquiry_production_model = StringField(
        _('enquiry production model'),
        validators=[],
        default='',
        description=_('enquiry production model'),
        render_kw={
            'placeholder': _('enquiry production model'),
            'rel': 'tooltip',
            'title': _('enquiry production model'),
            'autocomplete': 'off',
        }
    )
    enquiry_quantity = IntegerField(
        _('enquiry quantity'),
        validators=[],
        default=1,
        description=_('enquiry quantity'),
        render_kw={
            'placeholder': _('enquiry quantity'),
            'rel': 'tooltip',
            'title': _('enquiry quantity'),
            'type': 'number',
            'step': 1,
            'min': 1,
            'max': 10000,
        }
    )
    production_id = IntegerField(
        _('production id'),
        validators=[
            InputRequired(),  # 可以为0 询价时可能不确认具体型号
        ],
        default=0,
        render_kw={
            'placeholder': _('production id'),
            'rel': "tooltip",
            'title': _('production id'),
            'readonly': 'readonly',
            'type': 'hidden',
        }
    )
    production_brand = StringField(
        _('production brand'),
        validators=[],
        default='',
        description=_('production brand'),
        render_kw={
            'placeholder': _('production brand'),
            'rel': 'tooltip',
            'title': _('production brand'),
            'readonly': 'readonly',
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
    production_sku = StringField(
        _('production sku'),
        validators=[],
        default='',
        description=_('production sku'),
        render_kw={
            'placeholder': _('production sku'),
            'rel': 'tooltip',
            'title': _('production sku'),
            'readonly': 'readonly',
        }
    )
    quantity = IntegerField(
        _('quantity'),
        validators=[],
        default=1,
        description=_('quantity'),
        render_kw={
            'placeholder': _('quantity'),
            'rel': 'tooltip',
            'title': _('quantity'),
            'type': 'number',
            'step': 1,
            'min': 1,
            'max': 10000,
        }
    )
    unit_price = DecimalField(
        _('unit price'),
        validators=[],
        default=0.00,
        description=_('unit price'),
        render_kw={
            'placeholder': _('unit price'),
            'rel': 'tooltip',
            'title': _('unit price'),
            'type': 'number',
            'step': 0.01,
            'min': 0.00,
            'max': 1000000.00,
        }
    )
    note = StringField(
        _('note'),
        validators=[],
        default='',
        description=_('note'),
        render_kw={
            'placeholder': _('note'),
            'rel': 'tooltip',
            'title': _('note'),
        }
    )
    delivery_time = StringField(
        _('delivery time'),
        validators=[],
        default='',
        description=_('delivery time'),
        render_kw={
            'placeholder': _('delivery time'),
            'rel': 'tooltip',
            'title': _('delivery time'),
        }
    )
    status_ordered = BooleanField(
        _('ordered status'),
        default=False,
        validators=[],
        render_kw={
            'rel': 'tooltip',
            'title': _('ordered status'),
        }
    )


class EnquiryItemEditForm(EnquiryItemAddForm):
    id = IntegerField(
        _('production id'),
        validators=[
            InputRequired(),
        ],
        default=0,
        render_kw={
            'type': 'hidden',
        }
    )


class EnquiryAddForm(FlaskForm):
    uid = SelectField(
        _('enquiry user'),
        validators=[
            DataRequired(),
        ],
        coerce=int,
        description=_('enquiry user'),
        render_kw={
            'rel': 'tooltip',
            'title': _('enquiry user'),
        }
    )
    supplier_cid = IntegerField(
        _('supplier company id'),
        validators=[
            DataRequired(),
        ],
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
    supplier_contact_id = IntegerField(
        _('supplier contact id'),
        validators=[
            DataRequired(),
        ],
        description=_('supplier contact id'),
        render_kw={
            'rel': 'tooltip',
            'title': _('supplier contact id'),
            'type': 'hidden',
        }
    )
    supplier_contact_name = StringField(
        _('supplier contact name'),
        validators=[],
        description=_('supplier contact name'),
        render_kw={
            'placeholder': _('supplier contact name'),
            'rel': 'tooltip',
            'title': _('supplier contact name'),
        }
    )
    delivery_way = StringField(
        _('delivery way'),
        validators=[],
        description=_('delivery way'),
        render_kw={
            'placeholder': _('delivery way'),
            'rel': 'tooltip',
            'title': _('delivery way'),
        }
    )
    note = StringField(
        _('enquiry note'),
        validators=[],
        description=_('enquiry note'),
        render_kw={
            'placeholder': _('enquiry note'),
            'rel': 'tooltip',
            'title': _('enquiry note'),
        }
    )
    status_order = SelectField(
        _('order status'),
        validators=[
            InputRequired(),
        ],
        coerce=int,
        description=_('order status'),
        render_kw={
            'rel': 'tooltip',
            'title': _('order status'),
        }
    )
    amount_enquiry = DecimalField(
        _('amount enquiry'),
        validators=[
            AmountEnquiryValidate()
        ],
        description=_('amount enquiry'),
        render_kw={
            'placeholder': _('amount enquiry'),
            'rel': 'tooltip',
            'title': _('amount enquiry'),
            'type': 'number',
            'disabled': 'disabled',
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
    enquiry_items = FieldList(
        FormField(EnquiryItemAddForm),
        label='报价明细',
        min_entries=1,
        max_entries=12,
    )


class EnquiryEditForm(FlaskForm):
    uid = SelectField(
        _('enquiry user'),
        validators=[],
        coerce=int,
        description=_('enquiry user'),
        render_kw={
            'rel': 'tooltip',
            'title': _('enquiry user'),
        }
    )
    supplier_cid = IntegerField(
        _('supplier company id'),
        validators=[
            DataRequired(),
        ],
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
    supplier_contact_id = IntegerField(
        _('supplier contact id'),
        validators=[
            DataRequired(),
        ],
        # default=0,
        description=_('supplier contact id'),
        render_kw={
            'rel': 'tooltip',
            'title': _('supplier contact id'),
            'type': 'hidden',
        }
    )
    supplier_contact_name = StringField(
        _('supplier contact name'),
        validators=[],
        description=_('supplier contact name'),
        render_kw={
            'placeholder': _('supplier contact name'),
            'rel': 'tooltip',
            'title': _('supplier contact name'),
        }
    )
    delivery_way = StringField(
        _('delivery way'),
        validators=[],
        description=_('delivery way'),
        render_kw={
            'placeholder': _('delivery way'),
            'rel': 'tooltip',
            'title': _('delivery way'),
        }
    )
    note = StringField(
        _('enquiry note'),
        validators=[],
        description=_('enquiry note'),
        render_kw={
            'placeholder': _('enquiry note'),
            'rel': 'tooltip',
            'title': _('enquiry note'),
        }
    )
    status_order = SelectField(
        _('order status'),
        validators=[
            InputRequired(),
        ],
        coerce=int,
        description=_('order status'),
        render_kw={
            'rel': 'tooltip',
            'title': _('order status'),
        }
    )
    amount_enquiry = DecimalField(
        _('amount enquiry'),
        validators=[
            AmountEnquiryValidate()
        ],
        description=_('amount enquiry'),
        render_kw={
            'placeholder': _('amount enquiry'),
            'rel': 'tooltip',
            'title': _('amount enquiry'),
            'type': 'number',
            'readonly': 'readonly',
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
    enquiry_items = FieldList(
        FormField(EnquiryItemEditForm),
        label='报价明细',
        min_entries=1,
        max_entries=12,
    )
