#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: sales_orders.py
@time: 2019-02-19 10:43
"""


from blinker import Namespace


from app_backend import app

from app_backend.api.sales_order_items import get_sales_order_items_rows, edit_sales_order_items, delete_sales_order_items


_signal = Namespace()


# 状态跟踪
signal_sales_orders_status_auth = _signal.signal('signal_sales_orders_status_auth')  # 审核状态
signal_sales_orders_status_delete = _signal.signal('signal_sales_orders_status_delete')  # 删除状态


@signal_sales_orders_status_auth.connect_via(app)
def sales_orders_status_auth(sender, **extra):
    """
    状态跟踪 - 审核状态
    :param sender:
    :param extra:
    :return:
    """
    print(sender, extra)


@signal_sales_orders_status_delete.connect_via(app)
def sales_orders_status_delete(sender, **extra):
    """
    状态跟踪 - 删除状态
        1、明细删除状态同步更新
    :param sender:
    :param extra:
    :return:
    """
    # print(sender, extra)
    sales_order_id = extra.get('sales_order_id')
    status_delete = extra.get('status_delete')
    current_time = extra.get('current_time')
    if not sales_order_id:
        return
    sales_order_items = get_sales_order_items_rows(sales_order_id=sales_order_id)
    result = True
    for sales_order_item in sales_order_items:
        sales_order_item_id = sales_order_item.id
        sales_order_item_data = {
            'status_delete': status_delete,
            'delete_time': current_time,
            'update_time': current_time,
        }
        result = result and edit_sales_order_items(sales_order_item_id, sales_order_item_data)
    return result
