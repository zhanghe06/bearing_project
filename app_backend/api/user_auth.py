#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: user_auth.py
@time: 2018-03-16 10:02
"""

from app_backend import db
from app_common.libs.mysql_orm_op import DbInstance
from app_backend.models.bearing_project import UserAuth

db_instance = DbInstance(db)


def get_user_auth_row_by_id(user_auth_id):
    """
    通过 id 获取信息
    :param user_auth_id:
    :return: None/object
    """
    return db_instance.get_row_by_id(UserAuth, user_auth_id)


def get_user_auth_row(*args, **kwargs):
    """
    获取信息
    :param args:
    :param kwargs:
    :return: None/object
    """
    return db_instance.get_row(UserAuth, *args, **kwargs)


def get__auth_rows(*args, **kwargs):
    """
    获取列表
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_rows(UserAuth, *args, **kwargs)


def add_user_auth(user_auth_data):
    """
    添加信息
    :param user_auth_data:
    :return: None/Value of user.id
    :except:
    """
    return db_instance.add(UserAuth, user_auth_data)


def edit_user_auth(user_auth_id, user_auth_data):
    """
    修改信息
    :param user_auth_id:
    :param user_auth_data:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.edit(UserAuth, user_auth_id, user_auth_data)


def delete_user_auth(user_auth_id):
    """
    删除信息
    :param user_auth_id:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.delete(UserAuth, user_auth_id)


def get_user_auth_pagination(page=1, per_page=10, *args, **kwargs):
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
    rows = db_instance.get_pagination(UserAuth, page, per_page, *args, **kwargs)
    return rows
