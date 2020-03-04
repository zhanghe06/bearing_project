#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: delivery_items.py
@time: 2019-02-11 17:41
"""


from app_common.libs.mysql_orm_op import DbInstance
from app_backend.models.model_bearing import DeliveryItems
from app_backend.databases.bearing import db_bearing

db_instance = DbInstance(db_bearing)


def get_delivery_items_rows(*args, **kwargs):
    """
    获取列表
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_rows(DeliveryItems, *args, **kwargs)


def add_delivery_items(delivery_items_data):
    """
    添加信息
    :param delivery_items_data:
    :return: None/Value of user.id
    :except:
    """
    return db_instance.add(DeliveryItems, delivery_items_data)


def edit_delivery_items(delivery_items_id, delivery_items_data):
    """
    修改信息
    :param delivery_items_id:
    :param delivery_items_data:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.edit(DeliveryItems, delivery_items_id, delivery_items_data)


def delete_delivery_items(delivery_items_id):
    """
    删除信息
    :param delivery_items_id:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.delete(DeliveryItems, delivery_items_id)


def delete_delivery_items_table():
    """
    清空表
    :return:
    """
    return db_instance.delete_table(DeliveryItems)


def count_delivery_items(*args, **kwargs):
    """
    计数
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.count(DeliveryItems, *args, **kwargs)


def get_delivery_items_pagination(page=1, per_page=10, *args, **kwargs):
    """
    获取列表（分页）
    Usage:
        items: 信息列表
        has_next: 如果本页之后还有超过一个分页，则返回True
        has_prev: 如果本页之前还有超过一个分页，则返回True
        next_num: 返回下一页的页码
        prev_num: 返回上一页的页码
        iter_pages(): 页码列表
        iter_pages(left_edge=2, left_current=2, right_current=5, right_edge=2) 页码列表默认参数
    :param page:
    :param per_page:
    :param args:
    :param kwargs:
    :return:
    """
    rows = db_instance.get_pagination(DeliveryItems, page, per_page, *args, **kwargs)
    return rows
