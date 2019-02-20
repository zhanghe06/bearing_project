#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: sales_order_items.py
@time: 2018-09-13 14:13
"""


from app_common.libs.mysql_orm_op import DbInstance
from app_backend.models.bearing_project import SalesOrderItems
from app_backend import db

db_instance = DbInstance(db)


def get_sales_order_items_rows(*args, **kwargs):
    """
    获取列表
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_rows(SalesOrderItems, *args, **kwargs)


def add_sales_order_items(sales_orders_item_data):
    """
    添加信息
    :param sales_orders_item_data:
    :return: None/Value of user.id
    :except:
    """
    return db_instance.add(SalesOrderItems, sales_orders_item_data)


def edit_sales_order_items(sales_orders_item_id, sales_orders_item_data):
    """
    修改信息
    :param sales_orders_item_id:
    :param sales_orders_item_data:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.edit(SalesOrderItems, sales_orders_item_id, sales_orders_item_data)


def delete_sales_order_items(sales_orders_item_id):
    """
    删除信息
    :param sales_orders_item_id:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.delete(SalesOrderItems, sales_orders_item_id)


def delete_sales_order_items_table():
    """
    清空表
    :return:
    """
    return db_instance.delete_table(SalesOrderItems)


def count_sales_order_items(*args, **kwargs):
    """
    计数
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.count(SalesOrderItems, *args, **kwargs)


def get_sales_order_items_pagination(page=1, per_page=10, *args, **kwargs):
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
    rows = db_instance.get_pagination(SalesOrderItems, page, per_page, *args, **kwargs)
    return rows
