#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: production_sensitive.py
@time: 2018-08-14 14:49
"""


from app_backend import db
from app_common.libs.mysql_orm_op import DbInstance
from app_backend.models.bearing_project import ProductionSensitive
from app_common.maps.default import default_choices_int
from app_common.maps.status_delete import STATUS_DEL_NO

db_instance = DbInstance(db)


def get_production_sensitive_row_by_id(production_sensitive_id):
    """
    通过 id 获取信息
    :param production_sensitive_id:
    :return: None/object
    """
    return db_instance.get_row_by_id(ProductionSensitive, production_sensitive_id)


def get_production_sensitive_row(*args, **kwargs):
    """
    获取信息
    :param args:
    :param kwargs:
    :return: None/object
    """
    return db_instance.get_row(ProductionSensitive, *args, **kwargs)


def get_production_sensitive_rows(*args, **kwargs):
    """
    获取列表
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_rows(ProductionSensitive, *args, **kwargs)


def get_production_sensitive_limit_rows_by_last_id(last_pk_id, limit_num, *args, **kwargs):
    """
    通过最后一个主键 id 获取最新信息列表
    :param last_pk_id:
    :param limit_num:
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_limit_rows_by_last_id(ProductionSensitive, last_pk_id, limit_num, *args, **kwargs)


def add_production_sensitive(production_sensitive_data):
    """
    添加信息
    :param production_sensitive_data:
    :return: None/Value of user.id
    :except:
    """
    return db_instance.add(ProductionSensitive, production_sensitive_data)


def edit_production_sensitive(production_sensitive_id, production_sensitive_data):
    """
    修改信息
    :param production_sensitive_id:
    :param production_sensitive_data:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.edit(ProductionSensitive, production_sensitive_id, production_sensitive_data)


def delete_production_sensitive(production_sensitive_id):
    """
    删除信息
    :param production_sensitive_id:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.delete(ProductionSensitive, production_sensitive_id)


def get_production_sensitive_pagination(page=1, per_page=10, *args, **kwargs):
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
    rows = db_instance.get_pagination(ProductionSensitive, page, per_page, *args, **kwargs)
    return rows


def delete_production_sensitive_table():
    """
    清空表
    :return:
    """
    return db_instance.delete_table(ProductionSensitive)


def count_production_sensitive(*args, **kwargs):
    """
    计数
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.count(ProductionSensitive, *args, **kwargs)


def get_distinct_production_sensitive_brand(*args, **kwargs):
    """
    获取品牌
    :param args:
    :param kwargs:
    :return: List
    """
    field = 'production_brand'
    return map(lambda x: getattr(x, field), db_instance.get_distinct_field(ProductionSensitive, field, *args, **kwargs))
