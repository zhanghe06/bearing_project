#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: quotation_item.py
@time: 2018-03-16 10:00
"""


from app_common.libs.mysql_orm_op import DbInstance
from app_backend.models.bearing_project import QuoteItem
from app_backend import db

db_instance = DbInstance(db)


def get_quote_item_rows(*args, **kwargs):
    """
    获取列表
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_rows(QuoteItem, *args, **kwargs)
