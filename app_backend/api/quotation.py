#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: quotation.py
@time: 2018-03-16 09:59
"""

from copy import copy
from datetime import datetime
from sqlalchemy.sql import func
from app_backend.databases.bearing import db_bearing
from app_backend.api.customer import get_customer_rows_by_ids
from app_backend.api.user import get_user_rows_by_ids
from app_common.libs.mysql_orm_op import DbInstance
from app_backend.models.model_bearing import Quotation
from app_common.maps.default import DEFAULT_SEARCH_CHOICES_INT
from app_common.maps.status_delete import STATUS_DEL_NO
from app_common.tools.date_time import get_current_day_time_ends, get_hours, time_local_to_utc, \
    get_current_month_time_ends, get_days, get_current_year_time_ends, get_months
from app_common.maps.status_order import STATUS_ORDER_OK

db_instance = DbInstance(db_bearing)


def get_quotation_row_by_id(quotation_id):
    """
    通过 id 获取信息
    :param quotation_id:
    :return: None/object
    """
    return db_instance.get_row_by_id(Quotation, quotation_id)


def get_quotation_row(*args, **kwargs):
    """
    获取信息
    :param args:
    :param kwargs:
    :return: None/object
    """
    return db_instance.get_row(Quotation, *args, **kwargs)


def get_quotation_latest(*args, **kwargs):
    """
    获取信息
    :param args:
    :param kwargs:
    :return: None/object
    """
    return db_instance.get_latest(Quotation, *args, **kwargs)


def get_quotation_rows(*args, **kwargs):
    """
    获取列表
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_rows(Quotation, *args, **kwargs)


def add_quotation(quotation_data):
    """
    添加信息
    :param quotation_data:
    :return: None/Value of user.id
    :except:
    """
    return db_instance.add(Quotation, quotation_data)


def edit_quotation(quotation_id, quotation_data):
    """
    修改信息
    :param quotation_id:
    :param quotation_data:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.edit(Quotation, quotation_id, quotation_data)


def delete_quotation(quotation_id):
    """
    删除信息
    :param quotation_id:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.delete(Quotation, quotation_id)


def delete_quotation_table():
    """
    清空表
    :return:
    """
    return db_instance.delete_table(Quotation)


def count_quotation(*args, **kwargs):
    """
    计数
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.count(Quotation, *args, **kwargs)


def get_quotation_pagination(page=1, per_page=10, *args, **kwargs):
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
    rows = db_instance.get_pagination(Quotation, page, per_page, *args, **kwargs)
    return rows


def quotation_total_stats(time_based='hour'):
    """
    报价总量统计
    :return:
    """
    condition = []
    # 按小时统计
    if time_based == 'hour':
        start_time, end_time = get_current_day_time_ends()
        hours = get_hours(False)
        hours_zerofill = get_hours()
        result = dict(zip(hours, [0] * len(hours)))
        condition.extend(
            [
                Quotation.create_time >= time_local_to_utc(start_time),
                Quotation.create_time <= time_local_to_utc(end_time)
            ]
        )
        rows = db.session \
            .query(func.hour(Quotation.create_time).label('hour'), func.count(Quotation.id)) \
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
                Quotation.create_time >= time_local_to_utc(start_time),
                Quotation.create_time <= time_local_to_utc(end_time)
            ]
        )
        rows = db.session \
            .query(func.day(Quotation.create_time).label('date'), func.count(Quotation.id)) \
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
                Quotation.create_time >= time_local_to_utc(start_time),
                Quotation.create_time <= time_local_to_utc(end_time)
            ]
        )
        rows = db.session \
            .query(func.month(Quotation.create_time).label('month'), func.count(Quotation.id)) \
            .filter(*condition) \
            .group_by('month') \
            .limit(len(months)) \
            .all()
        result.update(dict(rows))
        return [(months_zerofill[i], result[month]) for i, month in enumerate(months)]


def quotation_order_stats(time_based='hour'):
    """
    报价成交统计
    :return:
    """
    condition = [Quotation.status_order == STATUS_ORDER_OK]
    # 按小时统计
    if time_based == 'hour':
        start_time, end_time = get_current_day_time_ends()
        hours = get_hours(False)
        hours_zerofill = get_hours()
        result = dict(zip(hours, [0] * len(hours)))
        condition.extend(
            [
                Quotation.create_time >= time_local_to_utc(start_time),
                Quotation.create_time <= time_local_to_utc(end_time)
            ]
        )
        rows = db.session \
            .query(func.hour(Quotation.create_time).label('hour'), func.count(Quotation.id)) \
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
                Quotation.create_time >= time_local_to_utc(start_time),
                Quotation.create_time <= time_local_to_utc(end_time)
            ]
        )
        rows = db.session \
            .query(func.day(Quotation.create_time).label('date'), func.count(Quotation.id)) \
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
                Quotation.create_time >= time_local_to_utc(start_time),
                Quotation.create_time <= time_local_to_utc(end_time)
            ]
        )
        rows = db.session \
            .query(func.month(Quotation.create_time).label('month'), func.count(Quotation.id)) \
            .filter(*condition) \
            .group_by('month') \
            .limit(len(months)) \
            .all()
        result.update(dict(rows))
        return [(months_zerofill[i], result[month]) for i, month in enumerate(months)]


def get_distinct_quotation_uid(*args, **kwargs):
    """
    获取用户
    :param args:
    :param kwargs:
    :return: List
    """
    field = 'uid'
    return map(lambda x: getattr(x, field), db_instance.get_distinct_field(Quotation, field, *args, **kwargs))


def get_distinct_quotation_cid(*args, **kwargs):
    """
    获取客户
    :param args:
    :param kwargs:
    :return: List
    """
    field = 'cid'
    return map(lambda x: getattr(x, field), db_instance.get_distinct_field(Quotation, field, *args, **kwargs))


def get_quotation_user_list_choices():
    quotation_user_list = copy(DEFAULT_SEARCH_CHOICES_INT)
    uid_list = get_distinct_quotation_uid(status_delete=STATUS_DEL_NO)
    user_rows = get_user_rows_by_ids(uid_list)
    quotation_user_list.extend([(user.id, user.name) for user in user_rows])
    return quotation_user_list


def get_quotation_customer_list_choices(uid):
    # todo 移动到客户模块
    quotation_user_list = copy(DEFAULT_SEARCH_CHOICES_INT)
    cid_list = get_distinct_quotation_cid(status_delete=STATUS_DEL_NO, uid=uid)
    customer_rows = get_customer_rows_by_ids(cid_list)
    quotation_user_list.extend([(customer.id, customer.company_name) for customer in customer_rows])
    return quotation_user_list
