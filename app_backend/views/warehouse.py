#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: warehouse.py
@time: 2018-04-06 00:59
"""

from __future__ import unicode_literals

import json
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
    get_warehouse_pagination,
    get_warehouse_row_by_id,
    add_warehouse,
    edit_warehouse,
    get_warehouse_choices,
    # warehouse_current_stats,
    # warehouse_former_stats,
)
from app_backend.api.warehouse import (
    get_warehouse_rows,
    # get_distinct_brand,
)
from app_backend.api.inventory import count_inventory
from app_backend.api.rack import count_rack
from app_backend.forms.warehouse import (
    WarehouseSearchForm,
    WarehouseAddForm,
    WarehouseEditForm,
)
from app_backend.models.bearing_project import Warehouse
from app_backend.permissions import permission_role_administrator, permission_role_stock_keeper
from app_backend.permissions.warehouse import (
    permission_warehouse_section_add,
    permission_warehouse_section_search,
    permission_warehouse_section_export,
    permission_warehouse_section_stats,
)
from app_common.maps.default import default_search_choices_int, default_search_choice_option_int
from app_common.maps.status_delete import (
    STATUS_DEL_OK,
    STATUS_DEL_NO)
from app_common.maps.type_role import TYPE_ROLE_MANAGER
from app_common.tools import json_default

# 定义蓝图
bp_warehouse = Blueprint('warehouse', __name__, url_prefix='/warehouse')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


@bp_warehouse.route('/lists.html', methods=['GET', 'POST'])
@login_required
@permission_warehouse_section_search.require(http_exception=403)
def lists():
    """
    产品列表
    :return:
    """
    template_name = 'warehouse/lists.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('warehouse lists')

    # 搜索条件
    form = WarehouseSearchForm(request.form)
    form.id.choices = get_warehouse_choices()
    # app.logger.info('')

    search_condition = [
        Warehouse.status_delete == STATUS_DEL_NO,
    ]
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Search Failure'), 'danger')
            # 单独处理csrf_token
            if hasattr(form, 'csrf_token') and getattr(form, 'csrf_token').errors:
                map(lambda x: flash(x, 'danger'), form.csrf_token.errors)
        else:
            if form.id.data != default_search_choice_option_int:
                search_condition.append(Warehouse.id == form.id.data)
            if form.address.data:
                search_condition.append(Warehouse.address == form.address.data)
        # 处理导出
        if form.op.data == 1:
            # 检查导出权限
            if not permission_warehouse_section_export.can():
                abort(403)
            column_names = Warehouse.__table__.columns.keys()
            query_sets = get_warehouse_rows(*search_condition)

            return excel.make_response_from_query_sets(
                query_sets=query_sets,
                column_names=column_names,
                file_type='csv',
                file_name='%s.csv' % _('warehouse lists')
            )
        # 批量删除
        if form.op.data == 2:
            warehouse_ids = request.form.getlist('warehouse_id')
            # 检查删除权限
            if not (permission_role_administrator.can() or permission_role_stock_keeper.can()):
                ext_msg = _('Permission Denied')
                flash(_('Del Failure, %(ext_msg)s', ext_msg=ext_msg), 'danger')
            else:
                permitted = True
                for warehouse_id in warehouse_ids:
                    # 检查是否正在使用
                    # 库存、货架
                    if count_inventory(**{'warehouse_id': warehouse_id, 'status_delete': STATUS_DEL_NO}):
                        ext_msg = _('Currently In Use')
                        flash(_('Del Failure, %(ext_msg)s', ext_msg=ext_msg), 'danger')
                        permitted = False
                        break
                    if count_rack(**{'warehouse_id': warehouse_id, 'status_delete': STATUS_DEL_NO}):
                        ext_msg = _('Currently In Use')
                        flash(_('Del Failure, %(ext_msg)s', ext_msg=ext_msg), 'danger')
                        permitted = False
                        break
                if permitted:
                    result_total = True
                    for warehouse_id in warehouse_ids:
                        current_time = datetime.utcnow()
                        warehouse_data = {
                            'status_delete': STATUS_DEL_OK,
                            'delete_time': current_time,
                            'update_time': current_time,
                        }
                        result = edit_warehouse(warehouse_id, warehouse_data)
                        result_total = result_total and result
                    if result_total:
                        flash(_('Del Success'), 'success')
                    else:
                        flash(_('Del Failure'), 'danger')

    # 翻页数据
    pagination = get_warehouse_pagination(form.page.data, PER_PAGE_BACKEND, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )


@bp_warehouse.route('/<int:warehouse_id>/info.html')
@login_required
def info(warehouse_id):
    """
    产品详情
    :param warehouse_id:
    :return:
    """
    # 详情数据
    warehouse_info = get_warehouse_row_by_id(warehouse_id)
    # 检查资源是否存在
    if not warehouse_info:
        abort(404)
    # 检查资源是否删除
    if warehouse_info.status_delete == STATUS_DEL_OK:
        abort(410)
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('warehouse info')
    # 渲染模板
    return render_template('warehouse/info.html', warehouse_info=warehouse_info, **document_info)


@bp_warehouse.route('/add.html', methods=['GET', 'POST'])
@login_required
@permission_warehouse_section_add.require(http_exception=403)
def add():
    """
    创建产品
    :return:
    """
    template_name = 'warehouse/add.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('warehouse add')

    # 加载创建表单
    form = WarehouseAddForm(request.form)

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
        warehouse_data = {
            'name': form.name.data,
            'address': form.address.data,
            'linkman': form.linkman.data,
            'tel': form.tel.data,
            'fax': form.fax.data,
            'create_time': current_time,
            'update_time': current_time,
        }
        result = add_warehouse(warehouse_data)
        # 创建操作成功
        if result:
            flash(_('Add Success'), 'success')
            return redirect(request.args.get('next') or url_for('warehouse.lists'))
        # 创建操作失败
        else:
            flash(_('Add Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                **document_info
            )


@bp_warehouse.route('/<int:warehouse_id>/edit.html', methods=['GET', 'POST'])
@login_required
@permission_role_stock_keeper.require(http_exception=403)
def edit(warehouse_id):
    """
    产品编辑
    """
    warehouse_info = get_warehouse_row_by_id(warehouse_id)
    # 检查资源是否存在
    if not warehouse_info:
        abort(404)
    # 检查资源是否删除
    if warehouse_info.status_delete == STATUS_DEL_OK:
        abort(410)

    template_name = 'warehouse/edit.html'

    # 加载编辑表单
    form = WarehouseEditForm(request.form)

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('warehouse edit')

    # 进入编辑页面
    if request.method == 'GET':
        # 表单赋值
        form.name.data = warehouse_info.name
        form.address.data = warehouse_info.address
        form.linkman.data = warehouse_info.linkman
        form.tel.data = warehouse_info.tel
        form.fax.data = warehouse_info.fax
        # form.create_time.data = warehouse_info.create_time
        # form.update_time.data = warehouse_info.update_time
        # 渲染页面
        return render_template(
            template_name,
            warehouse_id=warehouse_id,
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
                warehouse_id=warehouse_id,
                form=form,
                **document_info
            )
        # 表单校验成功
        current_time = datetime.utcnow()
        warehouse_data = {
            'name': form.name.data,
            'address': form.address.data,
            'linkman': form.linkman.data,
            'tel': form.tel.data,
            'fax': form.fax.data,
            'update_time': current_time,
        }
        result = edit_warehouse(warehouse_id, warehouse_data)
        # 编辑操作成功
        if result:
            flash(_('Edit Success'), 'success')
            return redirect(request.args.get('next') or url_for('warehouse.lists'))
        # 编辑操作失败
        else:
            flash(_('Edit Failure'), 'danger')
            return render_template(
                template_name,
                warehouse_id=warehouse_id,
                form=form,
                **document_info
            )


@bp_warehouse.route('/ajax/del', methods=['GET', 'POST'])
@login_required
def ajax_delete():
    """
    产品删除
    :return:
    """
    ajax_success_msg = AJAX_SUCCESS_MSG.copy()
    ajax_failure_msg = AJAX_FAILURE_MSG.copy()

    # 检查请求方法
    if not (request.method == 'GET' and request.is_xhr):
        ext_msg = _('Method Not Allowed')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查请求参数
    warehouse_id = request.args.get('warehouse_id', 0, type=int)
    if not warehouse_id:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查删除权限
    if not (permission_role_administrator.can() or permission_role_stock_keeper.can()):
        ext_msg = _('Permission Denied')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    warehouse_info = get_warehouse_row_by_id(warehouse_id)
    # 检查资源是否存在
    if not warehouse_info:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)
    # 检查资源是否删除
    if warehouse_info.status_delete == STATUS_DEL_OK:
        ext_msg = _('Already deleted')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)
    # 检查是否正在使用
    # 库存、货架
    if count_inventory(**{'warehouse_id': warehouse_id, 'status_delete': STATUS_DEL_NO}):
        ext_msg = _('Currently In Use')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)
    if count_rack(**{'warehouse_id': warehouse_id, 'status_delete': STATUS_DEL_NO}):
        ext_msg = _('Currently In Use')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    current_time = datetime.utcnow()
    warehouse_data = {
        'status_delete': STATUS_DEL_OK,
        'delete_time': current_time,
        'update_time': current_time,
    }
    result = edit_warehouse(warehouse_id, warehouse_data)
    if result:
        ajax_success_msg['msg'] = _('Del Success')
        return jsonify(ajax_success_msg)
    else:
        ajax_failure_msg['msg'] = _('Del Failure')
        return jsonify(ajax_failure_msg)

# @bp_warehouse.route('/ajax/stats', methods=['GET', 'POST'])
# @login_required
# def ajax_stats():
#     """
#     获取产品统计
#     :return:
#     """
#     time_based = request.args.get('time_based', 'hour')
#     result_warehouse_current = warehouse_current_stats(time_based)
#     result_warehouse_former = warehouse_former_stats(time_based)
#
#     line_chart_data = {
#         'labels': [label for label, _ in result_warehouse_current],
#         'datasets': [
#             {
#                 'label': '在职',
#                 'backgroundColor': 'rgba(220,220,220,0.5)',
#                 'borderColor': 'rgba(220,220,220,1)',
#                 'pointBackgroundColor': 'rgba(220,220,220,1)',
#                 'pointBorderColor': '#fff',
#                 'pointBorderWidth': 2,
#                 'data': [data for _, data in result_warehouse_current]
#             },
#             {
#                 'label': '离职',
#                 'backgroundColor': 'rgba(151,187,205,0.5)',
#                 'borderColor': 'rgba(151,187,205,1)',
#                 'pointBackgroundColor': 'rgba(151,187,205,1)',
#                 'pointBorderColor': '#fff',
#                 'pointBorderWidth': 2,
#                 'data': [data for _, data in result_warehouse_former]
#             }
#         ]
#     }
#     return json.dumps(line_chart_data, default=json_default)
#
#
# @bp_warehouse.route('/stats.html')
# @login_required
# @permission_warehouse_section_stats.require(http_exception=403)
# def stats():
#     """
#     产品统计
#     :return:
#     """
#     # 统计数据
#     time_based = request.args.get('time_based', 'hour')
#     if time_based not in ['hour', 'date', 'month']:
#         abort(404)
#     # 文档信息
#     document_info = DOCUMENT_INFO.copy()
#     document_info['TITLE'] = _('warehouse stats')
#     # 渲染模板
#     return render_template(
#         'warehouse/stats.html',
#         time_based=time_based,
#         **document_info
#     )
#
#
# @bp_warehouse.route('/<int:warehouse_id>/stats.html')
# @login_required
# @permission_warehouse_section_stats.require(http_exception=403)
# def stats_item(warehouse_id):
#     """
#     产品统计明细
#     :param warehouse_id:
#     :return:
#     """
#     warehouse_info = get_warehouse_row_by_id(warehouse_id)
#     # 检查资源是否存在
#     if not warehouse_info:
#         abort(404)
#     # 检查资源是否删除
#     if warehouse_info.status_delete == STATUS_DEL_OK:
#         abort(410)
#
#     # 统计数据
#     warehouse_stats_item_info = get_warehouse_row_by_id(warehouse_id)
#     # 文档信息
#     document_info = DOCUMENT_INFO.copy()
#     document_info['TITLE'] = _('warehouse stats item')
#     # 渲染模板
#     return render_template(
#         'warehouse/stats_item.html',
#         warehouse_stats_item_info=warehouse_stats_item_info,
#         **document_info
#     )
