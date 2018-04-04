#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: user.py
@time: 2018-03-16 09:58
"""

from datetime import datetime
from sqlalchemy.sql import func
from app_backend import db
from app_backend.login import User
from app_common.libs.mysql_orm_op import DbInstance
from app_common.tools.date_time import get_current_day_time_ends, get_hours, time_local_to_utc, \
    get_current_month_time_ends, get_days, get_current_year_time_ends, get_months
from app_common.maps.status_delete import STATUS_DEL_NO, STATUS_DEL_OK

db_instance = DbInstance(db)


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


def delete_user(user_id):
    """
    删除信息
    :param user_id:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.delete(User, user_id)


def get_user_pagination(page=1, per_page=10, *args, **kwargs):
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
    rows = db_instance.get_pagination(User, page, per_page, *args, **kwargs)
    return rows


def user_current_stats(time_based='hour'):
    """
    在职用户统计
    :return:
    """
    condition = [User.status_delete == STATUS_DEL_NO]
    # 按小时统计
    if time_based == 'hour':
        start_time, end_time = get_current_day_time_ends()
        hours = get_hours(False)
        hours_zerofill = get_hours()
        result = dict(zip(hours, [0] * len(hours)))
        condition.extend(
            [
                User.create_time >= time_local_to_utc(start_time),
                User.create_time <= time_local_to_utc(end_time)
            ]
        )
        rows = db.session \
            .query(func.hour(User.create_time).label('hour'), func.count(User.id)) \
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
                User.create_time >= time_local_to_utc(start_time),
                User.create_time <= time_local_to_utc(end_time)
            ]
        )
        rows = db.session \
            .query(func.day(User.create_time).label('date'), func.count(User.id)) \
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
                User.create_time >= time_local_to_utc(start_time),
                User.create_time <= time_local_to_utc(end_time)
            ]
        )
        rows = db.session \
            .query(func.month(User.create_time).label('month'), func.count(User.id)) \
            .filter(*condition) \
            .group_by('month') \
            .limit(len(months)) \
            .all()
        result.update(dict(rows))
        return [(months_zerofill[i], result[month]) for i, month in enumerate(months)]


def user_former_stats(time_based='hour'):
    """
    离职用户统计
    :return:
    """
    condition = [User.status_delete == STATUS_DEL_OK]
    # 按小时统计
    if time_based == 'hour':
        start_time, end_time = get_current_day_time_ends()
        hours = get_hours(False)
        hours_zerofill = get_hours()
        result = dict(zip(hours, [0] * len(hours)))
        condition.extend(
            [
                User.create_time >= time_local_to_utc(start_time),
                User.create_time <= time_local_to_utc(end_time)
            ]
        )
        rows = db.session \
            .query(func.hour(User.create_time).label('hour'), func.count(User.id)) \
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
                User.create_time >= time_local_to_utc(start_time),
                User.create_time <= time_local_to_utc(end_time)
            ]
        )
        rows = db.session \
            .query(func.day(User.create_time).label('date'), func.count(User.id)) \
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
                User.create_time >= time_local_to_utc(start_time),
                User.create_time <= time_local_to_utc(end_time)
            ]
        )
        rows = db.session \
            .query(func.month(User.create_time).label('month'), func.count(User.id)) \
            .filter(*condition) \
            .group_by('month') \
            .limit(len(months)) \
            .all()
        result.update(dict(rows))
        return [(months_zerofill[i], result[month]) for i, month in enumerate(months)]
