#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: purchase.py
@time: 2018-08-31 15:41
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
from flask_login import login_required, current_user

from app_backend import (
    app,
    excel,
)
from app_backend.api.supplier import get_supplier_row_by_id
from app_backend.signals.purchase import signal_purchase_status_delete

from app_common.maps.default import default_search_choices_int, default_search_choice_option_int
from app_backend.api.purchase import add_purchase, get_purchase_user_list_choices, get_purchase_rows, \
    get_purchase_pagination, edit_purchase, get_purchase_row_by_id
from app_backend.api.purchase_items import add_purchase_items, edit_purchase_items
from app_backend.api.user import get_user_choices
from app_backend.forms.purchase import PurchaseSearchForm
from app_backend.forms.purchase import PurchaseAddForm
from app_common.maps.status_order import STATUS_ORDER_CHOICES
from app_common.maps.status_delete import (
    STATUS_DEL_OK,
    STATUS_DEL_NO)

from app_backend.models.bearing_project import Purchase
from app_backend.permissions import (
    permission_purchase_section_add,
    permission_purchase_section_search,
    permission_purchase_section_export,
    permission_purchase_section_stats,
    PurchaseItemGetPermission,
    PurchaseItemEditPermission,
    PurchaseItemDelPermission,
)

# 定义蓝图
bp_purchase = Blueprint('purchase', __name__, url_prefix='/purchase')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


@bp_purchase.route('/lists.html', methods=['GET', 'POST'])
@login_required
def lists():
    template_name = 'purchase/lists.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('purchase lists')

    # 搜索条件
    form = PurchaseSearchForm(request.form)
    form.uid.choices = get_purchase_user_list_choices()
    # app.logger.info('')

    search_condition = [
        Purchase.status_delete == STATUS_DEL_NO,
    ]
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Search Failure'), 'danger')
            # 单独处理csrf_token
            if hasattr(form, 'csrf_token') and getattr(form, 'csrf_token').errors:
                map(lambda x: flash(x, 'danger'), form.csrf_token.errors)
        else:
            if form.uid.data != default_search_choice_option_int:
                search_condition.append(Purchase.uid == form.uid.data)
            if form.supplier_cid.data and form.supplier_company_name.data:
                search_condition.append(Purchase.cid == form.supplier_cid.data)
            if form.start_create_time.data:
                search_condition.append(Purchase.create_time >= form.start_create_time.data)
            if form.end_create_time.data:
                search_condition.append(Purchase.create_time <= form.end_create_time.data)
        # 处理导出
        if form.op.data == 1:
            # 检查导出权限
            if not permission_purchase_section_export.can():
                abort(403)
            column_names = Purchase.__table__.columns.keys()
            query_sets = get_purchase_rows(*search_condition)

            return excel.make_response_from_query_sets(
                query_sets=query_sets,
                column_names=column_names,
                file_type='csv',
                file_name='%s.csv' % _('purchase lists')
            )
        # 批量删除
        if form.op.data == 2:
            order_ids = request.form.getlist('order_id')
            # 检查删除权限
            permitted = True
            for order_id in order_ids:
                purchase_item_del_permission = PurchaseItemDelPermission(order_id)
                if not purchase_item_del_permission.can():
                    ext_msg = _('Permission Denied')
                    flash(_('Del Failure, %(ext_msg)s', ext_msg=ext_msg), 'danger')
                    permitted = False
                    break
            if permitted:
                result_total = True
                for order_id in order_ids:
                    current_time = datetime.utcnow()
                    quotation_data = {
                        'status_delete': STATUS_DEL_OK,
                        'delete_time': current_time,
                        'update_time': current_time,
                    }
                    result = edit_purchase(order_id, quotation_data)
                    if result:
                        # 发送删除信号
                        signal_data = {
                            'order_id': order_id,
                            'status_delete': STATUS_DEL_OK,
                            'current_time': current_time,
                        }
                        signal_purchase_status_delete.send(app, **signal_data)
                    result_total = result_total and result
                if result_total:
                    flash(_('Del Success'), 'success')
                else:
                    flash(_('Del Failure'), 'danger')
    # 翻页数据
    pagination = get_purchase_pagination(form.page.data, PER_PAGE_BACKEND, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )


@bp_purchase.route('/add.html', methods=['GET', 'POST'])
@login_required
def add():
    """
    采购进货
    :return:
    """
    # return jsonify({})
    template_name = 'purchase/add.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('purchase add')

    # 加载创建表单
    form = PurchaseAddForm(request.form)
    form.uid.choices = get_user_choices()
    form.uid.data = current_user.id
    # form.contact_id.choices = default_choices_int

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

        # 表单新增空行
        if form.data_line_add.data is not None:
            if form.purchase_items.max_entries and len(
                    form.purchase_items.entries) >= form.purchase_items.max_entries:
                flash('最多创建%s条记录' % form.purchase_items.max_entries, 'danger')
            else:
                form.purchase_items.append_entry()

            return render_template(
                template_name,
                form=form,
                **document_info
            )
        # 表单删除一行
        if form.data_line_del.data is not None:
            if form.purchase_items.min_entries and len(
                    form.purchase_items.entries) <= form.purchase_items.min_entries:
                flash('最少保留%s条记录' % form.purchase_items.min_entries, 'danger')
            else:
                data_line_index = form.data_line_del.data
                form.purchase_items.entries.pop(data_line_index)

            return render_template(
                template_name,
                form=form,
                **document_info
            )

        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Add Failure'), 'danger')
            # flash(form.errors, 'danger')
            return render_template(
                template_name,
                form=form,
                **document_info
            )

        # 表单校验成功

        # 创建采购进货
        current_time = datetime.utcnow()
        purchase_data = {
            'uid': form.uid.data,
            'supplier_cid': form.supplier_cid.data,
            'supplier_contact_id': form.supplier_contact_id.data,
            # 'type_purchase': form.type_purchase.data,
            'create_time': current_time,
            'update_time': current_time,
        }
        purchase_id = add_purchase(purchase_data)

        amount_purchase = 0
        for quotation_item in form.purchase_items.entries:
            current_time = datetime.utcnow()
            purchase_item_data = {
                'purchase_id': purchase_id,
                'uid': form.uid.data,
                'supplier_cid': form.supplier_cid.data,
                'supplier_company_name': get_supplier_row_by_id(form.supplier_cid.data).company_name,
                'production_id': quotation_item.form.production_id.data,
                'production_brand': quotation_item.form.production_brand.data,
                'production_model': quotation_item.form.production_model.data,
                'production_sku': quotation_item.form.production_sku.data,
                'note': quotation_item.form.note.data,
                'quantity': quotation_item.form.quantity.data,
                'unit_price': quotation_item.form.unit_price.data,
                'create_time': current_time,
                'update_time': current_time,
            }

            # 新增
            add_purchase_items(purchase_item_data)
            amount_purchase += (purchase_item_data['quantity'] or 0) * (purchase_item_data['unit_price'] or 0)

        # 更新报价
        purchase_data = {
            'amount_production': amount_purchase,
            'amount_purchase': amount_purchase,
            'update_time': current_time,
        }
        result = edit_purchase(purchase_id, purchase_data)

        # todo 事务

        # 明细保存
        # 总表保存

        # 创建操作成功
        if result:
            flash(_('Add Success'), 'success')
            return redirect(request.args.get('next') or url_for('purchase.lists'))
        # 创建操作失败
        else:
            flash(_('Add Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                **document_info
            )


@bp_purchase.route('/ajax/del', methods=['GET', 'POST'])
@login_required
def ajax_delete():
    """
    采购进货删除
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
    purchase_id = request.args.get('purchase_id', 0, type=int)
    if not purchase_id:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查删除权限
    purchase_item_del_permission = PurchaseItemDelPermission(purchase_id)
    if not purchase_item_del_permission.can():
        ext_msg = _('Permission Denied')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    purchase_info = get_purchase_row_by_id(purchase_id)
    # 检查资源是否存在
    if not purchase_info:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)
    # 检查资源是否删除
    if purchase_info.status_delete == STATUS_DEL_OK:
        ext_msg = _('Already deleted')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_success_msg)

    current_time = datetime.utcnow()
    purchase_data = {
        'status_delete': STATUS_DEL_OK,
        'delete_time': current_time,
        'update_time': current_time,
    }
    result = edit_purchase(purchase_id, purchase_data)
    if result:
        # 发送删除信号
        signal_data = {
            'purchase_id': purchase_id,
            'status_delete': STATUS_DEL_OK,
            'current_time': current_time,
        }
        signal_purchase_status_delete.send(app, **signal_data)

        ajax_success_msg['msg'] = _('Del Success')
        return jsonify(ajax_success_msg)
    else:
        ajax_failure_msg['msg'] = _('Del Failure')
        return jsonify(ajax_failure_msg)
