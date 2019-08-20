#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: supplier.py
@time: 2018-09-12 16:39
"""


from blinker import Namespace


from app_backend import app

from app_backend.api.supplier_invoice import get_supplier_invoice_row_by_id, edit_supplier_invoice
from app_backend.api.supplier_contact import get_supplier_contact_rows, edit_supplier_contact
from app_backend.api.enquiry import get_enquiry_rows, edit_enquiry
from app_backend.api.enquiry_items import get_enquiry_items_rows, edit_enquiry_items

_signal = Namespace()


# 状态跟踪
signal_supplier_status_delete = _signal.signal('signal_supplier_status_delete')  # 删除状态


@signal_supplier_status_delete.connect_via(app)
def supplier_status_delete(sender, **extra):
    """
    状态跟踪 - 删除状态
        1、开票资料删除状态同步更新
        2、联系方式删除状态同步更新
        3、渠道询价删除状态同步更新
        4、渠道进货删除状态同步更新
    :param sender:
    :param extra:
    :return:
    """
    # print(sender, extra)
    supplier_id = extra.get('supplier_id')
    status_delete = extra.get('status_delete')
    current_time = extra.get('current_time')
    if not supplier_id:
        return

    result = True
    # 1、开票资料删除状态同步更新
    supplier_invoice_info = get_supplier_invoice_row_by_id(supplier_id)
    if supplier_invoice_info:
        supplier_invoice_data = {
            'status_delete': status_delete,
            'delete_time': current_time,
            'update_time': current_time,
        }
        result = result and edit_supplier_invoice(supplier_id, supplier_invoice_data)

    # 2、联系方式删除状态同步更新
    supplier_contact_items = get_supplier_contact_rows(cid=supplier_id)
    for supplier_contact_item in supplier_contact_items:
        supplier_contact_item_id = supplier_contact_item.id
        supplier_contact_item_data = {
            'status_delete': status_delete,
            'delete_time': current_time,
            'update_time': current_time,
        }
        result = result and edit_supplier_contact(supplier_contact_item_id, supplier_contact_item_data)

    # 3、渠道询价删除状态同步更新
    # 询价总表
    enquiry_items = get_enquiry_rows(supplier_cid=supplier_id)
    for enquiry_item in enquiry_items:
        enquiry_item_id = enquiry_item.id
        enquiry_item_data = {
            'status_delete': status_delete,
            'delete_time': current_time,
            'update_time': current_time,
        }
        result = result and edit_enquiry(enquiry_item_id, enquiry_item_data)
        # 询价明细
        enquiry_items_items = get_enquiry_items_rows(enquiry_id=enquiry_item_id)
        for enquiry_item_item in enquiry_items_items:
            enquiry_item_item_id = enquiry_item_item.id
            enquiry_item_item_data = {
                'status_delete': status_delete,
                'delete_time': current_time,
                'update_time': current_time,
            }
            result = result and edit_enquiry_items(enquiry_item_item_id, enquiry_item_item_data)

    return result
