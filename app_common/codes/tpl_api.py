#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: tpl_api.py
@time: 2018-07-18 14:09
"""

from __future__ import unicode_literals


CODE_TEMPLATE_API = '''
#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: %(section)s.py
@time: %(time)s
"""

from datetime import datetime
from sqlalchemy.sql import func
from app_backend import db
from app_common.libs.mysql_orm_op import DbInstance
from app_backend.models.bearing_project import %(model)s

db_instance = DbInstance(db)


def get_%(section)s_row_by_id(%(section)s_id):
    """
    通过 id 获取信息
    :param %(section)s_id:
    :return: None/object
    """
    return db_instance.get_row_by_id(%(model)s, %(section)s_id)


def get_%(section)s_row(*args, **kwargs):
    """
    获取信息
    :param args:
    :param kwargs:
    :return: None/object
    """
    return db_instance.get_row(%(model)s, *args, **kwargs)


def get_%(section)s_rows(*args, **kwargs):
    """
    获取列表
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_rows(%(model)s, *args, **kwargs)


def get_%(section)s_rows_by_ids(pk_ids):
    """
    通过一组 ids 获取信息列表
    :param pk_ids:
    :return:
    """
    return db_instance.get_rows_by_ids(%(model)s, pk_ids)


def add_%(section)s(%(section)s_data):
    """
    添加信息
    :param %(section)s_data:
    :return: None/Value of user.id
    :except:
    """
    return db_instance.add(%(model)s, %(section)s_data)


def edit_%(section)s(%(section)s_id, %(section)s_data):
    """
    修改信息
    :param %(section)s_id:
    :param %(section)s_data:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.edit(%(model)s, %(section)s_id, %(section)s_data)


def delete_%(section)s(%(section)s_id):
    """
    删除信息
    :param %(section)s_id:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.delete(%(model)s, %(section)s_id)


def get_%(section)s_pagination(page=1, per_page=10, *args, **kwargs):
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
    rows = db_instance.get_pagination(%(model)s, page, per_page, *args, **kwargs)
    return rows
'''
