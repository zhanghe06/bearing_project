#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: login_user.py
@time: 2018-03-23 14:52
"""

from app_backend.databases.bearing import db_bearing
from app_backend.login import LoginUser
from app_common.libs.mysql_orm_op import DbInstance

db_instance = DbInstance(db_bearing)


def get_login_user_row_by_id(user_id):
    """
    通过 id 获取信息
    :param user_id:
    :return: None/object
    """
    return db_instance.get_row_by_id(LoginUser, user_id)


def get_login_user_row(*args, **kwargs):
    """
    获取信息
    :param args:
    :param kwargs:
    :return: None/object
    """
    return db_instance.get_row(LoginUser, *args, **kwargs)


def get_login_user_rows(*args, **kwargs):
    """
    获取列表
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_rows(LoginUser, *args, **kwargs)


def add_login_user(user_data):
    """
    添加信息
    :param user_data:
    :return: None/Value of user.id
    :except:
    """
    return db_instance.add(LoginUser, user_data)


def edit_login_user(user_id, user_data):
    """
    修改信息
    :param user_id:
    :param user_data:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.edit(LoginUser, user_id, user_data)


def delete_login_user(user_id):
    """
    删除信息
    :param user_id:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.delete(LoginUser, user_id)


def get_login_user_pagination(page=1, per_page=10, *args, **kwargs):
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
    rows = db_instance.get_pagination(LoginUser, page, per_page, *args, **kwargs)
    return rows
