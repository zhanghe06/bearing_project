#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: enquiry.py
@time: 2018-09-12 22:21
"""


from blinker import Namespace


from app_backend import app

from app_backend.api.enquiry_items import get_enquiry_items_rows, edit_enquiry_items, delete_enquiry_items


_signal = Namespace()


# 状态跟踪
signal_enquiry_status_auth = _signal.signal('signal_enquiry_status_auth')  # 审核状态
signal_enquiry_status_delete = _signal.signal('signal_enquiry_status_delete')  # 删除状态


@signal_enquiry_status_auth.connect_via(app)
def enquiry_status_auth(sender, **extra):
    """
    状态跟踪 - 审核状态
    :param sender:
    :param extra:
    :return:
    """
    print(sender, extra)


@signal_enquiry_status_delete.connect_via(app)
def enquiry_status_delete(sender, **extra):
    """
    状态跟踪 - 删除状态
        1、明细删除状态同步更新
    :param sender:
    :param extra:
    :return:
    """
    # print(sender, extra)
    enquiry_id = extra.get('enquiry_id')
    status_delete = extra.get('status_delete')
    current_time = extra.get('current_time')
    if not enquiry_id:
        return
    enquiry_items = get_enquiry_items_rows(enquiry_id=enquiry_id)
    result = True
    for enquiry_item in enquiry_items:
        enquiry_item_id = enquiry_item.id
        enquiry_item_data = {
            'status_delete': status_delete,
            'delete_time': current_time,
            'update_time': current_time,
        }
        result = result and edit_enquiry_items(enquiry_item_id, enquiry_item_data)
    return result
