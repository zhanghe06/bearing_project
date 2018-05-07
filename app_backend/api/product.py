#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: product.py
@time: 2018-03-16 09:59
"""


from app_backend import db
from app_common.libs.mysql_orm_op import DbInstance
from app_backend.models.bearing_project import Product

db_instance = DbInstance(db)


def get_product_row_by_id(product_id):
    """
    通过 id 获取信息
    :param product_id:
    :return: None/object
    """
    return db_instance.get_row_by_id(Product, product_id)


def get_product_row(*args, **kwargs):
    """
    获取信息
    :param args:
    :param kwargs:
    :return: None/object
    """
    return db_instance.get_row(Product, *args, **kwargs)


def get_product_rows(*args, **kwargs):
    """
    获取列表
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_rows(Product, *args, **kwargs)


def add_product(product_data):
    """
    添加信息
    :param product_data:
    :return: None/Value of user.id
    :except:
    """
    return db_instance.add(Product, product_data)


def edit_product(product_id, product_data):
    """
    修改信息
    :param product_id:
    :param product_data:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.edit(Product, product_id, product_data)


def delete_product(product_id):
    """
    删除信息
    :param product_id:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.delete(Product, product_id)


def get_product_pagination(page=1, per_page=10, *args, **kwargs):
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
    rows = db_instance.get_pagination(Product, page, per_page, *args, **kwargs)
    return rows


def get_distinct_brand(*args, **kwargs):
    """
    获取品牌
    :param args:
    :param kwargs:
    :return: List
    """
    field = 'product_brand'
    return map(lambda x: getattr(x, field), db_instance.get_distinct_field(Product, field, *args, **kwargs))
