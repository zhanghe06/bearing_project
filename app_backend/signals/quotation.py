#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: quotation.py
@time: 2018-08-15 16:16
"""


from blinker import Namespace


from app_backend import app

from app_backend.api.quotation_item import get_quotation_item_rows, edit_quotation_item, delete_quotation_item


_signal = Namespace()


# 状态跟踪
signal_quotation_status_auth = _signal.signal('signal_quotation_status_auth')  # 审核状态
signal_quotation_status_delete = _signal.signal('signal_quotation_status_delete')  # 删除状态


@signal_quotation_status_auth.connect_via(app)
def quotation_status_auth(sender, **extra):
    """
    状态跟踪 - 审核状态
    :param sender:
    :param extra:
    :return:
    """
    print(sender, extra)


@signal_quotation_status_delete.connect_via(app)
def quotation_status_delete(sender, **extra):
    """
    状态跟踪 - 删除状态
        1、明细删除状态同步更新
    :param sender:
    :param extra:
    :return:
    """
    # print(sender, extra)
    quotation_id = extra.get('quotation_id')
    status_delete = extra.get('status_delete')
    current_time = extra.get('current_time')
    if not quotation_id:
        return
    quotation_items = get_quotation_item_rows(quotation_id=quotation_id)
    result = True
    for quotation_item in quotation_items:
        quotation_item_id = quotation_item.id
        quotation_item_data = {
            'status_delete': status_delete,
            'delete_time': current_time,
            'update_time': current_time,
        }
        result = result and edit_quotation_item(quotation_item_id, quotation_item_data)
    return result
