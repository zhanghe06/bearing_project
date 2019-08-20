#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: sales_order.py
@time: 2018-08-31 18:05
"""

from __future__ import unicode_literals

from copy import copy

from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from six import iteritems
from wtforms import StringField, BooleanField, DateField, IntegerField, SelectField, \
    DecimalField
from wtforms.fields import FieldList, FormField
from wtforms.validators import InputRequired, DataRequired, ValidationError, \
    Optional

# from app_backend.api.user import get_user_rows
from app_common.maps.default import DEFAULT_SEARCH_CHOICES_INT, DEFAULT_SEARCH_CHOICES_INT_OPTION
from app_common.maps.type_role import TYPE_ROLE_DICT

# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

role_id_choices = copy(DEFAULT_SEARCH_CHOICES_INT)
role_id_choices.extend(iteritems(TYPE_ROLE_DICT))


class AmountSalesOrderValidate(object):
    """
    订单总金额校验（总金额小于1亿）
    订单数量 1-10000
    订单单价 0.00-1000000.00
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        amount_sales_orders = 0

        for sales_order_item in form.sales_order_items.entries:
            amount_sales_orders += (sales_order_item.form.quantity.data or 0) * (
                sales_order_item.form.unit_price.data or 0)

        if amount_sales_orders >= 100000000:
            # raise ValidationError(self.message or _('Data limit exceeded'))
            # TODO why? 使用翻译报错 unicode l'' 这是什么类型
            raise ValidationError(self.message or '数据超出限制')


class SalesOrderSearchForm(FlaskForm):
    uid = SelectField(
        _('sales order user'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=DEFAULT_SEARCH_CHOICES_INT_OPTION,
        coerce=int,
        # choices=sales_order_brand_choices,
        description=_('sales order user'),
        render_kw={
            'rel': 'tooltip',
            'title': _('sales order user'),
        }
    )
    customer_cid = IntegerField(
        _('customer company id'),
        validators=[
            InputRequired(),
        ],
        default=0,
        description=_('customer company id'),
        render_kw={
            'rel': 'tooltip',
            'title': _('customer company id'),
            'placeholder': _('customer company id'),
            'autocomplete': 'off',
            'type': 'hidden',
        }
    )
    customer_company_name = StringField(
        _('customer company name'),
        validators=[],
        description=_('customer company name'),
        render_kw={
            'placeholder': _('customer company name'),
            'rel': 'tooltip',
            'title': _('customer company name'),
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


class SalesOrderItemAddForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False  # disable csrf
        FlaskForm.__init__(self, *args, **kwargs)

    sales_order_id = IntegerField(
        _('sales order id'),
        validators=[
        ],
        render_kw={
            'placeholder': _('sales order id'),
            'rel': "tooltip",
            'title': _('sales order id'),
        }
    )
    custom_production_brand = StringField(
        _('custom production brand'),
        validators=[],
        default='',
        description=_('custom production brand'),
        render_kw={
            'placeholder': _('custom production brand'),
            'rel': 'tooltip',
            'title': _('custom production brand'),
            'readonly': 'readonly',
        }
    )
    custom_production_model = StringField(
        _('custom production model'),
        validators=[],
        default='',
        description=_('custom production model'),
        render_kw={
            'placeholder': _('custom production model'),
            'rel': 'tooltip',
            'title': _('custom production model'),
            'autocomplete': 'off',
        }
    )
    production_id = IntegerField(
        _('production id'),
        validators=[
            DataRequired(),
        ],
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
    type_tax = BooleanField(
        _('type tax'),
        default=True,
        validators=[],
        render_kw={
            'rel': 'tooltip',
            'title': _('type tax'),
            'checked': 'checked',
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


class SalesOrderItemEditForm(SalesOrderItemAddForm):
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


class SalesOrderAddForm(FlaskForm):
    uid = SelectField(
        _('sales order user'),
        validators=[
            DataRequired(),
        ],
        coerce=int,
        description=_('sales order user'),
        render_kw={
            'rel': 'tooltip',
            'title': _('sales order user'),
        }
    )
    customer_cid = IntegerField(
        _('customer company id'),
        validators=[
            DataRequired(),
        ],
        description=_('customer company id'),
        render_kw={
            'rel': 'tooltip',
            'title': _('customer company id'),
            'placeholder': _('customer company id'),
            'autocomplete': 'off',
            'type': 'hidden',
        }
    )
    customer_company_name = StringField(
        _('customer company name'),
        validators=[],
        description=_('customer company name'),
        render_kw={
            'placeholder': _('customer company name'),
            'rel': 'tooltip',
            'title': _('customer company name'),
        }
    )
    customer_contact_id = IntegerField(
        _('customer contact id'),
        validators=[
            DataRequired(),
        ],
        # default=0,
        description=_('customer contact id'),
        render_kw={
            'rel': 'tooltip',
            'title': _('customer contact id'),
            'type': 'hidden',
        }
    )
    customer_contact_name = StringField(
        _('customer contact name'),
        validators=[],
        description=_('customer contact name'),
        render_kw={
            'placeholder': _('customer contact name'),
            'rel': 'tooltip',
            'title': _('customer contact name'),
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
    type_tax = BooleanField(
        _('type tax'),
        default=True,
        validators=[],
        render_kw={
            'rel': 'tooltip',
            'title': _('type tax'),
            'checked': 'checked',
        }
    )
    note = StringField(
        _('sales order note'),
        validators=[],
        description=_('sales order note'),
        render_kw={
            'placeholder': _('sales order note'),
            'rel': 'tooltip',
            'title': _('sales order note'),
        }
    )
    # status_order = SelectField(
    #     _('sales order status'),
    #     validators=[
    #         InputRequired(),
    #     ],
    #     coerce=int,
    #     description=_('sales order status'),
    #     render_kw={
    #         'rel': 'tooltip',
    #         'title': _('sales order status'),
    #     }
    # )
    amount_order = DecimalField(
        _('amount order'),
        validators=[
            AmountSalesOrderValidate()
        ],
        description=_('amount order'),
        render_kw={
            'placeholder': _('amount order'),
            'rel': 'tooltip',
            'title': _('amount order'),
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
    sales_order_items = FieldList(
        FormField(SalesOrderItemAddForm),
        label='报价明细',
        min_entries=1,
        max_entries=12,
    )


class SalesOrderEditForm(FlaskForm):
    uid = SelectField(
        _('sales order user'),
        validators=[],
        coerce=int,
        description=_('sales order user'),
        render_kw={
            'rel': 'tooltip',
            'title': _('sales order user'),
        }
    )
    customer_cid = IntegerField(
        _('customer company id'),
        validators=[
            DataRequired(),
        ],
        description=_('customer company id'),
        render_kw={
            'rel': 'tooltip',
            'title': _('customer company id'),
            'placeholder': _('customer company id'),
            'autocomplete': 'off',
            'type': 'hidden',
        }
    )
    customer_company_name = StringField(
        _('customer company name'),
        validators=[],
        description=_('customer company name'),
        render_kw={
            'placeholder': _('customer company name'),
            'rel': 'tooltip',
            'title': _('customer company name'),
        }
    )
    customer_contact_id = IntegerField(
        _('customer contact id'),
        validators=[
            DataRequired(),
        ],
        # default=0,
        description=_('customer contact id'),
        render_kw={
            'rel': 'tooltip',
            'title': _('customer contact id'),
            'type': 'hidden',
        }
    )
    customer_contact_name = StringField(
        _('customer contact name'),
        validators=[],
        description=_('customer contact name'),
        render_kw={
            'placeholder': _('customer contact name'),
            'rel': 'tooltip',
            'title': _('customer contact name'),
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
    type_tax = BooleanField(
        _('type tax'),
        default=True,
        validators=[],
        render_kw={
            'rel': 'tooltip',
            'title': _('type tax'),
            'checked': 'checked',
        }
    )
    note = StringField(
        _('sales order note'),
        validators=[],
        description=_('sales order note'),
        render_kw={
            'placeholder': _('sales order note'),
            'rel': 'tooltip',
            'title': _('sales order note'),
        }
    )
    status_order = SelectField(
        _('sales order status'),
        validators=[
            InputRequired(),
        ],
        coerce=int,
        description=_('sales order status'),
        render_kw={
            'rel': 'tooltip',
            'title': _('sales order status'),
        }
    )
    amount_order = DecimalField(
        _('amount order'),
        validators=[
            AmountSalesOrderValidate()
        ],
        description=_('amount order'),
        render_kw={
            'placeholder': _('amount order'),
            'rel': 'tooltip',
            'title': _('amount order'),
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
    sales_order_items = FieldList(
        FormField(SalesOrderItemEditForm),
        label='报价明细',
        min_entries=1,
        max_entries=12,
    )
