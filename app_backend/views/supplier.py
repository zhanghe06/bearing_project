#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: supplier.py
@time: 2018-07-17 14:53
"""

from __future__ import unicode_literals

import json
from copy import deepcopy
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
from flask_login import login_required, current_user

from app_backend import (
    app,
    excel,
)

# 定义蓝图
from app_backend.api.production_sensitive import count_production_sensitive
from app_backend.api.quotation import count_quotation
from app_backend.api.supplier import get_supplier_rows, edit_supplier, get_supplier_pagination, get_supplier_row_by_id, \
    supplier_end_user_stats, supplier_middleman_stats, add_supplier
from app_backend.api.user import get_user_rows, get_user_choices
from app_backend.forms.supplier import SupplierSearchForm, SupplierEditForm, SupplierAddForm
from app_backend.models.bearing_project import Supplier
from app_backend.permissions import permission_supplier_section_export, SupplierItemDelPermission, \
    permission_supplier_section_search, SupplierItemGetPermission, permission_supplier_section_stats
from app_backend.signals.supplier import signal_supplier_status_delete
from app_common.maps.default import default_search_choice_option_int, default_search_choices_int
from app_common.maps.status_delete import STATUS_DEL_NO, STATUS_DEL_OK
from app_common.maps.type_company import TYPE_COMPANY_CHOICES
from app_common.maps.type_role import TYPE_ROLE_SALES
from app_common.tools import json_default

bp_supplier = Blueprint('supplier', __name__, url_prefix='/supplier')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
PER_PAGE_BACKEND_MODAL = app.config.get('PER_PAGE_BACKEND_MODAL', 10)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


def get_sales_user_list():
    sales_user_list = deepcopy(default_search_choices_int)
    user_list = get_user_rows(**{'role_id': TYPE_ROLE_SALES})
    sales_user_list.extend([(0, '-')])
    sales_user_list.extend([(user.id, user.name) for user in user_list])
    return sales_user_list


@bp_supplier.route('/lists.html', methods=['GET', 'POST'])
@login_required
@permission_supplier_section_search.require(http_exception=403)
def lists():
    """
    渠道列表
    :return:
    """
    template_name = 'supplier/lists.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('supplier lists')

    # 搜索条件
    form = SupplierSearchForm(request.form)
    form.owner_uid.choices = get_sales_user_list()
    # app.logger.info('')

    search_condition = [
        Supplier.status_delete == STATUS_DEL_NO,
    ]
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Search Failure'), 'danger')
            # 单独处理csrf_token
            if hasattr(form, 'csrf_token') and getattr(form, 'csrf_token').errors:
                map(lambda x: flash(x, 'danger'), form.csrf_token.errors)
        else:
            if form.company_name.data:
                search_condition.append(Supplier.company_name.like('%%%s%%' % form.company_name.data))
            if form.company_type.data != default_search_choice_option_int:
                search_condition.append(Supplier.company_type == form.company_type.data)
            if form.owner_uid.data != default_search_choice_option_int:
                search_condition.append(Supplier.owner_uid == form.owner_uid.data)
            if form.start_create_time.data:
                search_condition.append(Supplier.create_time >= form.start_create_time.data)
            if form.end_create_time.data:
                search_condition.append(Supplier.create_time <= form.end_create_time.data)
        # 处理导出
        if form.op.data == 1:
            # 检查导出权限
            if not permission_supplier_section_export.can():
                abort(403)
            column_names = Supplier.__table__.columns.keys()
            query_sets = get_supplier_rows(*search_condition)

            return excel.make_response_from_query_sets(
                query_sets=query_sets,
                column_names=column_names,
                file_type='csv',
                file_name='%s.csv' % _('supplier lists')
            )
        # 批量删除
        if form.op.data == 2:
            supplier_ids = request.form.getlist('supplier_id')
            # 检查删除权限
            permitted = True
            for supplier_id in supplier_ids:
                # 明细权限
                supplier_item_del_permission = SupplierItemDelPermission(supplier_id)
                if not supplier_item_del_permission.can():
                    ext_msg = _('Permission Denied')
                    flash(_('Del Failure, %(ext_msg)s', ext_msg=ext_msg), 'danger')
                    permitted = False
                    break
                # 检查是否正在使用
                # 报价、订单、敏感型号
                if count_quotation(**{'cid': supplier_id, 'status_delete': STATUS_DEL_NO}):
                    ext_msg = _('Currently In Use')
                    flash(_('Del Failure, %(ext_msg)s', ext_msg=ext_msg), 'danger')
                    permitted = False
                    break
                if count_production_sensitive(**{'cid': supplier_id, 'status_delete': STATUS_DEL_NO}):
                    ext_msg = _('Currently In Use')
                    flash(_('Del Failure, %(ext_msg)s', ext_msg=ext_msg), 'danger')
                    permitted = False
                    break
            if permitted:
                result_total = True
                for supplier_id in supplier_ids:
                    current_time = datetime.utcnow()
                    supplier_data = {
                        'status_delete': STATUS_DEL_OK,
                        'delete_time': current_time,
                        'update_time': current_time,
                    }
                    result = edit_supplier(supplier_id, supplier_data)
                    if result:
                        # 发送删除信号
                        signal_data = {
                            'supplier_id': supplier_id,
                            'status_delete': STATUS_DEL_OK,
                            'current_time': current_time,
                        }
                        signal_supplier_status_delete.send(app, **signal_data)
                    result_total = result_total and result
                if result_total:
                    flash(_('Del Success'), 'success')
                else:
                    flash(_('Del Failure'), 'danger')

    # 翻页数据
    pagination = get_supplier_pagination(form.page.data, PER_PAGE_BACKEND, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )


@bp_supplier.route('/search.html', methods=['GET', 'POST'])
@login_required
@permission_supplier_section_search.require(http_exception=403)
def search():
    """
    渠道搜索
    :return:
    """
    template_name = 'supplier/search_modal.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('Supplier Search')

    # 搜索条件
    form = SupplierSearchForm(request.form)
    form.owner_uid.choices = get_sales_user_list()
    # app.logger.info('')

    search_condition = [
        Supplier.status_delete == STATUS_DEL_NO,
    ]
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Search Failure'), 'danger')
            # 单独处理csrf_token
            if hasattr(form, 'csrf_token') and getattr(form, 'csrf_token').errors:
                map(lambda x: flash(x, 'danger'), form.csrf_token.errors)
        else:
            if form.company_type.data != default_search_choice_option_int:
                search_condition.append(Supplier.company_type == form.company_type.data)
            if form.company_name.data:
                search_condition.append(Supplier.company_name.like('%%%s%%' % form.company_name.data))
    # 翻页数据
    pagination = get_supplier_pagination(form.page.data, PER_PAGE_BACKEND_MODAL, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )


@bp_supplier.route('/<int:supplier_id>/info.html')
@login_required
def info(supplier_id):
    """
    渠道详情
    :param supplier_id:
    :return:
    """
    # 检查读取权限
    supplier_item_get_permission = SupplierItemGetPermission(supplier_id)
    if not supplier_item_get_permission.can():
        abort(403)
    # 详情数据
    supplier_info = get_supplier_row_by_id(supplier_id)
    # 检查资源是否存在
    if not supplier_info:
        abort(404)
    # 检查资源是否删除
    if supplier_info.status_delete == STATUS_DEL_OK:
        abort(410)
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('supplier info')
    # 渲染模板
    return render_template('supplier/info.html', supplier_info=supplier_info, **document_info)


@bp_supplier.route('/add.html', methods=['GET', 'POST'])
@login_required
# @permission_supplier_section_add.require(http_exception=403)
def add():
    """
    创建渠道
    :return:
    """
    template_name = 'supplier/add.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('supplier add')

    # 加载创建表单
    form = SupplierAddForm(request.form)

    form.company_type.choices = TYPE_COMPANY_CHOICES
    form.owner_uid.choices = get_user_choices()
    form.owner_uid.data = current_user.id

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
            flash(form.errors, 'danger')
            flash(_('Add Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                **document_info
            )

        # 表单校验成功
        current_time = datetime.utcnow()
        supplier_data = {
            'company_name': form.company_name.data,
            'company_address': form.company_address.data,
            'company_site': form.company_site.data,
            'company_tel': form.company_tel.data,
            'company_fax': form.company_fax.data,
            'company_email': form.company_email.data,
            'company_type': form.company_type.data,
            'owner_uid': form.owner_uid.data,
            'create_time': current_time,
            'update_time': current_time,
        }
        result = add_supplier(supplier_data)
        # 创建操作成功
        if result:
            flash(_('Add Success'), 'success')
            return redirect(request.args.get('next') or url_for('supplier.edit', supplier_id=result))
        # 创建操作失败
        else:
            flash(_('Add Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                **document_info
            )


@bp_supplier.route('/<int:supplier_id>/edit.html', methods=['GET', 'POST'])
@login_required
def edit(supplier_id):
    """
    渠道编辑
    """
    # 检查编辑权限
    # supplier_item_edit_permission = SupplierItemEditPermission(supplier_id)
    # if not supplier_item_edit_permission.can():
    #     abort(403)

    supplier_info = get_supplier_row_by_id(supplier_id)
    # 检查资源是否存在
    if not supplier_info:
        abort(404)
    # 检查资源是否删除
    if supplier_info.status_delete == STATUS_DEL_OK:
        abort(410)

    template_name = 'supplier/edit.html'

    # 加载编辑表单
    form = SupplierEditForm(request.form)

    form.company_type.choices = TYPE_COMPANY_CHOICES
    form.owner_uid.choices = get_user_choices()

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('supplier edit')

    # 进入编辑页面
    if request.method == 'GET':
        # 表单赋值
        form.id.data = supplier_info.id
        form.company_name.data = supplier_info.company_name
        form.company_address.data = supplier_info.company_address
        form.company_site.data = supplier_info.company_site
        form.company_tel.data = supplier_info.company_tel
        form.company_fax.data = supplier_info.company_fax
        form.company_email.data = supplier_info.company_email
        form.company_type.data = supplier_info.company_type
        form.owner_uid.data = supplier_info.owner_uid
        form.create_time.data = supplier_info.create_time
        form.update_time.data = supplier_info.update_time
        # 渲染页面
        return render_template(
            template_name,
            supplier_id=supplier_id,
            form=form,
            **document_info
        )

    # 处理编辑请求
    if request.method == 'POST':
        # 表单校验失败
        if supplier_id != form.id.data or not form.validate_on_submit():
            flash(_('Edit Failure'), 'danger')
            # flash(form.errors, 'danger')
            return render_template(
                template_name,
                supplier_id=supplier_id,
                form=form,
                **document_info
            )
        # 表单校验成功
        current_time = datetime.utcnow()
        supplier_data = {
            'company_name': form.company_name.data,
            'company_address': form.company_address.data,
            'company_site': form.company_site.data,
            'company_tel': form.company_tel.data,
            'company_fax': form.company_fax.data,
            'company_email': form.company_email.data,
            'company_type': form.company_type.data,
            'owner_uid': form.owner_uid.data,
            'update_time': current_time,
        }
        result = edit_supplier(supplier_id, supplier_data)
        # 编辑操作成功
        if result:
            flash(_('Edit Success'), 'success')
            return redirect(request.args.get('next') or url_for('supplier.lists'))
        # 编辑操作失败
        else:
            flash(_('Edit Failure'), 'danger')
            return render_template(
                template_name,
                supplier_id=supplier_id,
                form=form,
                **document_info
            )


@bp_supplier.route('/ajax/del', methods=['GET', 'POST'])
@login_required
def ajax_delete():
    """
    渠道删除
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
    supplier_id = request.args.get('supplier_id', 0, type=int)
    if not supplier_id:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查删除权限
    supplier_item_del_permission = SupplierItemDelPermission(supplier_id)
    if not supplier_item_del_permission.can():
        ext_msg = _('Permission Denied')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    supplier_info = get_supplier_row_by_id(supplier_id)
    # 检查资源是否存在
    if not supplier_info:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)
    # 检查资源是否删除
    if supplier_info.status_delete == STATUS_DEL_OK:
        ext_msg = _('Already deleted')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)
    # 检查是否正在使用
    # 报价、订单、敏感型号
    if count_quotation(**{'cid': supplier_id, 'status_delete': STATUS_DEL_NO}):
        ext_msg = _('Currently In Use')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)
    if count_production_sensitive(**{'cid': supplier_id, 'status_delete': STATUS_DEL_NO}):
        ext_msg = _('Currently In Use')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    current_time = datetime.utcnow()
    supplier_data = {
        'status_delete': STATUS_DEL_OK,
        'delete_time': current_time,
        'update_time': current_time,
    }
    result = edit_supplier(supplier_id, supplier_data)
    if result:

        # 发送删除信号
        signal_data = {
            'supplier_id': supplier_id,
            'status_delete': STATUS_DEL_OK,
            'current_time': current_time,
        }
        signal_supplier_status_delete.send(app, **signal_data)

        ajax_success_msg['msg'] = _('Del Success')
        return jsonify(ajax_success_msg)
    else:
        ajax_failure_msg['msg'] = _('Del Failure')
        return jsonify(ajax_failure_msg)


@bp_supplier.route('/ajax/stats', methods=['GET', 'POST'])
@login_required
def ajax_stats():
    """
    获取渠道统计
    :return:
    """
    time_based = request.args.get('time_based', 'hour')
    result_supplier_middleman = supplier_middleman_stats(time_based)
    result_supplier_end_user = supplier_end_user_stats(time_based)

    line_chart_data = {
        'labels': [label for label, _ in result_supplier_middleman],
        'datasets': [
            {
                'label': '同行',
                'backgroundColor': 'rgba(220,220,220,0.5)',
                'borderColor': 'rgba(220,220,220,1)',
                'pointBackgroundColor': 'rgba(220,220,220,1)',
                'pointBorderColor': '#fff',
                'pointBorderWidth': 2,
                'data': [data for _, data in result_supplier_middleman]
            },
            {
                'label': '终端',
                'backgroundColor': 'rgba(151,187,205,0.5)',
                'borderColor': 'rgba(151,187,205,1)',
                'pointBackgroundColor': 'rgba(151,187,205,1)',
                'pointBorderColor': '#fff',
                'pointBorderWidth': 2,
                'data': [data for _, data in result_supplier_end_user]
            }
        ]
    }
    return json.dumps(line_chart_data, default=json_default)


@bp_supplier.route('/stats.html')
@login_required
@permission_supplier_section_stats.require(http_exception=403)
def stats():
    """
    渠道统计
    :return:
    """
    # 统计数据
    time_based = request.args.get('time_based', 'hour')
    if time_based not in ['hour', 'date', 'month']:
        abort(404)
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('supplier stats')
    # 渲染模板
    return render_template(
        'supplier/stats.html',
        time_based=time_based,
        **document_info
    )


@bp_supplier.route('/<int:supplier_id>/stats.html')
@login_required
@permission_supplier_section_stats.require(http_exception=403)
def stats_item(supplier_id):
    """
    渠道统计明细
    :param supplier_id:
    :return:
    """
    supplier_info = get_supplier_row_by_id(supplier_id)
    # 检查资源是否存在
    if not supplier_info:
        abort(404)
    # 检查资源是否删除
    if supplier_info.status_delete == STATUS_DEL_OK:
        abort(410)

    # 统计数据
    supplier_stats_item_info = get_supplier_row_by_id(supplier_id)
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('supplier stats item')
    # 渲染模板
    return render_template(
        'supplier/stats_item.html',
        supplier_stats_item_info=supplier_stats_item_info,
        **document_info
    )
