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


def add_quote_item(quote_item_data):
    """
    添加信息
    :param quote_item_data:
    :return: None/Value of user.id
    :except:
    """
    return db_instance.add(QuoteItem, quote_item_data)


def edit_quote_item(quote_item_id, quote_item_data):
    """
    修改信息
    :param quote_item_id:
    :param quote_item_data:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.edit(QuoteItem, quote_item_id, quote_item_data)


def delete_quote_item(quote_item_id):
    """
    删除信息
    :param quote_item_id:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.delete(QuoteItem, quote_item_id)
