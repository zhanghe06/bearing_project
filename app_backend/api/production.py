#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: productionion.py
@time: 2018-03-16 09:59
"""

from app_backend import db
from app_common.libs.mysql_orm_op import DbInstance
from app_backend.models.bearing_project import Production
from app_common.maps.default import default_choices_int
from app_common.maps.status_delete import STATUS_DEL_NO

db_instance = DbInstance(db)


def get_production_row_by_id(production_id):
    """
    通过 id 获取信息
    :param production_id:
    :return: None/object
    """
    return db_instance.get_row_by_id(Production, production_id)


def get_production_row(*args, **kwargs):
    """
    获取信息
    :param args:
    :param kwargs:
    :return: None/object
    """
    return db_instance.get_row(Production, *args, **kwargs)


def get_production_rows(*args, **kwargs):
    """
    获取列表
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_rows(Production, *args, **kwargs)


def get_production_limit_rows_by_last_id(last_pk_id, limit_num, *args, **kwargs):
    """
    通过最后一个主键 id 获取最新信息列表
    :param last_pk_id:
    :param limit_num:
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_limit_rows_by_last_id(Production, last_pk_id, limit_num, *args, **kwargs)


def add_production(production_data):
    """
    添加信息
    :param production_data:
    :return: None/Value of user.id
    :except:
    """
    return db_instance.add(Production, production_data)


def edit_production(production_id, production_data):
    """
    修改信息
    :param production_id:
    :param production_data:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.edit(Production, production_id, production_data)


def delete_production(production_id):
    """
    删除信息
    :param production_id:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.delete(Production, production_id)


def get_production_pagination(page=1, per_page=10, *args, **kwargs):
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
    rows = db_instance.get_pagination(Production, page, per_page, *args, **kwargs)
    return rows


def delete_production_table():
    """
    清空表
    :return:
    """
    return db_instance.delete_table(Production)


def count_production(*args, **kwargs):
    """
    计数
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.count(Production, *args, **kwargs)


def get_distinct_production_brand(*args, **kwargs):
    """
    获取品牌
    :param args:
    :param kwargs:
    :return: List
    """
    field = 'production_brand'
    return map(lambda x: getattr(x, field), db_instance.get_distinct_field(Production, field, *args, **kwargs))


def get_production_choices(keywords):
    """
    获取选项
    :param keywords:
    :return:
    """

    from app_backend.clients.client_es import es_client
    from app_common.libs.es import ES

    es = ES(es_client)

    index = 'production'
    doc_type = 'bearing'
    field = 'production_model'
    # keywords = '7008ACDGA/P4A'
    query_from = 0
    size = 0

    es_result = es.search_fulltext(index, doc_type, field, keywords, query_from, size)

    catalogue_choices = map(lambda x: (
        x['id'], x['value'], '%s <small class="text-muted">%s</small>' % (x['label'], x['info']['production_brand']),
        x['info']['production_brand']), es_result['data'])
    return catalogue_choices
