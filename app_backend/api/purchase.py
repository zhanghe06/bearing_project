#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: purchase.py
@time: 2018-07-27 20:07
"""

from copy import copy
from datetime import datetime
from sqlalchemy.sql import func
from app_backend.databases.bearing import db_bearing
from app_backend.api.customer import get_customer_rows_by_ids
from app_backend.api.user import get_user_rows_by_ids
from app_common.libs.mysql_orm_op import DbInstance
from app_backend.models.model_bearing import Purchase, PurchaseItems, Inventory, Warehouse, Rack
from app_common.maps.default import DEFAULT_SEARCH_CHOICES_INT
from app_common.maps.status_delete import STATUS_DEL_NO
from app_common.tools.date_time import get_current_day_time_ends, get_hours, time_local_to_utc, \
    get_current_month_time_ends, get_days, get_current_year_time_ends, get_months
from app_common.maps.status_order import STATUS_ORDER_OK
from app_common.maps.status_audit import STATUS_AUDIT_OK, STATUS_AUDIT_NO

db_instance = DbInstance(db_bearing)


def get_purchase_row_by_id(purchase_id):
    """
    通过 id 获取信息
    :param purchase_id:
    :return: None/object
    """
    return db_instance.get_row_by_id(Purchase, purchase_id)


def get_purchase_row(*args, **kwargs):
    """
    获取信息
    :param args:
    :param kwargs:
    :return: None/object
    """
    return db_instance.get_row(Purchase, *args, **kwargs)


def get_purchase_rows(*args, **kwargs):
    """
    获取列表
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_rows(Purchase, *args, **kwargs)


def add_purchase(purchase_data):
    """
    添加信息
    :param purchase_data:
    :return: None/Value of user.id
    :except:
    """
    return db_instance.add(Purchase, purchase_data)


def edit_purchase(purchase_id, purchase_data):
    """
    修改信息
    :param purchase_id:
    :param purchase_data:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.edit(Purchase, purchase_id, purchase_data)


def delete_purchase(purchase_id):
    """
    删除信息
    :param purchase_id:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.delete(Purchase, purchase_id)


def delete_purchase_table():
    """
    清空表
    :return:
    """
    return db_instance.delete_table(Purchase)


def count_purchase(*args, **kwargs):
    """
    计数
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.count(Purchase, *args, **kwargs)


def get_purchase_pagination(page=1, per_page=10, *args, **kwargs):
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
    rows = db_instance.get_pagination(Purchase, page, per_page, *args, **kwargs)
    return rows


def get_distinct_purchase_uid(*args, **kwargs):
    """
    获取用户
    :param args:
    :param kwargs:
    :return: List
    """
    field = 'uid'
    return map(lambda x: getattr(x, field), db_instance.get_distinct_field(Purchase, field, *args, **kwargs))


def get_purchase_user_list_choices():
    purchase_user_list = copy(DEFAULT_SEARCH_CHOICES_INT)
    uid_list = get_distinct_purchase_uid(status_delete=STATUS_DEL_NO)
    user_rows = get_user_rows_by_ids(uid_list)
    purchase_user_list.extend([(user.id, user.name) for user in user_rows])
    return purchase_user_list


def audit_purchase(purchase_id):
    """
    审核信息
    :param purchase_id:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    try:
        current_time = datetime.utcnow()

        # 更新审核状态
        purchase_obj = db_instance.db_instance.session.query(Purchase).filter(Purchase.id == purchase_id)
        purchase_info = purchase_obj.first()  # type: Purchase
        if not purchase_info:
            raise Exception('Purchase not found')
        if purchase_info.status_audit == STATUS_AUDIT_OK:
            return True
        purchase_info.status_audit = STATUS_AUDIT_OK  # 审核成功
        purchase_info.audit_time = current_time
        purchase_info.update_time = current_time

        # 获取进货明细
        purchase_items_obj = db_instance.db_instance.session.query(PurchaseItems).filter(PurchaseItems.purchase_id == purchase_id)
        purchase_items = purchase_items_obj.all()

        # 遍历进货型号
        for purchase_item in purchase_items:
            # 查询库存
            inventory_obj = db_instance.db_instance.session.query(Inventory).filter(
                Inventory.production_id == purchase_item.production_id,
                Inventory.warehouse_id == purchase_item.warehouse_id,
                Inventory.rack_id == purchase_item.rack_id,
            )
            inventory_info = inventory_obj.first()  # type: Inventory
            if inventory_info:
                # 增加库存数量
                stock_qty_current = inventory_info.stock_qty_current + purchase_item.quantity
                if stock_qty_current < 0:
                    raise Exception('Inventory insufficient')
                inventory_info.stock_qty_current = stock_qty_current
                inventory_info.update_time = current_time
            else:
                # 获取仓库
                warehouse_info = db_instance.db_instance.session.query(Warehouse).filter(
                    Warehouse.id == purchase_item.warehouse_id).first()
                if not warehouse_info:
                    raise Exception('Warehouse not found')
                # 获取仓位
                rack_info = db_instance.db_instance.session.query(Rack).filter(Rack.id == purchase_item.rack_id).first()
                if not rack_info:
                    raise Exception('Rack not found')
                # 新建库存记录
                inventory_data = Inventory(
                    production_id=purchase_item.production_id,
                    production_brand=purchase_item.production_brand,
                    production_model=purchase_item.production_model,
                    production_sku=purchase_item.production_sku,
                    warehouse_id=purchase_item.warehouse_id,
                    warehouse_name=warehouse_info.name,
                    rack_id=purchase_item.rack_id,
                    rack_name=rack_info.name,
                    stock_qty_current=purchase_item.quantity,
                    note=purchase_item.note,
                    create_time=current_time,
                    update_time=current_time,
                )
                db_instance.db_instance.session.add(inventory_data)

        db_instance.db_instance.session.commit()
        return True
    except Exception as e:
        db_instance.db_instance.session.rollback()
        raise e


def cancel_audit_purchase(purchase_id):
    """
    取消审核
    :param purchase_id:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    try:
        current_time = datetime.utcnow()

        # 更新审核状态
        purchase_obj = db_instance.db_instance.session.query(Purchase).filter(Purchase.id == purchase_id)
        purchase_info = purchase_obj.first()  # type: Purchase
        if not purchase_info:
            raise Exception('Purchase not found')
        if purchase_info.status_audit == STATUS_AUDIT_NO:
            return True
        purchase_info.status_audit = STATUS_AUDIT_NO  # 取消审核
        purchase_info.audit_time = current_time
        purchase_info.update_time = current_time

        # 获取进货明细
        purchase_items_obj = db_instance.db_instance.session.query(PurchaseItems).filter(PurchaseItems.purchase_id == purchase_id)
        purchase_items = purchase_items_obj.all()

        # 遍历进货型号
        for purchase_item in purchase_items:
            # 查询库存
            inventory_obj = db_instance.db_instance.session.query(Inventory).filter(
                Inventory.production_id == purchase_item.production_id,
                Inventory.warehouse_id == purchase_item.warehouse_id,
                Inventory.rack_id == purchase_item.rack_id,
            )
            inventory_info = inventory_obj.first()  # type: Inventory
            if not inventory_info:
                raise Exception('Inventory not found')
            # 扣减库存数量
            stock_qty_current = inventory_info.stock_qty_current - purchase_item.quantity
            if stock_qty_current < 0:
                raise Exception('Inventory insufficient')
            inventory_info.stock_qty_current = stock_qty_current
            inventory_info.update_time = current_time

        db_instance.db_instance.session.commit()
        return True
    except Exception as e:
        db_instance.db_instance.session.rollback()
        raise e
