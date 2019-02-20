#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: delivery.py
@time: 2019-02-21 01:00
"""


from blinker import Namespace


from app_backend import app

from app_backend.api.delivery_items import get_delivery_items_rows, edit_delivery_items, delete_delivery_items


_signal = Namespace()


# 状态跟踪
signal_delivery_status_auth = _signal.signal('signal_delivery_status_auth')  # 审核状态
signal_delivery_status_delete = _signal.signal('signal_delivery_status_delete')  # 删除状态


@signal_delivery_status_auth.connect_via(app)
def delivery_status_auth(sender, **extra):
    """
    状态跟踪 - 审核状态
    :param sender:
    :param extra:
    :return:
    """
    print(sender, extra)


@signal_delivery_status_delete.connect_via(app)
def delivery_status_delete(sender, **extra):
    """
    状态跟踪 - 删除状态
        1、明细删除状态同步更新
    :param sender:
    :param extra:
    :return:
    """
    # print(sender, extra)
    delivery_id = extra.get('delivery_id')
    status_delete = extra.get('status_delete')
    current_time = extra.get('current_time')
    if not delivery_id:
        return
    delivery_items = get_delivery_items_rows(delivery_id=delivery_id)
    result = True
    for delivery_item in delivery_items:
        delivery_item_id = delivery_item.id
        delivery_item_data = {
            'status_delete': status_delete,
            'delete_time': current_time,
            'update_time': current_time,
        }
        result = result and edit_delivery_items(delivery_item_id, delivery_item_data)
    return result
