#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: inventory.py
@time: 2018-04-06 00:59
"""


from __future__ import unicode_literals

import json
from copy import copy
from datetime import datetime

from flask import (
    request,
    flash,
    render_template,
    url_for,
    redirect,
    abort,
    jsonify,
    Blueprint,
)
from flask_babel import gettext as _
from flask_login import login_required

from app_backend import app
from app_backend import excel
from app_backend.api.warehouse import (
    get_warehouse_choices,
)
from app_backend.api.rack import (
    get_rack_choices,
)
from app_backend.api.inventory import (
    get_inventory_pagination,
    get_inventory_row_by_id,
    add_inventory,
    edit_inventory,
    # inventory_current_stats,
    # inventory_former_stats,
)
from app_backend.api.inventory import (
    get_inventory_rows,
    # get_distinct_brand,
)
from app_backend.forms.inventory import (
    InventorySearchForm,
    InventoryAddForm,
    InventoryEditForm,
)
from app_backend.models.bearing_project import Inventory
from app_backend.permissions import (
    permission_inventory_section_add,
    permission_inventory_section_search,
    permission_inventory_section_export,
    permission_inventory_section_stats,
    permission_role_stock_keeper,
)
from app_common.maps.default import default_choices_int, default_choice_option_int
from app_common.maps.status_delete import (
    STATUS_DEL_OK,
)
from app_common.maps.type_role import TYPE_ROLE_MANAGER
from app_common.tools import json_default

# 定义蓝图
bp_inventory = Blueprint('inventory', __name__, url_prefix='/inventory')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


@bp_inventory.route('/lists.html', methods=['GET', 'POST'])
@bp_inventory.route('/lists/<int:page>.html', methods=['GET', 'POST'])
@login_required
# @permission_inventory_section_search.require(http_exception=403)
def lists(page=1):
    """
    库存列表
    :param page:
    :return:
    """
    template_name = 'inventory/lists.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('inventory lists')

    # 搜索条件
    form = InventorySearchForm(request.form)
    form.warehouse_id.choices = get_warehouse_choices()
    form.rack_id.choices = get_rack_choices(form.warehouse_id.data)
    # app.logger.info('')

    search_condition = []
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Search Failure'), 'danger')
            # 单独处理csrf_token
            if hasattr(form, 'csrf_token') and getattr(form, 'csrf_token').errors:
                map(lambda x: flash(x, 'danger'), form.csrf_token.errors)
        else:
            if form.warehouse_id.data != default_choice_option_int:
                search_condition.append(Inventory.warehouse_id == form.warehouse_id.data)
            if form.rack_id.data != default_choice_option_int:
                search_condition.append(Inventory.rack_id == form.rack_id.data)
        # 处理导出
        if form.op.data == 1:
            # 检查导出权限
            if not permission_inventory_section_export.can():
                abort(403)
            column_names = Inventory.__table__.columns.keys()
            query_sets = get_inventory_rows(*search_condition)

            return excel.make_response_from_query_sets(
                query_sets=query_sets,
                column_names=column_names,
                file_type='csv',
                file_name='%s.csv' % _('inventory lists')
            )
    # 翻页数据
    pagination = get_inventory_pagination(page, PER_PAGE_BACKEND, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )


@bp_inventory.route('/<int:inventory_id>/info.html')
@login_required
def info(inventory_id):
    """
    库存详情
    :param inventory_id:
    :return:
    """
    # 详情数据
    inventory_info = get_inventory_row_by_id(inventory_id)
    # 检查资源是否存在
    if not inventory_info:
        abort(404)
    # 检查资源是否删除
    if inventory_info.status_delete == STATUS_DEL_OK:
        abort(410)
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('inventory info')
    # 渲染模板
    return render_template('inventory/info.html', inventory_info=inventory_info, **document_info)


@bp_inventory.route('/add.html', methods=['GET', 'POST'])
@login_required
@permission_inventory_section_add.require(http_exception=403)
def add():
    """
    创建库存
    :return:
    """
    template_name = 'inventory/add.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('inventory add')

    # 加载创建表单
    form = InventoryAddForm(request.form)

    # 进入创建页面
    if request.method == 'GET':
        # 渲染页面
        return render_template(
            template_name,
            form=form,
            **document_info
        )

    # 处理创建请求
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Add Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                **document_info
            )

        # 表单校验成功
        current_time = datetime.utcnow()
        inventory_data = {
            'warehouse_id': form.warehouse_id.data,
            'name': form.name.data,
            'create_time': current_time,
            'update_time': current_time,
        }
        result = add_inventory(inventory_data)
        # 创建操作成功
        if result:
            flash(_('Add Success'), 'success')
            return redirect(request.args.get('next') or url_for('inventory.lists'))
        # 创建操作失败
        else:
            flash(_('Add Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                **document_info
            )


@bp_inventory.route('/<int:inventory_id>/edit.html', methods=['GET', 'POST'])
@login_required
@permission_role_stock_keeper.require(http_exception=403)
def edit(inventory_id):
    """
    库存编辑
    """
    inventory_info = get_inventory_row_by_id(inventory_id)
    # 检查资源是否存在
    if not inventory_info:
        abort(404)
    # 检查资源是否删除
    if inventory_info.status_delete == STATUS_DEL_OK:
        abort(410)

    template_name = 'inventory/edit.html'

    # 加载编辑表单
    form = InventoryEditForm(request.form)

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('inventory edit')

    # 进入编辑页面
    if request.method == 'GET':
        # 表单赋值
        form.warehouse_id.data = inventory_info.warehouse_id
        form.name.data = inventory_info.name
        form.create_time.data = inventory_info.create_time
        form.update_time.data = inventory_info.update_time
        # 渲染页面
        return render_template(
            template_name,
            inventory_id=inventory_id,
            form=form,
            **document_info
        )

    # 处理编辑请求
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Edit Failure'), 'danger')
            return render_template(
                template_name,
                inventory_id=inventory_id,
                form=form,
                **document_info
            )
        # 表单校验成功
        current_time = datetime.utcnow()
        inventory_data = {
            'warehouse_id': form.warehouse_id.data,
            'name': form.name.data,
            'update_time': current_time,
        }
        result = edit_inventory(inventory_id, inventory_data)
        # 编辑操作成功
        if result:
            flash(_('Edit Success'), 'success')
            return redirect(request.args.get('next') or url_for('inventory.lists'))
        # 编辑操作失败
        else:
            flash(_('Edit Failure'), 'danger')
            return render_template(
                template_name,
                inventory_id=inventory_id,
                form=form,
                **document_info
            )


@bp_inventory.route('/ajax/del', methods=['GET', 'POST'])
@login_required
def ajax_delete():
    """
    库存删除
    :return:
    """
    ajax_success_msg = AJAX_SUCCESS_MSG.copy()
    ajax_failure_msg = AJAX_FAILURE_MSG.copy()

    # 检查请求方法
    if not (request.method == 'GET' and request.is_xhr):
        ajax_failure_msg['msg'] = _('Del Failure')  # Method Not Allowed
        return jsonify(ajax_failure_msg)

    # 检查请求参数
    inventory_id = request.args.get('inventory_id', 0, type=int)
    if not inventory_id:
        ajax_failure_msg['msg'] = _('Del Failure')  # ID does not exist
        return jsonify(ajax_failure_msg)

    # 检查删除权限
    if not permission_role_stock_keeper.can():
        ajax_failure_msg['msg'] = _('Del Failure')  # Permission Denied
        return jsonify(ajax_failure_msg)

    inventory_info = get_inventory_row_by_id(inventory_id)
    # 检查资源是否存在
    if not inventory_info:
        ajax_failure_msg['msg'] = _('Del Failure')  # ID does not exist
        return jsonify(ajax_failure_msg)
    # 检查资源是否删除
    if inventory_info.status_delete == STATUS_DEL_OK:
        ajax_success_msg['msg'] = _('Del Success')  # Already deleted
        return jsonify(ajax_success_msg)

    current_time = datetime.utcnow()
    inventory_data = {
        'status_delete': STATUS_DEL_OK,
        'delete_time': current_time,
        'update_time': current_time,
    }
    result = edit_inventory(inventory_id, inventory_data)
    if result:
        ajax_success_msg['msg'] = _('Del Success')
        return jsonify(ajax_success_msg)
    else:
        ajax_failure_msg['msg'] = _('Del Failure')
        return jsonify(ajax_failure_msg)


# @bp_inventory.route('/ajax/stats', methods=['GET', 'POST'])
# @login_required
# def ajax_stats():
#     """
#     获取库存统计
#     :return:
#     """
#     time_based = request.args.get('time_based', 'hour')
#     result_inventory_current = inventory_current_stats(time_based)
#     result_inventory_former = inventory_former_stats(time_based)
#
#     line_chart_data = {
#         'labels': [label for label, _ in result_inventory_current],
#         'datasets': [
#             {
#                 'label': '在职',
#                 'backgroundColor': 'rgba(220,220,220,0.5)',
#                 'borderColor': 'rgba(220,220,220,1)',
#                 'pointBackgroundColor': 'rgba(220,220,220,1)',
#                 'pointBorderColor': '#fff',
#                 'pointBorderWidth': 2,
#                 'data': [data for _, data in result_inventory_current]
#             },
#             {
#                 'label': '离职',
#                 'backgroundColor': 'rgba(151,187,205,0.5)',
#                 'borderColor': 'rgba(151,187,205,1)',
#                 'pointBackgroundColor': 'rgba(151,187,205,1)',
#                 'pointBorderColor': '#fff',
#                 'pointBorderWidth': 2,
#                 'data': [data for _, data in result_inventory_former]
#             }
#         ]
#     }
#     return json.dumps(line_chart_data, default=json_default)
#
#
# @bp_inventory.route('/stats.html')
# @login_required
# @permission_inventory_section_stats.require(http_exception=403)
# def stats():
#     """
#     库存统计
#     :return:
#     """
#     # 统计数据
#     time_based = request.args.get('time_based', 'hour')
#     if time_based not in ['hour', 'date', 'month']:
#         abort(404)
#     # 文档信息
#     document_info = DOCUMENT_INFO.copy()
#     document_info['TITLE'] = _('inventory stats')
#     # 渲染模板
#     return render_template(
#         'inventory/stats.html',
#         time_based=time_based,
#         **document_info
#     )
#
#
# @bp_inventory.route('/<int:inventory_id>/stats.html')
# @login_required
# @permission_inventory_section_stats.require(http_exception=403)
# def stats_item(inventory_id):
#     """
#     库存统计明细
#     :param inventory_id:
#     :return:
#     """
#     inventory_info = get_inventory_row_by_id(inventory_id)
#     # 检查资源是否存在
#     if not inventory_info:
#         abort(404)
#     # 检查资源是否删除
#     if inventory_info.status_delete == STATUS_DEL_OK:
#         abort(410)
#
#     # 统计数据
#     inventory_stats_item_info = get_inventory_row_by_id(inventory_id)
#     # 文档信息
#     document_info = DOCUMENT_INFO.copy()
#     document_info['TITLE'] = _('inventory stats item')
#     # 渲染模板
#     return render_template(
#         'inventory/stats_item.html',
#         inventory_stats_item_info=inventory_stats_item_info,
#         **document_info
#     )

