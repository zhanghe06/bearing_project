#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: purchase.py
@time: 2019-02-18 22:57
"""


from blinker import Namespace


from app_backend import app

from app_backend.api.purchase_items import get_purchase_items_rows, edit_purchase_items, delete_purchase_items


_signal = Namespace()


# 状态跟踪
signal_purchase_status_auth = _signal.signal('signal_purchase_status_auth')  # 审核状态
signal_purchase_status_delete = _signal.signal('signal_purchase_status_delete')  # 删除状态


@signal_purchase_status_auth.connect_via(app)
def purchase_status_auth(sender, **extra):
    """
    状态跟踪 - 审核状态
    :param sender:
    :param extra:
    :return:
    """
    print(sender, extra)


@signal_purchase_status_delete.connect_via(app)
def purchase_status_delete(sender, **extra):
    """
    状态跟踪 - 删除状态
        1、明细删除状态同步更新
    :param sender:
    :param extra:
    :return:
    """
    # print(sender, extra)
    purchase_id = extra.get('purchase_id')
    status_delete = extra.get('status_delete')
    current_time = extra.get('current_time')
    if not purchase_id:
        return
    purchase_items = get_purchase_items_rows(purchase_id=purchase_id)
    result = True
    for purchase_item in purchase_items:
        purchase_item_id = purchase_item.id
        purchase_item_data = {
            'status_delete': status_delete,
            'delete_time': current_time,
            'update_time': current_time,
        }
        result = result and edit_purchase_items(purchase_item_id, purchase_item_data)
    return result
