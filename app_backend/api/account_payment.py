#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: account_payment.py
@time: 2019-08-20 17:03
"""

from app_backend.databases.bearing import db_bearing
from app_backend.models.model_bearing import AccountPayment
from app_common.libs.mysql_orm_op import DbInstance

db_instance = DbInstance(db_bearing)


def get_account_payment_row_by_id(account_payment_id):
    """
    通过 id 获取信息
    :param account_payment_id:
    :return: None/object
    """
    return db_instance.get_row_by_id(AccountPayment, account_payment_id)


def get_account_payment_row(*args, **kwargs):
    """
    获取信息
    :param args:
    :param kwargs:
    :return: None/object
    """
    return db_instance.get_row(AccountPayment, *args, **kwargs)


def get_account_payment_rows(*args, **kwargs):
    """
    获取列表
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_rows(AccountPayment, *args, **kwargs)


def get_account_payment_limit_rows_by_last_id(last_pk_id, limit_num, *args, **kwargs):
    """
    通过最后一个主键 id 获取最新信息列表
    :param last_pk_id:
    :param limit_num:
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_limit_rows_by_last_id(AccountPayment, last_pk_id, limit_num, *args, **kwargs)


def add_account_payment(account_payment_data):
    """
    添加信息
    :param account_payment_data:
    :return: None/Value of user.id
    :except:
    """
    return db_instance.add(AccountPayment, account_payment_data)


def edit_account_payment(account_payment_id, account_payment_data):
    """
    修改信息
    :param account_payment_id:
    :param account_payment_data:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.edit(AccountPayment, account_payment_id, account_payment_data)


def delete_account_payment(account_payment_id):
    """
    删除信息
    :param account_payment_id:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.delete(AccountPayment, account_payment_id)


def get_account_payment_pagination(page=1, per_page=10, *args, **kwargs):
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
    rows = db_instance.get_pagination(AccountPayment, page, per_page, *args, **kwargs)
    return rows


def delete_account_payment_table():
    """
    清空表
    :return:
    """
    return db_instance.delete_table(AccountPayment)


def count_account_payment(*args, **kwargs):
    """
    计数
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.count(AccountPayment, *args, **kwargs)
