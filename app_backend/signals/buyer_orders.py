#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: buyer_orders.py
@time: 2018-09-13 14:12
"""


from blinker import Namespace


from app_backend import app

from app_backend.api.buyer_order_items import get_buyer_order_items_rows, edit_buyer_order_items, delete_buyer_order_items


_signal = Namespace()


# 状态跟踪
signal_buyer_orders_status_auth = _signal.signal('signal_buyer_orders_status_auth')  # 审核状态
signal_buyer_orders_status_delete = _signal.signal('signal_buyer_orders_status_delete')  # 删除状态


@signal_buyer_orders_status_auth.connect_via(app)
def buyer_orders_status_auth(sender, **extra):
    """
    状态跟踪 - 审核状态
    :param sender:
    :param extra:
    :return:
    """
    print(sender, extra)


@signal_buyer_orders_status_delete.connect_via(app)
def buyer_orders_status_delete(sender, **extra):
    """
    状态跟踪 - 删除状态
        1、明细删除状态同步更新
    :param sender:
    :param extra:
    :return:
    """
    # print(sender, extra)
    buyer_orders_id = extra.get('buyer_orders_id')
    status_delete = extra.get('status_delete')
    current_time = extra.get('current_time')
    if not buyer_orders_id:
        return
    buyer_orders_items = get_buyer_order_items_rows(buyer_orders_id=buyer_orders_id)
    result = True
    for buyer_orders_item in buyer_orders_items:
        buyer_orders_item_id = buyer_orders_item.id
        buyer_orders_item_data = {
            'status_delete': status_delete,
            'delete_time': current_time,
            'update_time': current_time,
        }
        result = result and edit_buyer_order_items(buyer_orders_item_id, buyer_orders_item_data)
    return result
