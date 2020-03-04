#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: bank_account.py
@time: 2018-04-06 12:20
"""

from copy import copy
from datetime import datetime
from sqlalchemy.sql import func
from app_backend.databases.bearing import db_bearing
from app_common.libs.mysql_orm_op import DbInstance
from app_backend.models.model_bearing import BankAccount
from app_common.maps.default import DEFAULT_SEARCH_CHOICES_INT, DEFAULT_SELECT_CHOICES_INT
from app_common.tools.date_time import get_current_day_time_ends, get_hours, time_local_to_utc, \
    get_current_month_time_ends, get_days, get_current_year_time_ends, get_months
from app_common.maps.status_order import STATUS_ORDER_OK
from app_common.maps.status_delete import STATUS_DEL_NO

db_instance = DbInstance(db_bearing)


def get_bank_account_row_by_id(bank_account_id):
    """
    通过 id 获取信息
    :param bank_account_id:
    :return: None/object
    """
    return db_instance.get_row_by_id(BankAccount, bank_account_id)


def get_bank_account_row(*args, **kwargs):
    """
    获取信息
    :param args:
    :param kwargs:
    :return: None/object
    """
    return db_instance.get_row(BankAccount, *args, **kwargs)


def get_bank_account_rows(*args, **kwargs):
    """
    获取列表
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_rows(BankAccount, *args, **kwargs)


def add_bank_account(bank_account_data):
    """
    添加信息
    :param bank_account_data:
    :return: None/Value of user.id
    :except:
    """
    return db_instance.add(BankAccount, bank_account_data)


def edit_bank_account(bank_account_id, bank_account_data):
    """
    修改信息
    :param bank_account_id:
    :param bank_account_data:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.edit(BankAccount, bank_account_id, bank_account_data)


def delete_bank_account(bank_account_id):
    """
    删除信息
    :param bank_account_id:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.delete(BankAccount, bank_account_id)


def get_bank_account_pagination(page=1, per_page=10, *args, **kwargs):
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
    rows = db_instance.get_pagination(BankAccount, page, per_page, *args, **kwargs)
    return rows


def get_bank_account_choices(option_type='search'):
    """
    获取选项
    :param option_type: 'search'/'create'/'update'
    :return:
    """
    bank_account_choices = copy(DEFAULT_SEARCH_CHOICES_INT) if option_type == 'search' else copy(
        DEFAULT_SELECT_CHOICES_INT)
    bank_account_list = map(lambda x: (getattr(x, 'id'), getattr(x, 'name')),
                         db_instance.get_rows(BankAccount, BankAccount.status_delete == STATUS_DEL_NO))
    bank_account_choices.extend(bank_account_list)
    return bank_account_choices
