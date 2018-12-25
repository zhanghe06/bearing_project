#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: customer.py
@time: 2018-08-15 18:10
"""


from blinker import Namespace


from app_backend import app

from app_backend.api.customer_invoice import get_customer_invoice_row_by_id, edit_customer_invoice
from app_backend.api.customer_contact import get_customer_contact_rows, edit_customer_contact
from app_backend.api.quotation import get_quotation_rows, edit_quotation
from app_backend.api.quotation_items import get_quotation_items_rows, edit_quotation_items

_signal = Namespace()


# 状态跟踪
signal_customer_status_delete = _signal.signal('signal_customer_status_delete')  # 删除状态


@signal_customer_status_delete.connect_via(app)
def customer_status_delete(sender, **extra):
    """
    状态跟踪 - 删除状态
        1、开票资料删除状态同步更新
        2、联系方式删除状态同步更新
        3、客户报价删除状态同步更新
    :param sender:
    :param extra:
    :return:
    """
    # print(sender, extra)
    customer_id = extra.get('customer_id')
    status_delete = extra.get('status_delete')
    current_time = extra.get('current_time')
    if not customer_id:
        return

    result = True
    # 1、开票资料删除状态同步更新
    customer_invoice_info = get_customer_invoice_row_by_id(customer_id)
    if customer_invoice_info:
        customer_invoice_data = {
            'status_delete': status_delete,
            'delete_time': current_time,
            'update_time': current_time,
        }
        result = result and edit_customer_invoice(customer_id, customer_invoice_data)

    # 2、联系方式删除状态同步更新
    customer_contact_items = get_customer_contact_rows(cid=customer_id)
    for customer_contact_item in customer_contact_items:
        customer_contact_item_id = customer_contact_item.id
        customer_contact_item_data = {
            'status_delete': status_delete,
            'delete_time': current_time,
            'update_time': current_time,
        }
        result = result and edit_customer_contact(customer_contact_item_id, customer_contact_item_data)

    # 3、客户报价删除状态同步更新
    # 报价总表
    quotation_items = get_quotation_rows(cid=customer_id)
    for quotation_item in quotation_items:
        quotation_item_id = quotation_item.id
        quotation_item_data = {
            'status_delete': status_delete,
            'delete_time': current_time,
            'update_time': current_time,
        }
        result = result and edit_quotation(quotation_item_id, quotation_item_data)
        # 报价明细
        quotation_items_items = get_quotation_items_rows(quotation_id=quotation_item_id)
        for quotation_item_item in quotation_items_items:
            quotation_item_item_id = quotation_item_item.id
            quotation_item_item_data = {
                'status_delete': status_delete,
                'delete_time': current_time,
                'update_time': current_time,
            }
            result = result and edit_quotation_items(quotation_item_item_id, quotation_item_item_data)

    return result
