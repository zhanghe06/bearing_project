#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: inventory.py
@time: 2018-04-06 12:20
"""

from datetime import datetime
from sqlalchemy.sql import func
from app_backend import db
from app_common.libs.mysql_orm_op import DbInstance
from app_backend.models.bearing_project import Inventory, Warehouse, Rack
from app_common.tools.date_time import get_current_day_time_ends, get_hours, time_local_to_utc, \
    get_current_month_time_ends, get_days, get_current_year_time_ends, get_months
from app_common.maps.status_order import STATUS_ORDER_OK

db_instance = DbInstance(db)


def get_inventory_row_by_id(inventory_id):
    """
    通过 id 获取信息
    :param inventory_id:
    :return: None/object
    """
    return db_instance.get_row_by_id(Inventory, inventory_id)


def get_inventory_row(*args, **kwargs):
    """
    获取信息
    :param args:
    :param kwargs:
    :return: None/object
    """
    return db_instance.get_row(Inventory, *args, **kwargs)


def get_inventory_rows(*args, **kwargs):
    """
    获取列表
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_rows(Inventory, *args, **kwargs)


def add_inventory(inventory_data):
    """
    添加信息
    :param inventory_data:
    :return: None/Value of user.id
    :except:
    """
    return db_instance.add(Inventory, inventory_data)


def edit_inventory(inventory_id, inventory_data):
    """
    修改信息
    :param inventory_id:
    :param inventory_data:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.edit(Inventory, inventory_id, inventory_data)


def delete_inventory(inventory_id):
    """
    删除信息
    :param inventory_id:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.delete(Inventory, inventory_id)


def count_inventory(*args, **kwargs):
    """
    计数
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.count(Inventory, *args, **kwargs)


def get_inventory_pagination(page=1, per_page=10, *args, **kwargs):
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
    rows = db_instance.get_pagination(Inventory, page, per_page, *args, **kwargs)
    return rows


def get_distinct_inventory_brand(*args, **kwargs):
    """
    获取品牌
    :param args:
    :param kwargs:
    :return: List
    """
    field = 'production_brand'
    return map(lambda x: getattr(x, field), db_instance.get_distinct_field(Inventory, field, *args, **kwargs))


def transfer_inventory(inventory_id, warehouse_id, rack_id, num):
    """
    库存移位
    :param inventory_id:
    :param warehouse_id:
    :param rack_id:
    :param num:
    :return: Boole
    :except:
    """
    try:
        inventory_obj_from = db_instance.db_instance.session.query(Inventory).filter(Inventory.id == inventory_id)
        inventory_info_from = inventory_obj_from.first()

        # 数量校验
        if inventory_info_from.stock_qty < num or num < 0:
            raise Exception('Quantity out of range')
        # 库位校验
        if inventory_info_from.warehouse_id == warehouse_id and inventory_info_from.rack_id == rack_id:
            raise Exception('Same warehouse rack')

        current_time = datetime.utcnow()

        # 1、原始库位操作
        if inventory_info_from.stock_qty == num:
            # 清空原库
            inventory_obj_from.delete()
        else:
            # 更新原库
            inventory_data = {
                'stock_qty': inventory_info_from.stock_qty - num,
                'update_time': current_time,
            }
            inventory_obj_from.update(inventory_data)

        # 2、目标库位操作

        # 查询目标库位的同型号记录
        inventory_obj_to = db_instance.db_instance.session.query(Inventory).filter(
            Inventory.warehouse_id == warehouse_id,
            Inventory.rack_id == rack_id,
            Inventory.production_id == inventory_info_from.production_id,
        )
        inventory_info_to = inventory_obj_to.first()

        if inventory_info_to:
            # 更新记录
            inventory_data = {
                'stock_qty': inventory_info_to.stock_qty + num,
                'update_time': current_time,
            }
            inventory_obj_to.update(inventory_data)
        else:
            # 插入记录
            # 获取仓库
            warehouse_info = db_instance.db_instance.session.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
            if not warehouse_info:
                raise Exception('Warehouse not found')
            # 获取仓位
            rack_info = db_instance.db_instance.session.query(Rack).filter(Rack.id == rack_id).first()
            if not rack_info:
                raise Exception('Rack not found')
            inventory_data = Inventory(
                production_id=inventory_info_from.production_id,
                production_brand=inventory_info_from.production_brand,
                production_model=inventory_info_from.production_model,
                production_sku=inventory_info_from.production_sku,
                warehouse_id=warehouse_id,
                warehouse_name=warehouse_info.warehouse_name,
                rack_id=rack_id,
                rack_name=rack_info.rack_name,
                stock_qty=num,
                note=inventory_info_from.note,
                create_time=current_time,
                update_time=current_time,
            )
            db_instance.db_instance.session.add(inventory_data)

        db_instance.db_instance.session.commit()
        return True
    except Exception as e:
        db_instance.db_instance.session.rollback()
        raise e
