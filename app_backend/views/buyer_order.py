#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: buyer_order.py
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
from werkzeug import exceptions

# 定义蓝图
from app_backend.api.buyer_order import get_buyer_order_rows, edit_buyer_order, get_buyer_order_pagination, \
    add_buyer_order, get_buyer_order_row_by_id
from app_backend.api.buyer_order_items import add_buyer_order_items, get_buyer_order_items_rows, edit_buyer_order_items, delete_buyer_order_items
from app_backend.api.buyer_order import get_buyer_order_user_list_choices
from app_backend.api.supplier_contact import get_supplier_contact_row_by_id
from app_backend.api.user import get_user_choices, get_user_row_by_id
from app_backend.api.supplier import get_supplier_row_by_id
from app_backend.forms.buyer_order import BuyerOrderSearchForm, BuyerOrderAddForm, BuyerOrderEditForm, BuyerOrderItemsEditForm
from app_backend.models.bearing_project import BuyerOrder
from app_backend.permissions import permission_buyer_orders_section_export, BuyerOrderItemDelPermission
from app_backend.signals.buyer_orders import signal_buyer_orders_status_delete
from app_common.maps.default import default_search_choice_option_int
from app_common.maps.status_delete import STATUS_DEL_NO, STATUS_DEL_OK
from app_common.maps.status_audit import STATUS_AUDIT_NO, STATUS_AUDIT_OK

from app_common.tools.date_time import time_utc_to_local, time_local_to_utc

bp_buyer_order = Blueprint('buyer_order', __name__, url_prefix='/buyer/order')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


@bp_buyer_order.route('/lists.html', methods=['GET', 'POST'])
@login_required
def lists():
    """
    采购订单列表
    :return:
    """
    template_name = 'buyer/order/lists.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('buyer order lists')

    # 搜索条件
    form = BuyerOrderSearchForm(request.form)
    form.uid.choices = get_buyer_order_user_list_choices()
    # app.logger.info('')

    search_condition = [
        BuyerOrder.status_delete == STATUS_DEL_NO,
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
                search_condition.append(BuyerOrder.uid == form.uid.data)
            if form.supplier_cid.data and form.supplier_company_name.data:
                search_condition.append(BuyerOrder.cid == form.supplier_cid.data)
            if form.start_create_time.data:
                search_condition.append(BuyerOrder.create_time >= form.start_create_time.data)
            if form.end_create_time.data:
                search_condition.append(BuyerOrder.create_time <= form.end_create_time.data)
        # 处理导出
        if form.op.data == 1:
            # 检查导出权限
            if not permission_buyer_orders_section_export.can():
                abort(403)
            column_names = BuyerOrder.__table__.columns.keys()
            query_sets = get_buyer_order_rows(*search_condition)

            return excel.make_response_from_query_sets(
                query_sets=query_sets,
                column_names=column_names,
                file_type='csv',
                file_name='%s.csv' % _('buyer order lists')
            )
        # 批量删除
        if form.op.data == 2:
            order_ids = request.form.getlist('order_id')
            # 检查删除权限
            permitted = True
            for order_id in order_ids:
                buyer_orders_item_del_permission = BuyerOrderItemDelPermission(order_id)
                if not buyer_orders_item_del_permission.can():
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
                    result = edit_buyer_order(order_id, quotation_data)
                    if result:
                        # 发送删除信号
                        signal_data = {
                            'order_id': order_id,
                            'status_delete': STATUS_DEL_OK,
                            'current_time': current_time,
                        }
                        signal_buyer_orders_status_delete.send(app, **signal_data)
                    result_total = result_total and result
                if result_total:
                    flash(_('Del Success'), 'success')
                else:
                    flash(_('Del Failure'), 'danger')
    # 翻页数据
    pagination = get_buyer_order_pagination(form.page.data, PER_PAGE_BACKEND, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )


@bp_buyer_order.route('/add.html', methods=['GET', 'POST'])
@login_required
def add():
    template_name = 'buyer/order/add.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('buyer order add')

    # 加载创建表单
    form = BuyerOrderAddForm(request.form)
    form.uid.choices = get_user_choices()
    form.uid.data = current_user.id
    # form.contact_id.choices = default_choices_int

    # 进入创建页面
    if request.method == 'GET':

        # 克隆单据
        from_type = request.args.get('from_type')
        from_id = request.args.get('from_id', type=int)
        # 克隆单据 - 报价单
        if from_type == 'buyer_order' and from_id:
            buyer_order_id = from_id
            buyer_order_info = get_buyer_order_row_by_id(buyer_order_id)
            # 检查资源是否存在
            if not buyer_order_info:
                abort(404)
            # 检查资源是否删除
            if buyer_order_info.status_delete == STATUS_DEL_OK:
                abort(410)

            # 获取明细
            buyer_order_items = get_buyer_order_items_rows(buyer_order_id=buyer_order_id)
            # 表单赋值
            form.uid.data = buyer_order_info.uid
            form.supplier_cid.data = buyer_order_info.supplier_cid
            form.supplier_contact_id.data = buyer_order_info.supplier_contact_id
            form.type_tax.data = buyer_order_info.type_tax
            form.amount_order.data = buyer_order_info.amount_order
            while len(form.buyer_order_items) > 0:
                form.buyer_order_items.pop_entry()
            for buyer_order_item in buyer_order_items:
                buyer_order_item_form = BuyerOrderItemsEditForm()
                buyer_order_item_form.id = buyer_order_item.id
                buyer_order_item_form.buyer_order_id = buyer_order_item.buyer_order_id
                buyer_order_item_form.uid = buyer_order_item.uid
                # buyer_order_item_form.supplier_cid = buyer_order_item.supplier_cid
                # buyer_order_item_form.supplier_company_name = buyer_order_item.supplier_company_name
                buyer_order_item_form.custom_production_brand = buyer_order_item.custom_production_brand
                buyer_order_item_form.custom_production_model = buyer_order_item.custom_production_model
                buyer_order_item_form.production_id = buyer_order_item.production_id
                buyer_order_item_form.production_brand = buyer_order_item.production_brand
                buyer_order_item_form.production_model = buyer_order_item.production_model
                buyer_order_item_form.production_sku = buyer_order_item.production_sku
                buyer_order_item_form.delivery_time = buyer_order_item.delivery_time
                buyer_order_item_form.quantity = buyer_order_item.quantity
                buyer_order_item_form.unit_price = buyer_order_item.unit_price
                buyer_order_item_form.note = buyer_order_item.note
                buyer_order_item_form.type_tax = buyer_order_item.type_tax
                form.buyer_order_items.append_entry(buyer_order_item_form)

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
            if form.buyer_order_items.max_entries and len(
                    form.buyer_order_items.entries) >= form.buyer_order_items.max_entries:
                flash('最多创建%s条记录' % form.buyer_order_items.max_entries, 'danger')
            else:
                form.buyer_order_items.append_entry()

            return render_template(
                template_name,
                form=form,
                **document_info
            )
        # 表单删除一行
        if form.data_line_del.data is not None:
            if form.buyer_order_items.min_entries and len(
                    form.buyer_order_items.entries) <= form.buyer_order_items.min_entries:
                flash('最少保留%s条记录' % form.buyer_order_items.min_entries, 'danger')
            else:
                data_line_index = form.data_line_del.data
                form.buyer_order_items.entries.pop(data_line_index)

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
        buyer_order_data = {
            'uid': form.uid.data,
            'supplier_cid': form.supplier_cid.data,
            'supplier_contact_id': form.supplier_contact_id.data,
            'type_tax': form.type_tax.data,
            'delivery_way': form.delivery_way.data,
            'create_time': current_time,
            'update_time': current_time,
        }
        buyer_order_id = add_buyer_order(buyer_order_data)

        amount_buyer_order = 0
        for buyer_order_item in form.buyer_order_items.entries:
            current_time = datetime.utcnow()
            buyer_order_item_data = {
                'buyer_order_id': buyer_order_id,
                'uid': form.uid.data,
                'supplier_cid': form.supplier_cid.data,
                'supplier_company_name': get_supplier_row_by_id(form.supplier_cid.data).company_name,
                'custom_production_brand': buyer_order_item.form.custom_production_brand.data,
                'custom_production_model': buyer_order_item.form.custom_production_model.data,
                'production_id': buyer_order_item.form.production_id.data,
                'production_brand': buyer_order_item.form.production_brand.data,
                'production_model': buyer_order_item.form.production_model.data,
                'production_sku': buyer_order_item.form.production_sku.data,
                'delivery_time': buyer_order_item.form.delivery_time.data,
                'quantity': buyer_order_item.form.quantity.data,
                'unit_price': buyer_order_item.form.unit_price.data,
                'note': buyer_order_item.form.note.data,
                'type_tax': form.type_tax.data,
                'create_time': current_time,
                'update_time': current_time,
            }

            # 新增
            add_buyer_order_items(buyer_order_item_data)
            amount_buyer_order += (buyer_order_item_data['quantity'] or 0) * (buyer_order_item_data['unit_price'] or 0)

        # 更新报价
        buyer_order_data = {
            'amount_production': amount_buyer_order,
            'amount_order': amount_buyer_order,
            'update_time': current_time,
        }
        result = edit_buyer_order(buyer_order_id, buyer_order_data)

        # todo 事务

        # 明细保存
        # 总表保存

        # 创建操作成功
        if result:
            flash(_('Add Success'), 'success')
            return redirect(request.args.get('next') or url_for('buyer_order.lists'))
        # 创建操作失败
        else:
            flash(_('Add Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                **document_info
            )


@bp_buyer_order.route('/<int:buyer_order_id>/edit.html', methods=['GET', 'POST'])
@login_required
def edit(buyer_order_id):
    """
    采购订单编辑
    """
    # 检查编辑权限
    # enquiry_item_edit_permission = EnquiryItemEditPermission(enquiry_id)
    # if not enquiry_item_edit_permission.can():
    #     abort(403)

    buyer_order_info = get_buyer_order_row_by_id(buyer_order_id)
    # 检查资源是否存在
    if not buyer_order_info:
        abort(404)
    # 检查资源是否删除
    if buyer_order_info.status_delete == STATUS_DEL_OK:
        abort(410)
    # 检查资源是否核准
    if buyer_order_info.status_audit == STATUS_AUDIT_OK:
        resource = _('Order')
        abort(exceptions.Locked.code,
              _('The %(resource)s has been approved, it cannot be modified', resource=resource))

    template_name = 'buyer/order/edit.html'

    # 加载编辑表单
    form = BuyerOrderEditForm(request.form)
    form.uid.choices = get_user_choices()
    # form.status_order.choices = STATUS_ORDER_CHOICES

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('buyer order edit')

    # 进入编辑页面
    if request.method == 'GET':
        # 获取明细
        buyer_order_items = get_buyer_order_items_rows(buyer_order_id=buyer_order_id)
        # 表单赋值
        form.uid.data = buyer_order_info.uid
        form.supplier_cid.data = buyer_order_info.supplier_cid
        form.supplier_contact_id.data = buyer_order_info.supplier_contact_id
        form.type_tax.data = buyer_order_info.type_tax
        form.amount_order.data = buyer_order_info.amount_order
        # form.buyer_order_items = buyer_order_items
        while len(form.buyer_order_items) > 0:
            form.buyer_order_items.pop_entry()
        for buyer_order_item in buyer_order_items:
            buyer_order_item_form = BuyerOrderItemsEditForm()
            buyer_order_item_form.id = buyer_order_item.id
            buyer_order_item_form.buyer_order_id = buyer_order_item.buyer_order_id
            buyer_order_item_form.uid = buyer_order_item.uid
            # buyer_order_item_form.supplier_cid = buyer_order_item.supplier_cid
            # buyer_order_item_form.supplier_company_name = buyer_order_item.supplier_company_name
            buyer_order_item_form.custom_production_brand = buyer_order_item.custom_production_brand
            buyer_order_item_form.custom_production_model = buyer_order_item.custom_production_model
            buyer_order_item_form.production_id = buyer_order_item.production_id
            buyer_order_item_form.production_brand = buyer_order_item.production_brand
            buyer_order_item_form.production_model = buyer_order_item.production_model
            buyer_order_item_form.production_sku = buyer_order_item.production_sku
            buyer_order_item_form.delivery_time = buyer_order_item.delivery_time
            buyer_order_item_form.quantity = buyer_order_item.quantity
            buyer_order_item_form.unit_price = buyer_order_item.unit_price
            buyer_order_item_form.note = buyer_order_item.note
            buyer_order_item_form.type_tax = buyer_order_item.type_tax
            form.buyer_order_items.append_entry(buyer_order_item_form)

        # 渲染页面
        return render_template(
            template_name,
            buyer_order_id=buyer_order_id,
            form=form,
            **document_info
        )

    # 处理编辑请求
    if request.method == 'POST':
        # 增删数据行不需要校验表单

        # 表单新增空行
        if form.data_line_add.data is not None:
            if form.buyer_order_items.max_entries and len(
                    form.buyer_order_items.entries) >= form.buyer_order_items.max_entries:
                flash('最多创建%s条记录' % form.buyer_order_items.max_entries, 'danger')
            else:
                form.buyer_order_items.append_entry()

            return render_template(
                template_name,
                buyer_order_id=buyer_order_id,
                form=form,
                **document_info
            )
        # 表单删除一行
        if form.data_line_del.data is not None:
            if form.buyer_order_items.min_entries and len(
                    form.buyer_order_items.entries) <= form.buyer_order_items.min_entries:
                flash('最少保留%s条记录' % form.buyer_order_items.min_entries, 'danger')
            else:
                data_line_index = form.data_line_del.data
                form.buyer_order_items.entries.pop(data_line_index)

            return render_template(
                template_name,
                buyer_order_id=buyer_order_id,
                form=form,
                **document_info
            )

        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Edit Failure'), 'danger')
            # flash(form.errors, 'danger')
            # flash(form.buyer_order_items.errors, 'danger')
            return render_template(
                template_name,
                buyer_order_id=buyer_order_id,
                form=form,
                **document_info
            )
        # 表单校验成功

        # 获取明细
        buyer_order_items = get_buyer_order_items_rows(buyer_order_id=buyer_order_id)
        buyer_order_items_ids = [item.id for item in buyer_order_items]

        # 数据新增、数据删除、数据修改

        buyer_order_items_ids_new = []
        amount_buyer_order = 0
        for buyer_order_item in form.buyer_order_items.entries:
            # 错误
            if buyer_order_item.form.id.data and buyer_order_item.form.id.data not in buyer_order_items_ids:
                continue

            buyer_order_item_data = {
                'buyer_order_id': buyer_order_id,
                'uid': form.uid.data,
                'supplier_cid': form.supplier_cid.data,
                'supplier_company_name': get_supplier_row_by_id(form.supplier_cid.data).company_name,
                'custom_production_brand': buyer_order_item.form.custom_production_brand.data,
                'custom_production_model': buyer_order_item.form.custom_production_model.data,
                'production_id': buyer_order_item.form.production_id.data,
                'production_brand': buyer_order_item.form.production_brand.data,
                'production_model': buyer_order_item.form.production_model.data,
                'production_sku': buyer_order_item.form.production_sku.data,
                'delivery_time': buyer_order_item.form.delivery_time.data,
                'quantity': buyer_order_item.form.quantity.data,
                'unit_price': buyer_order_item.form.unit_price.data,
                'note': buyer_order_item.form.note.data,
                'type_tax': form.type_tax.data,
            }

            if not buyer_order_item.form.id.data:
                # 新增
                add_buyer_order_items(buyer_order_item_data)
                amount_buyer_order += buyer_order_item_data['quantity'] * buyer_order_item_data['unit_price']
            else:
                # 修改
                edit_buyer_order_items(buyer_order_item.form.id.data, buyer_order_item_data)
                amount_buyer_order += buyer_order_item_data['quantity'] * buyer_order_item_data['unit_price']
                buyer_order_items_ids_new.append(buyer_order_item.form.id.data)
        # 删除
        buyer_order_items_ids_del = list(set(buyer_order_items_ids) - set(buyer_order_items_ids_new))
        for buyer_order_items_id in buyer_order_items_ids_del:
            delete_buyer_order_items(buyer_order_items_id)

        # 更新采购订单
        current_time = datetime.utcnow()
        buyer_order_data = {
            'uid': form.uid.data,
            'supplier_cid': form.supplier_cid.data,
            'supplier_contact_id': form.supplier_contact_id.data,
            'type_tax': form.type_tax.data,
            'amount_production': amount_buyer_order,
            'amount_order': amount_buyer_order,
            'update_time': current_time,
        }
        result = edit_buyer_order(buyer_order_id, buyer_order_data)

        # 编辑操作成功
        if result:
            flash(_('Edit Success'), 'success')
            return redirect(request.args.get('next') or url_for('buyer_order.lists'))
        # 编辑操作失败
        else:
            flash(_('Edit Failure'), 'danger')
            return render_template(
                template_name,
                buyer_order_id=buyer_order_id,
                form=form,
                **document_info
            )


@bp_buyer_order.route('/<int:buyer_order_id>/info.html')
@login_required
def info(buyer_order_id):
    """
    订单详情
    :param buyer_order_id:
    :return:
    """
    buyer_order_info = get_buyer_order_row_by_id(buyer_order_id)
    # 检查资源是否存在
    if not buyer_order_info:
        abort(404)
    # 检查资源是否删除
    if buyer_order_info.status_delete == STATUS_DEL_OK:
        abort(410)

    buyer_order_print_date = time_utc_to_local(buyer_order_info.update_time).strftime('%Y-%m-%d')
    buyer_order_code = '%s%s' % (g.BUYER_ORDER_PREFIX, time_utc_to_local(buyer_order_info.create_time).strftime('%y%m%d%H%M%S'))

    # 获取渠道公司信息
    supplier_info = get_supplier_row_by_id(buyer_order_info.supplier_cid)

    # 获取渠道联系方式
    supplier_contact_info = get_supplier_contact_row_by_id(buyer_order_info.supplier_contact_id)

    # 获取询价人员信息
    user_info = get_user_row_by_id(buyer_order_info.uid)

    buyer_order_items = get_buyer_order_items_rows(buyer_order_id=buyer_order_id)

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('buyer order info')

    template_name = 'buyer/order/info.html'

    return render_template(
        template_name,
        buyer_order_id=buyer_order_id,
        buyer_order_info=buyer_order_info,
        supplier_info=supplier_info,
        supplier_contact_info=supplier_contact_info,
        user_info=user_info,
        buyer_order_items=buyer_order_items,
        buyer_order_print_date=buyer_order_print_date,
        buyer_order_code=buyer_order_code,
        **document_info
    )


@bp_buyer_order.route('/<int:buyer_order_id>/preview.html')
@login_required
def preview(buyer_order_id):
    """
    打印预览
    :param buyer_order_id:
    :return:
    """
    buyer_order_info = get_buyer_order_row_by_id(buyer_order_id)
    # 检查资源是否存在
    if not buyer_order_info:
        abort(404)
    # 检查资源是否删除
    if buyer_order_info.status_delete == STATUS_DEL_OK:
        abort(410)

    buyer_order_print_date = time_utc_to_local(buyer_order_info.update_time).strftime('%Y-%m-%d')
    buyer_order_code = '%s%s' % (g.BUYER_ORDER_PREFIX, time_utc_to_local(buyer_order_info.create_time).strftime('%y%m%d%H%M%S'))

    # 获取渠道公司信息
    supplier_info = get_supplier_row_by_id(buyer_order_info.supplier_cid)

    # 获取渠道联系方式
    supplier_contact_info = get_supplier_contact_row_by_id(buyer_order_info.supplier_contact_id)

    # 获取询价人员信息
    user_info = get_user_row_by_id(buyer_order_info.uid)

    buyer_order_items = get_buyer_order_items_rows(buyer_order_id=buyer_order_id)

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('buyer order preview')

    template_name = 'buyer/order/preview.html'

    return render_template(
        template_name,
        buyer_order_id=buyer_order_id,
        buyer_order_info=buyer_order_info,
        supplier_info=supplier_info,
        supplier_contact_info=supplier_contact_info,
        user_info=user_info,
        buyer_order_items=buyer_order_items,
        buyer_order_print_date=buyer_order_print_date,
        buyer_order_code=buyer_order_code,
        **document_info
    )


@bp_buyer_order.route('/<int:buyer_order_id>.pdf')
@login_required
def pdf(buyer_order_id):
    """
    文件下载
    :param buyer_order_id:
    :return:
    """
    buyer_order_info = get_buyer_order_row_by_id(buyer_order_id)
    # 检查资源是否存在
    if not buyer_order_info:
        abort(404)
    # 检查资源是否删除
    if buyer_order_info.status_delete == STATUS_DEL_OK:
        abort(410)

    buyer_order_print_date = time_utc_to_local(buyer_order_info.update_time).strftime('%Y-%m-%d')
    buyer_order_code = '%s%s' % (g.BUYER_ORDER_PREFIX, time_utc_to_local(buyer_order_info.create_time).strftime('%y%m%d%H%M%S'))

    # 获取渠道公司信息
    supplier_info = get_supplier_row_by_id(buyer_order_info.supplier_cid)

    # 获取渠道联系方式
    supplier_contact_info = get_supplier_contact_row_by_id(buyer_order_info.supplier_contact_id)

    # 获取询价人员信息
    user_info = get_user_row_by_id(buyer_order_info.uid)

    buyer_order_items = get_buyer_order_items_rows(buyer_order_id=buyer_order_id)

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('buyer order pdf')

    template_name = 'buyer/order/pdf.html'

    html = render_template(
        template_name,
        buyer_order_id=buyer_order_id,
        buyer_order_info=buyer_order_info,
        supplier_info=supplier_info,
        supplier_contact_info=supplier_contact_info,
        user_info=user_info,
        buyer_order_items=buyer_order_items,
        buyer_order_print_date=buyer_order_print_date,
        buyer_order_code=buyer_order_code,
        **document_info
    )
    # return html
    return render_pdf(
        html=HTML(string=html),
        stylesheets=[CSS(string='@page {size:A4; margin:35px;}')],
        download_filename='采购订单.pdf'.encode('utf-8')
    )


@bp_buyer_order.route('/ajax/del', methods=['GET', 'POST'])
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
    buyer_order_id = request.args.get('buyer_order_id', 0, type=int)
    if not buyer_order_id:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查删除权限
    buyer_orders_item_del_permission = BuyerOrderItemDelPermission(buyer_order_id)
    if not buyer_orders_item_del_permission.can():
        ext_msg = _('Permission Denied')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    enquiry_info = get_buyer_order_row_by_id(buyer_order_id)
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
    result = edit_buyer_order(buyer_order_id, enquiry_data)
    if result:
        # 发送删除信号
        signal_data = {
            'buyer_order_id': buyer_order_id,
            'status_delete': STATUS_DEL_OK,
            'current_time': current_time,
        }
        signal_buyer_orders_status_delete.send(app, **signal_data)

        ajax_success_msg['msg'] = _('Del Success')
        return jsonify(ajax_success_msg)
    else:
        ajax_failure_msg['msg'] = _('Del Failure')
        return jsonify(ajax_failure_msg)


@bp_buyer_order.route('/ajax/audit', methods=['GET', 'POST'])
@login_required
def ajax_audit():
    """
    订单审核
    :return:
    """
    ajax_success_msg = AJAX_SUCCESS_MSG.copy()
    ajax_failure_msg = AJAX_FAILURE_MSG.copy()

    # 检查请求方法
    if not (request.method == 'GET' and request.is_xhr):
        ext_msg = _('Method Not Allowed')
        ajax_failure_msg['msg'] = _('Audit Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查请求参数
    buyer_order_id = request.args.get('buyer_order_id', 0, type=int)
    audit_status = request.args.get('audit_status', 0, type=int)
    if not buyer_order_id:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Audit Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查删除权限
    buyer_order_del_permission = BuyerOrderItemDelPermission(buyer_order_id)
    if not buyer_order_del_permission.can():
        ext_msg = _('Permission Denied')
        ajax_failure_msg['msg'] = _('Audit Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    buyer_order_info = get_buyer_order_row_by_id(buyer_order_id)
    # 检查资源是否存在
    if not buyer_order_info:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Audit Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)
    # 检查资源是否删除
    if buyer_order_info.status_delete == STATUS_DEL_OK:
        ext_msg = _('Already deleted')
        ajax_failure_msg['msg'] = _('Audit Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)
    # 检查审核状态是否变化
    if buyer_order_info.status_audit == audit_status:
        ext_msg = _('Already audited')
        ajax_failure_msg['msg'] = _('Audit Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    current_time = datetime.utcnow()
    buyer_order_data = {
        'status_audit': audit_status,
        'audit_time': current_time,
        'update_time': current_time,
    }
    result = edit_buyer_order(buyer_order_id, buyer_order_data)
    if result:
        ajax_success_msg['msg'] = _('Audit Success')
        return jsonify(ajax_success_msg)
    else:
        ajax_failure_msg['msg'] = _('Audit Failure')
        return jsonify(ajax_failure_msg)


@bp_buyer_order.route('/stats.html', methods=['GET', 'POST'])
@login_required
def stats():
    return jsonify({})
