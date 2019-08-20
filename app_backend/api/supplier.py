#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: supplier.py
@time: 2018-09-12 11:33
"""


from datetime import datetime
from sqlalchemy.sql import func
from app_backend import db
from app_common.libs.mysql_orm_op import DbInstance
from app_backend.models.bearing_project import Supplier
from app_common.maps.status_delete import STATUS_DEL_NO
from app_common.tools.date_time import get_current_day_time_ends, get_hours, time_local_to_utc, \
    get_current_month_time_ends, get_days, get_current_year_time_ends, get_months
from app_common.maps.type_company import TYPE_COMPANY_MIDDLEMAN, TYPE_COMPANY_FINAL_USER

db_instance = DbInstance(db)


def get_supplier_row_by_id(supplier_id):
    """
    通过 id 获取信息
    :param supplier_id:
    :return: None/object
    """
    return db_instance.get_row_by_id(Supplier, supplier_id)


def get_supplier_row(*args, **kwargs):
    """
    获取信息
    :param args:
    :param kwargs:
    :return: None/object
    """
    return db_instance.get_row(Supplier, *args, **kwargs)


def get_supplier_rows(*args, **kwargs):
    """
    获取列表
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_rows(Supplier, *args, **kwargs)


def get_supplier_rows_by_ids(pk_ids):
    """
    通过一组 ids 获取信息列表
    :param pk_ids:
    :return:
    """
    return db_instance.get_rows_by_ids(Supplier, pk_ids)


def add_supplier(supplier_data):
    """
    添加信息
    :param supplier_data:
    :return: None/Value of user.id
    :except:
    """
    return db_instance.add(Supplier, supplier_data)


def edit_supplier(supplier_id, supplier_data):
    """
    修改信息
    :param supplier_id:
    :param supplier_data:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.edit(Supplier, supplier_id, supplier_data)


def delete_supplier(supplier_id):
    """
    删除信息
    :param supplier_id:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.delete(Supplier, supplier_id)


def get_supplier_pagination(page=1, per_page=10, *args, **kwargs):
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
    rows = db_instance.get_pagination(Supplier, page, per_page, *args, **kwargs)
    return rows


def supplier_middleman_stats(time_based='hour'):
    """
    同行客户统计
    :return:
    """
    condition = [Supplier.company_type == TYPE_COMPANY_MIDDLEMAN]
    # 按小时统计
    if time_based == 'hour':
        start_time, end_time = get_current_day_time_ends()
        hours = get_hours(False)
        hours_zerofill = get_hours()
        result = dict(zip(hours, [0] * len(hours)))
        condition.extend(
            [
                Supplier.create_time >= time_local_to_utc(start_time),
                Supplier.create_time <= time_local_to_utc(end_time)
            ]
        )
        rows = db.session \
            .query(func.hour(Supplier.create_time).label('hour'), func.count(Supplier.id)) \
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
                Supplier.create_time >= time_local_to_utc(start_time),
                Supplier.create_time <= time_local_to_utc(end_time)
            ]
        )
        rows = db.session \
            .query(func.day(Supplier.create_time).label('date'), func.count(Supplier.id)) \
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
                Supplier.create_time >= time_local_to_utc(start_time),
                Supplier.create_time <= time_local_to_utc(end_time)
            ]
        )
        rows = db.session \
            .query(func.month(Supplier.create_time).label('month'), func.count(Supplier.id)) \
            .filter(*condition) \
            .group_by('month') \
            .limit(len(months)) \
            .all()
        result.update(dict(rows))
        return [(months_zerofill[i], result[month]) for i, month in enumerate(months)]


def supplier_end_user_stats(time_based='hour'):
    """
    终端客户统计
    :return:
    """
    condition = [Supplier.company_type == TYPE_COMPANY_FINAL_USER]
    # 按小时统计
    if time_based == 'hour':
        start_time, end_time = get_current_day_time_ends()
        hours = get_hours(False)
        hours_zerofill = get_hours()
        result = dict(zip(hours, [0] * len(hours)))
        condition.extend(
            [
                Supplier.create_time >= time_local_to_utc(start_time),
                Supplier.create_time <= time_local_to_utc(end_time)
            ]
        )
        rows = db.session \
            .query(func.hour(Supplier.create_time).label('hour'), func.count(Supplier.id)) \
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
                Supplier.create_time >= time_local_to_utc(start_time),
                Supplier.create_time <= time_local_to_utc(end_time)
            ]
        )
        rows = db.session \
            .query(func.day(Supplier.create_time).label('date'), func.count(Supplier.id)) \
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
                Supplier.create_time >= time_local_to_utc(start_time),
                Supplier.create_time <= time_local_to_utc(end_time)
            ]
        )
        rows = db.session \
            .query(func.month(Supplier.create_time).label('month'), func.count(Supplier.id)) \
            .filter(*condition) \
            .group_by('month') \
            .limit(len(months)) \
            .all()
        result.update(dict(rows))
        return [(months_zerofill[i], result[month]) for i, month in enumerate(months)]


def get_supplier_choices():
    """
    获取客户选项
    :return:
    """
    supplier_list = get_supplier_rows(status_delete=STATUS_DEL_NO)
    supplier_choices = [(supplier.id, supplier.company_name) for supplier in supplier_list]
    return supplier_choices