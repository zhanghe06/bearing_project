#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: customer.py
@time: 2018-03-16 09:59
"""

from datetime import datetime
from sqlalchemy.sql import func
from app_backend import db
from app_common.libs.mysql_orm_op import DbInstance
from app_backend.models.bearing_project import Customer
from app_common.maps.status_delete import STATUS_DEL_NO
from app_common.tools.date_time import get_current_day_time_ends, get_hours, time_local_to_utc, \
    get_current_month_time_ends, get_days, get_current_year_time_ends, get_months
from app_common.maps.type_company import TYPE_COMPANY_MIDDLEMAN, TYPE_COMPANY_END_USER

db_instance = DbInstance(db)


def get_customer_row_by_id(customer_id):
    """
    通过 id 获取信息
    :param customer_id:
    :return: None/object
    """
    return db_instance.get_row_by_id(Customer, customer_id)


def get_customer_row(*args, **kwargs):
    """
    获取信息
    :param args:
    :param kwargs:
    :return: None/object
    """
    return db_instance.get_row(Customer, *args, **kwargs)


def get_customer_rows(*args, **kwargs):
    """
    获取列表
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_rows(Customer, *args, **kwargs)


def get_customer_rows_by_ids(pk_ids):
    """
    通过一组 ids 获取信息列表
    :param pk_ids:
    :return:
    """
    return db_instance.get_rows_by_ids(Customer, pk_ids)


def add_customer(customer_data):
    """
    添加信息
    :param customer_data:
    :return: None/Value of user.id
    :except:
    """
    return db_instance.add(Customer, customer_data)


def edit_customer(customer_id, customer_data):
    """
    修改信息
    :param customer_id:
    :param customer_data:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.edit(Customer, customer_id, customer_data)


def delete_customer(customer_id):
    """
    删除信息
    :param customer_id:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.delete(Customer, customer_id)


def get_customer_pagination(page=1, per_page=10, *args, **kwargs):
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
    rows = db_instance.get_pagination(Customer, page, per_page, *args, **kwargs)
    return rows


def customer_middleman_stats(time_based='hour'):
    """
    同行客户统计
    :return:
    """
    condition = [Customer.company_type == TYPE_COMPANY_MIDDLEMAN]
    # 按小时统计
    if time_based == 'hour':
        start_time, end_time = get_current_day_time_ends()
        hours = get_hours(False)
        hours_zerofill = get_hours()
        result = dict(zip(hours, [0] * len(hours)))
        condition.extend(
            [
                Customer.create_time >= time_local_to_utc(start_time),
                Customer.create_time <= time_local_to_utc(end_time)
            ]
        )
        rows = db.session \
            .query(func.hour(Customer.create_time).label('hour'), func.count(Customer.id)) \
            .filter(*condition) \
            .group_by('hour') \
            .limit(len(hours)) \
            .all()
        result.update(dict(rows))
        return [(hours_zerofill[i], result[hour]) for i, hour in enumerate(hours)]
    # 按日期统计
    if time_based == 'date':
        start_time, end_time = get_current_month_time_ends()
        today = datetime.today()
        days = get_days(year=today.year, month=today.month, zerofill=False)
        days_zerofill = get_days(year=today.year, month=today.month)
        result = dict(zip(days, [0] * len(days)))
        condition.extend(
            [
                Customer.create_time >= time_local_to_utc(start_time),
                Customer.create_time <= time_local_to_utc(end_time)
            ]
        )
        rows = db.session \
            .query(func.day(Customer.create_time).label('date'), func.count(Customer.id)) \
            .filter(*condition) \
            .group_by('date') \
            .limit(len(days)) \
            .all()
        result.update(dict(rows))
        return [(days_zerofill[i], result[day]) for i, day in enumerate(days)]
    # 按月份统计
    if time_based == 'month':
        start_time, end_time = get_current_year_time_ends()
        months = get_months(False)
        months_zerofill = get_months()
        result = dict(zip(months, [0] * len(months)))
        condition.extend(
            [
                Customer.create_time >= time_local_to_utc(start_time),
                Customer.create_time <= time_local_to_utc(end_time)
            ]
        )
        rows = db.session \
            .query(func.month(Customer.create_time).label('month'), func.count(Customer.id)) \
            .filter(*condition) \
            .group_by('month') \
            .limit(len(months)) \
            .all()
        result.update(dict(rows))
        return [(months_zerofill[i], result[month]) for i, month in enumerate(months)]


def customer_end_user_stats(time_based='hour'):
    """
    终端客户统计
    :return:
    """
    condition = [Customer.company_type == TYPE_COMPANY_END_USER]
    # 按小时统计
    if time_based == 'hour':
        start_time, end_time = get_current_day_time_ends()
        hours = get_hours(False)
        hours_zerofill = get_hours()
        result = dict(zip(hours, [0] * len(hours)))
        condition.extend(
            [
                Customer.create_time >= time_local_to_utc(start_time),
                Customer.create_time <= time_local_to_utc(end_time)
            ]
        )
        rows = db.session \
            .query(func.hour(Customer.create_time).label('hour'), func.count(Customer.id)) \
            .filter(*condition) \
            .group_by('hour') \
            .limit(len(hours)) \
            .all()
        result.update(dict(rows))
        return [(hours_zerofill[i], result[hour]) for i, hour in enumerate(hours)]
    # 按日期统计
    if time_based == 'date':
        start_time, end_time = get_current_month_time_ends()
        today = datetime.today()
        days = get_days(year=today.year, month=today.month, zerofill=False)
        days_zerofill = get_days(year=today.year, month=today.month)
        result = dict(zip(days, [0] * len(days)))
        condition.extend(
            [
                Customer.create_time >= time_local_to_utc(start_time),
                Customer.create_time <= time_local_to_utc(end_time)
            ]
        )
        rows = db.session \
            .query(func.day(Customer.create_time).label('date'), func.count(Customer.id)) \
            .filter(*condition) \
            .group_by('date') \
            .limit(len(days)) \
            .all()
        result.update(dict(rows))
        return [(days_zerofill[i], result[day]) for i, day in enumerate(days)]
    # 按月份统计
    if time_based == 'month':
        start_time, end_time = get_current_year_time_ends()
        months = get_months(False)
        months_zerofill = get_months()
        result = dict(zip(months, [0] * len(months)))
        condition.extend(
            [
                Customer.create_time >= time_local_to_utc(start_time),
                Customer.create_time <= time_local_to_utc(end_time)
            ]
        )
        rows = db.session \
            .query(func.month(Customer.create_time).label('month'), func.count(Customer.id)) \
            .filter(*condition) \
            .group_by('month') \
            .limit(len(months)) \
            .all()
        result.update(dict(rows))
        return [(months_zerofill[i], result[month]) for i, month in enumerate(months)]


def get_customer_choices():
    """
    获取客户选项
    :return:
    """
    customer_list = get_customer_rows(status_delete=STATUS_DEL_NO)
    customer_choices = [(customer.id, customer.company_name) for customer in customer_list]
    return customer_choices
