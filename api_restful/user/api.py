#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: api.py
@time: 2020-02-28 21:26
"""


import datetime

from api_restful.databases.bearing import db_bearing
from app_common.maps.status_delete import STATUS_DEL_OK
from api_restful.models.model_bearing import User

from app_common.libs.mysql_orm_op import DbInstance


db_instance = DbInstance(db_bearing)


def get_user_row_by_id(user_id):
    """
    通过 id 获取信息
    :param user_id:
    :return: None/object
    """
    return db_instance.get_row_by_id(User, user_id)


def get_user_row(*args, **kwargs):
    """
    获取信息
    :param args:
    :param kwargs:
    :return: None/object
    """
    return db_instance.get_row(User, *args, **kwargs)


def get_user_rows(*args, **kwargs):
    """
    获取列表
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_rows(User, *args, **kwargs)


def get_user_limit_rows_by_last_id(last_pk, limit_num, *args, **kwargs):
    """
    通过最后一个主键 id 获取最新信息列表
    :param last_pk:
    :param limit_num:
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_limit_rows_by_last_id(User, last_pk, limit_num, *args, **kwargs)


def add_user(user_data):
    """
    添加信息
    :param user_data:
    :return: None/Value of user.id
    :except:
    """
    return db_instance.add(User, user_data)


def edit_user(user_id, user_data):
    """
    修改信息
    :param user_id:
    :param user_data:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.edit(User, user_id, user_data)


def delete_user(user_id, force=False):
    """
    删除信息
    :param user_id:
    :param force:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    if force:
        return db_instance.delete(User, user_id)
    else:
        data = {
            'status_delete': STATUS_DEL_OK,
            'delete_time': datetime.datetime.now()
        }
        if isinstance(user_id, list):
            return db_instance.update_rows(User, data, User.id.in_(user_id))
        else:
            return db_instance.edit(User, user_id, data)


def get_user_pagination(page=1, size=10, *args, **kwargs):
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
    :param size:
    :param args:
    :param kwargs:
    :return:
    """
    rows = db_instance.get_pagination(User, page, size, *args, **kwargs)
    return rows


def delete_user_table():
    """
    清空表
    :return:
    """
    return db_instance.delete_table(User)


def count_user(*args, **kwargs):
    """
    计数
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.count(User, *args, **kwargs)
