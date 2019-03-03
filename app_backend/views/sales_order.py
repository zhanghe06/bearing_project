#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: sales_order.py
@time: 2018-07-16 18:01
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
    g,
)
from flask_babel import gettext as _
from flask_login import login_required, current_user
from flask_weasyprint import render_pdf, HTML, CSS
from app_backend import (
    app,
    excel,
)

# 定义蓝图
from app_backend.api.sales_order import get_sales_order_rows, edit_sales_order, get_sales_order_pagination, \
    add_sales_order, get_sales_order_row_by_id
from app_backend.api.sales_order_items import add_sales_order_items, get_sales_order_items_rows, edit_sales_order_items, delete_sales_order_items
from app_backend.api.sales_order import get_sales_order_user_list_choices
from app_backend.api.supplier_contact import get_supplier_contact_row_by_id
from app_backend.api.user import get_user_choices, get_user_row_by_id
from app_backend.api.supplier import get_supplier_row_by_id
from app_backend.forms.sales_order import SalesOrderSearchForm, SalesOrderAddForm, SalesOrderEditForm, SalesOrderItemEditForm
from app_backend.models.bearing_project import SalesOrder
from app_backend.permissions import permission_sales_orders_section_export, SalesOrdersItemDelPermission
from app_backend.signals.sales_orders import signal_sales_orders_status_delete
from app_common.maps.default import default_search_choice_option_int
from app_common.maps.status_delete import STATUS_DEL_NO, STATUS_DEL_OK

from app_common.tools.date_time import time_utc_to_local, time_local_to_utc

# 定义蓝图
bp_sales_order = Blueprint('sales_order', __name__, url_prefix='/sales/order')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


@bp_sales_order.route('/lists.html', methods=['GET', 'POST'])
@login_required
def lists():
    """
    采购订单列表
    :return:
    """
    template_name = 'sales/order/lists.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('sales order lists')

    # 搜索条件
    form = SalesOrderSearchForm(request.form)
    form.uid.choices = get_sales_order_user_list_choices()
    # app.logger.info('')

    search_condition = [
        SalesOrder.status_delete == STATUS_DEL_NO,
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
                search_condition.append(SalesOrder.uid == form.uid.data)
            if form.customer_cid.data and form.customer_company_name.data:
                search_condition.append(SalesOrder.cid == form.customer_cid.data)
            if form.start_create_time.data:
                search_condition.append(SalesOrder.create_time >= form.start_create_time.data)
            if form.end_create_time.data:
                search_condition.append(SalesOrder.create_time <= form.end_create_time.data)
        # 处理导出
        if form.op.data == 1:
            # 检查导出权限
            if not permission_sales_orders_section_export.can():
                abort(403)
            column_names = SalesOrder.__table__.columns.keys()
            query_sets = get_sales_order_rows(*search_condition)

            return excel.make_response_from_query_sets(
                query_sets=query_sets,
                column_names=column_names,
                file_type='csv',
                file_name='%s.csv' % _('sales order lists')
            )
        # 批量删除
        if form.op.data == 2:
            order_ids = request.form.getlist('order_id')
            # 检查删除权限
            permitted = True
            for order_id in order_ids:
                sales_orders_item_del_permission = SalesOrdersItemDelPermission(order_id)
                if not sales_orders_item_del_permission.can():
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
                    result = edit_sales_order(order_id, quotation_data)
                    if result:
                        # 发送删除信号
                        signal_data = {
                            'order_id': order_id,
                            'status_delete': STATUS_DEL_OK,
                            'current_time': current_time,
                        }
                        signal_sales_orders_status_delete.send(app, **signal_data)
                    result_total = result_total and result
                if result_total:
                    flash(_('Del Success'), 'success')
                else:
                    flash(_('Del Failure'), 'danger')
    # 翻页数据
    pagination = get_sales_order_pagination(form.page.data, PER_PAGE_BACKEND, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )


@bp_sales_order.route('/add.html', methods=['GET', 'POST'])
@login_required
def add():
    template_name = 'sales/order/add.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('sales order add')

    # 加载创建表单
    form = SalesOrderAddForm(request.form)
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
            if form.sales_order_items.max_entries and len(
                    form.sales_order_items.entries) >= form.sales_order_items.max_entries:
                flash('最多创建%s条记录' % form.sales_order_items.max_entries, 'danger')
            else:
                form.sales_order_items.append_entry()

            return render_template(
                template_name,
                form=form,
                **document_info
            )
        # 表单删除一行
        if form.data_line_del.data is not None:
            if form.sales_order_items.min_entries and len(
                    form.sales_order_items.entries) <= form.sales_order_items.min_entries:
                flash('最少保留%s条记录' % form.sales_order_items.min_entries, 'danger')
            else:
                data_line_index = form.data_line_del.data
                form.sales_order_items.entries.pop(data_line_index)

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

        # 创建订单
        current_time = datetime.utcnow()
        sales_order_data = {
            'uid': form.uid.data,
            'customer_cid': form.customer_cid.data,
            'customer_contact_id': form.customer_contact_id.data,
            'type_tax': form.type_tax.data,
            'delivery_way': form.delivery_way.data,
            'create_time': current_time,
            'update_time': current_time,
        }
        sales_order_id = add_sales_order(sales_order_data)

        amount_sales_order = 0
        for sales_order_item in form.sales_order_items.entries:
            current_time = datetime.utcnow()
            sales_order_item_data = {
                'sales_order_id': sales_order_id,
                'uid': form.uid.data,
                'customer_cid': form.customer_cid.data,
                'customer_company_name': get_supplier_row_by_id(form.customer_cid.data).company_name,
                'custom_production_brand': sales_order_item.form.custom_production_brand.data,
                'custom_production_model': sales_order_item.form.custom_production_model.data,
                'production_id': sales_order_item.form.production_id.data,
                'production_brand': sales_order_item.form.production_brand.data,
                'production_model': sales_order_item.form.production_model.data,
                'production_sku': sales_order_item.form.production_sku.data,
                'delivery_time': sales_order_item.form.delivery_time.data,
                'quantity': sales_order_item.form.quantity.data,
                'unit_price': sales_order_item.form.unit_price.data,
                'note': sales_order_item.form.note.data,
                'type_tax': form.type_tax.data,
                'create_time': current_time,
                'update_time': current_time,
            }

            # 新增
            add_sales_order_items(sales_order_item_data)
            amount_sales_order += (sales_order_item_data['quantity'] or 0) * (sales_order_item_data['unit_price'] or 0)

        # 更新报价
        sales_order_data = {
            'amount_production': amount_sales_order,
            'amount_order': amount_sales_order,
            'update_time': current_time,
        }
        result = edit_sales_order(sales_order_id, sales_order_data)

        # todo 事务

        # 明细保存
        # 总表保存

        # 创建操作成功
        if result:
            flash(_('Add Success'), 'success')
            return redirect(request.args.get('next') or url_for('sales_order.lists'))
        # 创建操作失败
        else:
            flash(_('Add Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                **document_info
            )


@bp_sales_order.route('/<int:sales_order_id>/edit.html', methods=['GET', 'POST'])
@login_required
def edit(sales_order_id):
    """
    采购订单编辑
    """
    # 检查编辑权限
    # enquiry_item_edit_permission = EnquiryItemEditPermission(enquiry_id)
    # if not enquiry_item_edit_permission.can():
    #     abort(403)

    sales_order_info = get_sales_order_row_by_id(sales_order_id)
    # 检查资源是否存在
    if not sales_order_info:
        abort(404)
    # 检查资源是否删除
    if sales_order_info.status_delete == STATUS_DEL_OK:
        abort(410)

    template_name = 'sales/order/edit.html'

    # 加载编辑表单
    form = SalesOrderEditForm(request.form)
    form.uid.choices = get_user_choices()
    # form.status_order.choices = STATUS_ORDER_CHOICES

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('sales order edit')

    # 进入编辑页面
    if request.method == 'GET':
        # 获取明细
        sales_order_items = get_sales_order_items_rows(sales_order_id=sales_order_id)
        # 表单赋值
        form.uid.data = sales_order_info.uid
        form.customer_cid.data = sales_order_info.supplier_cid
        form.customer_contact_id.data = sales_order_info.supplier_contact_id
        form.type_tax.data = sales_order_info.type_tax
        form.amount_order.data = sales_order_info.amount_order
        # form.sales_order_items = sales_order_items
        while len(form.sales_order_items) > 0:
            form.sales_order_items.pop_entry()
        for sales_order_item in sales_order_items:
            sales_order_item_form = SalesOrderItemEditForm()
            sales_order_item_form.id = sales_order_item.id
            sales_order_item_form.sales_order_id = sales_order_item.sales_order_id
            sales_order_item_form.uid = sales_order_item.uid
            # sales_order_item_form.supplier_cid = sales_order_item.supplier_cid
            # sales_order_item_form.supplier_company_name = sales_order_item.supplier_company_name
            sales_order_item_form.custom_production_brand = sales_order_item.custom_production_brand
            sales_order_item_form.custom_production_model = sales_order_item.custom_production_model
            sales_order_item_form.production_id = sales_order_item.production_id
            sales_order_item_form.production_brand = sales_order_item.production_brand
            sales_order_item_form.production_model = sales_order_item.production_model
            sales_order_item_form.production_sku = sales_order_item.production_sku
            sales_order_item_form.delivery_time = sales_order_item.delivery_time
            sales_order_item_form.quantity = sales_order_item.quantity
            sales_order_item_form.unit_price = sales_order_item.unit_price
            sales_order_item_form.note = sales_order_item.note
            sales_order_item_form.type_tax = sales_order_item.type_tax
            form.sales_order_items.append_entry(sales_order_item_form)

        # 渲染页面
        return render_template(
            template_name,
            sales_order_id=sales_order_id,
            form=form,
            **document_info
        )

    # 处理编辑请求
    if request.method == 'POST':
        # 增删数据行不需要校验表单

        # 表单新增空行
        if form.data_line_add.data is not None:
            if form.sales_order_items.max_entries and len(
                    form.sales_order_items.entries) >= form.sales_order_items.max_entries:
                flash('最多创建%s条记录' % form.sales_order_items.max_entries, 'danger')
            else:
                form.sales_order_items.append_entry()

            return render_template(
                template_name,
                sales_order_id=sales_order_id,
                form=form,
                **document_info
            )
        # 表单删除一行
        if form.data_line_del.data is not None:
            if form.sales_order_items.min_entries and len(
                    form.sales_order_items.entries) <= form.sales_order_items.min_entries:
                flash('最少保留%s条记录' % form.sales_order_items.min_entries, 'danger')
            else:
                data_line_index = form.data_line_del.data
                form.sales_order_items.entries.pop(data_line_index)

            return render_template(
                template_name,
                sales_order_id=sales_order_id,
                form=form,
                **document_info
            )

        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Edit Failure'), 'danger')
            # flash(form.errors, 'danger')
            # flash(form.sales_order_items.errors, 'danger')
            return render_template(
                template_name,
                sales_order_id=sales_order_id,
                form=form,
                **document_info
            )
        # 表单校验成功

        # 获取明细
        sales_order_items = get_sales_order_items_rows(sales_order_id=sales_order_id)
        sales_order_items_ids = [item.id for item in sales_order_items]

        # 数据新增、数据删除、数据修改

        sales_order_items_ids_new = []
        amount_sales_order = 0
        for sales_order_item in form.sales_order_items.entries:
            # 错误
            if sales_order_item.form.id.data and sales_order_item.form.id.data not in sales_order_items_ids:
                continue

            sales_order_item_data = {
                'sales_order_id': sales_order_id,
                'uid': form.uid.data,
                'customer_cid': form.customer_cid.data,
                'customer_company_name': get_supplier_row_by_id(form.customer_cid.data).company_name,
                'custom_production_brand': sales_order_item.form.custom_production_brand.data,
                'custom_production_model': sales_order_item.form.custom_production_model.data,
                'production_id': sales_order_item.form.production_id.data,
                'production_brand': sales_order_item.form.production_brand.data,
                'production_model': sales_order_item.form.production_model.data,
                'production_sku': sales_order_item.form.production_sku.data,
                'delivery_time': sales_order_item.form.delivery_time.data,
                'quantity': sales_order_item.form.quantity.data,
                'unit_price': sales_order_item.form.unit_price.data,
                'note': sales_order_item.form.note.data,
                'type_tax': form.type_tax.data,
            }

            if not sales_order_item.form.id.data:
                # 新增
                add_sales_order_items(sales_order_item_data)
                amount_sales_order += sales_order_item_data['quantity'] * sales_order_item_data['unit_price']
            else:
                # 修改
                edit_sales_order_items(sales_order_item.form.id.data, sales_order_item_data)
                amount_sales_order += sales_order_item_data['quantity'] * sales_order_item_data['unit_price']
                sales_order_items_ids_new.append(sales_order_item.form.id.data)
        # 删除
        sales_order_items_ids_del = list(set(sales_order_items_ids) - set(sales_order_items_ids_new))
        for sales_order_items_id in sales_order_items_ids_del:
            delete_sales_order_items(sales_order_items_id)

        # 更新采购订单
        current_time = datetime.utcnow()
        sales_order_data = {
            'uid': form.uid.data,
            'customer_cid': form.customer_cid.data,
            'customer_contact_id': form.customer_contact_id.data,
            'type_tax': form.type_tax.data,
            'amount_production': amount_sales_order,
            'amount_order': amount_sales_order,
            'update_time': current_time,
        }
        result = edit_sales_order(sales_order_id, sales_order_data)

        # 编辑操作成功
        if result:
            flash(_('Edit Success'), 'success')
            return redirect(request.args.get('next') or url_for('sales_order.lists'))
        # 编辑操作失败
        else:
            flash(_('Edit Failure'), 'danger')
            return render_template(
                template_name,
                sales_order_id=sales_order_id,
                form=form,
                **document_info
            )


@bp_sales_order.route('/<int:sales_order_id>/preview.html')
@login_required
def preview(sales_order_id):
    """
    打印预览
    :param sales_order_id:
    :return:
    """
    sales_order_info = get_sales_order_row_by_id(sales_order_id)
    # 检查资源是否存在
    if not sales_order_info:
        abort(404)
    # 检查资源是否删除
    if sales_order_info.status_delete == STATUS_DEL_OK:
        abort(410)

    sales_order_print_date = time_utc_to_local(sales_order_info.update_time).strftime('%Y-%m-%d')
    sales_order_code = '%s%s' % (g.ENQUIRIES_PREFIX, time_utc_to_local(sales_order_info.create_time).strftime('%y%m%d%H%M%S'))

    # 获取渠道公司信息
    supplier_info = get_supplier_row_by_id(sales_order_info.supplier_cid)

    # 获取渠道联系方式
    supplier_contact_info = get_supplier_contact_row_by_id(sales_order_info.supplier_contact_id)

    # 获取询价人员信息
    user_info = get_user_row_by_id(sales_order_info.uid)

    sales_order_items = get_sales_order_items_rows(sales_order_id=sales_order_id)

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('sales order preview')

    template_name = 'sales/order/preview.html'

    return render_template(
        template_name,
        sales_order_id=sales_order_id,
        sales_order_info=sales_order_info,
        supplier_info=supplier_info,
        supplier_contact_info=supplier_contact_info,
        user_info=user_info,
        sales_order_items=sales_order_items,
        sales_order_print_date=sales_order_print_date,
        sales_order_code=sales_order_code,
        **document_info
    )


@bp_sales_order.route('/<int:sales_order_id>.pdf')
@login_required
def pdf(sales_order_id):
    """
    文件下载
    :param sales_order_id:
    :return:
    """
    sales_order_info = get_sales_order_row_by_id(sales_order_id)
    # 检查资源是否存在
    if not sales_order_info:
        abort(404)
    # 检查资源是否删除
    if sales_order_info.status_delete == STATUS_DEL_OK:
        abort(410)

    sales_order_print_date = time_utc_to_local(sales_order_info.update_time).strftime('%Y-%m-%d')
    sales_order_code = '%s%s' % (g.ENQUIRIES_PREFIX, time_utc_to_local(sales_order_info.create_time).strftime('%y%m%d%H%M%S'))

    # 获取客户公司信息
    supplier_info = get_supplier_row_by_id(sales_order_info.supplier_cid)

    # 获取客户联系方式
    supplier_contact_info = get_supplier_contact_row_by_id(sales_order_info.supplier_contact_id)

    # 获取询价人员信息
    user_info = get_user_row_by_id(sales_order_info.uid)

    sales_order_items = get_sales_order_items_rows(sales_order_id=sales_order_id)

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('sales order pdf')

    template_name = 'sales/order/pdf.html'

    html = render_template(
        template_name,
        sales_order_id=sales_order_id,
        sales_order_info=sales_order_info,
        supplier_info=supplier_info,
        supplier_contact_info=supplier_contact_info,
        user_info=user_info,
        sales_order_items=sales_order_items,
        sales_order_print_date=sales_order_print_date,
        sales_order_code=sales_order_code,
        **document_info
    )
    # return html
    return render_pdf(
        html=HTML(string=html),
        stylesheets=[CSS(string='@page {size:A4; margin:35px;}')],
        download_filename='采购订单.pdf'.encode('utf-8')
    )


@bp_sales_order.route('/ajax/del', methods=['GET', 'POST'])
@login_required
def ajax_delete():
    """
    采购订单删除
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
    sales_order_id = request.args.get('sales_order_id', 0, type=int)
    if not sales_order_id:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查删除权限
    sales_orders_item_del_permission = SalesOrdersItemDelPermission(sales_order_id)
    if not sales_orders_item_del_permission.can():
        ext_msg = _('Permission Denied')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    enquiry_info = get_sales_order_row_by_id(sales_order_id)
    # 检查资源是否存在
    if not enquiry_info:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)
    # 检查资源是否删除
    if enquiry_info.status_delete == STATUS_DEL_OK:
        ext_msg = _('Already deleted')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_success_msg)

    current_time = datetime.utcnow()
    enquiry_data = {
        'status_delete': STATUS_DEL_OK,
        'delete_time': current_time,
        'update_time': current_time,
    }
    result = edit_sales_order(sales_order_id, enquiry_data)
    if result:
        # 发送删除信号
        signal_data = {
            'sales_order_id': sales_order_id,
            'status_delete': STATUS_DEL_OK,
            'current_time': current_time,
        }
        signal_sales_orders_status_delete.send(app, **signal_data)

        ajax_success_msg['msg'] = _('Del Success')
        return jsonify(ajax_success_msg)
    else:
        ajax_failure_msg['msg'] = _('Del Failure')
        return jsonify(ajax_failure_msg)


@bp_sales_order.route('/stats.html', methods=['GET', 'POST'])
@login_required
def stats():
    return jsonify({})
