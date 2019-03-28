#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: delivery.py
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
    g,
)
from flask_babel import gettext as _
from flask_login import login_required, current_user
from flask_weasyprint import render_pdf, HTML, CSS

from app_backend import (
    app,
    excel,
)
from app_backend.api.customer import get_customer_row_by_id
from app_backend.api.customer_contact import get_customer_contact_row_by_id
from app_backend.api.rack import get_rack_choices
from app_backend.api.supplier import get_supplier_row_by_id
from app_backend.api.warehouse import get_warehouse_choices
from app_backend.signals.delivery import signal_delivery_status_delete

from app_common.maps.default import default_search_choices_int, default_search_choice_option_int
from app_backend.api.delivery import add_delivery, get_delivery_user_list_choices, get_delivery_rows, \
    get_delivery_pagination, edit_delivery, get_delivery_row_by_id
from app_backend.api.delivery_items import add_delivery_items, edit_delivery_items, get_delivery_items_rows, \
    delete_delivery_items
from app_backend.api.user import get_user_choices, get_user_row_by_id
from app_backend.forms.delivery import DeliverySearchForm, DeliveryEditForm, DeliveryItemsEditForm
from app_backend.forms.delivery import DeliveryAddForm
from app_common.maps.status_order import STATUS_ORDER_CHOICES
from app_common.maps.status_delete import (
    STATUS_DEL_OK,
    STATUS_DEL_NO)

from app_backend.models.bearing_project import Delivery
from app_backend.permissions import (
    permission_delivery_section_add,
    permission_delivery_section_search,
    permission_delivery_section_export,
    permission_delivery_section_stats,
    DeliveryItemGetPermission,
    DeliveryItemEditPermission,
    DeliveryItemDelPermission,
)


# 定义蓝图
from app_common.tools.date_time import time_utc_to_local

bp_delivery = Blueprint('delivery', __name__, url_prefix='/delivery')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


@bp_delivery.route('/lists.html', methods=['GET', 'POST'])
@login_required
def lists():
    template_name = 'delivery/lists.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('delivery lists')

    # 搜索条件
    form = DeliverySearchForm(request.form)
    form.uid.choices = get_delivery_user_list_choices()
    # app.logger.info('')

    search_condition = [
        Delivery.status_delete == STATUS_DEL_NO,
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
                search_condition.append(Delivery.uid == form.uid.data)
            if form.customer_cid.data and form.customer_company_name.data:
                search_condition.append(Delivery.cid == form.customer_cid.data)
            if form.start_create_time.data:
                search_condition.append(Delivery.create_time >= form.start_create_time.data)
            if form.end_create_time.data:
                search_condition.append(Delivery.create_time <= form.end_create_time.data)
        # 处理导出
        if form.op.data == 1:
            # 检查导出权限
            if not permission_delivery_section_export.can():
                abort(403)
            column_names = Delivery.__table__.columns.keys()
            query_sets = get_delivery_rows(*search_condition)

            return excel.make_response_from_query_sets(
                query_sets=query_sets,
                column_names=column_names,
                file_type='csv',
                file_name='%s.csv' % _('delivery lists')
            )
        # 批量删除
        if form.op.data == 2:
            order_ids = request.form.getlist('order_id')
            # 检查删除权限
            permitted = True
            for order_id in order_ids:
                delivery_item_del_permission = DeliveryItemDelPermission(order_id)
                if not delivery_item_del_permission.can():
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
                    result = edit_delivery(order_id, quotation_data)
                    if result:
                        # 发送删除信号
                        signal_data = {
                            'order_id': order_id,
                            'status_delete': STATUS_DEL_OK,
                            'current_time': current_time,
                        }
                        signal_delivery_status_delete.send(app, **signal_data)
                    result_total = result_total and result
                if result_total:
                    flash(_('Del Success'), 'success')
                else:
                    flash(_('Del Failure'), 'danger')
    # 翻页数据
    pagination = get_delivery_pagination(form.page.data, PER_PAGE_BACKEND, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )


@bp_delivery.route('/add.html', methods=['GET', 'POST'])
@login_required
def add():
    """
    新增销售出货
    :return:
    """
    # return jsonify({})
    template_name = 'delivery/add.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('delivery add')

    # 加载创建表单
    form = DeliveryAddForm(request.form)
    form.uid.choices = get_user_choices()
    form.uid.data = current_user.id
    form.warehouse_id.choices = get_warehouse_choices(option_type='create')
    # 内嵌表单货架选项
    for item_form in form.delivery_items:
        item_form.rack_id.choices = get_rack_choices(form.warehouse_id.data, option_type='create')

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
        # 修改仓库 - 不做校验
        if form.warehouse_changed.data:
            form.warehouse_changed.data = ''
            return render_template(
                template_name,
                form=form,
                **document_info
            )

        # 表单新增空行
        if form.data_line_add.data is not None:
            if form.delivery_items.max_entries and len(
                    form.delivery_items.entries) >= form.delivery_items.max_entries:
                flash('最多创建%s条记录' % form.delivery_items.max_entries, 'danger')
            else:
                form.delivery_items.append_entry()
                # 内嵌表单货架选项
                for item_form in form.delivery_items:
                    item_form.rack_id.choices = get_rack_choices(form.warehouse_id.data, option_type='create')

            return render_template(
                template_name,
                form=form,
                **document_info
            )
        # 表单删除一行
        if form.data_line_del.data is not None:
            if form.delivery_items.min_entries and len(
                    form.delivery_items.entries) <= form.delivery_items.min_entries:
                flash('最少保留%s条记录' % form.delivery_items.min_entries, 'danger')
            else:
                data_line_index = form.data_line_del.data
                form.delivery_items.entries.pop(data_line_index)

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
        delivery_data = {
            'uid': form.uid.data,
            'customer_cid': form.customer_cid.data,
            'customer_contact_id': form.customer_contact_id.data,
            # 'type_delivery': form.type_delivery.data,
            'warehouse_id': form.warehouse_id.data,
            'create_time': current_time,
            'update_time': current_time,
        }
        delivery_id = add_delivery(delivery_data)

        amount_delivery = 0
        for delivery_item in form.delivery_items.entries:
            current_time = datetime.utcnow()
            delivery_item_data = {
                'delivery_id': delivery_id,
                'uid': form.uid.data,
                'customer_cid': form.customer_cid.data,
                'customer_company_name': get_customer_row_by_id(form.customer_cid.data).company_name,
                'production_id': delivery_item.form.production_id.data,
                'production_brand': delivery_item.form.production_brand.data,
                'production_model': delivery_item.form.production_model.data,
                'production_sku': delivery_item.form.production_sku.data,
                'warehouse_id': form.warehouse_id.data,
                'rack_id': delivery_item.form.rack_id.data,
                'note': delivery_item.form.note.data,
                'quantity': delivery_item.form.quantity.data,
                'unit_price': delivery_item.form.unit_price.data,
                'create_time': current_time,
                'update_time': current_time,
            }

            # 新增
            add_delivery_items(delivery_item_data)
            amount_delivery += (delivery_item_data['quantity'] or 0) * (delivery_item_data['unit_price'] or 0)

        # 更新报价
        delivery_data = {
            'amount_production': amount_delivery,
            'amount_delivery': amount_delivery,
            'update_time': current_time,
        }
        result = edit_delivery(delivery_id, delivery_data)

        # todo 事务

        # 明细保存
        # 总表保存

        # 创建操作成功
        if result:
            flash(_('Add Success'), 'success')
            return redirect(request.args.get('next') or url_for('delivery.lists'))
        # 创建操作失败
        else:
            flash(_('Add Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                **document_info
            )


@bp_delivery.route('/<int:delivery_id>/edit.html', methods=['GET', 'POST'])
@login_required
def edit(delivery_id):
    """
    销售出货编辑
    """
    # 检查编辑权限
    # enquiry_item_edit_permission = EnquiryItemEditPermission(enquiry_id)
    # if not enquiry_item_edit_permission.can():
    #     abort(403)

    delivery_info = get_delivery_row_by_id(delivery_id)
    # 检查资源是否存在
    if not delivery_info:
        abort(404)
    # 检查资源是否删除
    if delivery_info.status_delete == STATUS_DEL_OK:
        abort(410)

    template_name = 'delivery/edit.html'

    # 加载编辑表单
    form = DeliveryEditForm(request.form)
    form.uid.choices = get_user_choices()
    form.warehouse_id.choices = get_warehouse_choices(option_type='update')
    # 内嵌表单货架选项
    for item_form in form.delivery_items:
        item_form.rack_id.choices = get_rack_choices(form.warehouse_id.data, option_type='update')

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('delivery edit')

    # 进入编辑页面
    if request.method == 'GET':
        # 获取明细
        delivery_items = get_delivery_items_rows(delivery_id=delivery_id)
        # 表单赋值
        form.uid.data = delivery_info.uid
        form.customer_cid.data = delivery_info.customer_cid
        form.customer_contact_id.data = delivery_info.customer_contact_id
        form.type_tax.data = delivery_info.type_tax
        form.warehouse_id.data = delivery_info.warehouse_id
        form.amount_delivery.data = delivery_info.amount_delivery
        # form.buyer_order_items = buyer_order_items
        while len(form.delivery_items) > 0:
            form.delivery_items.pop_entry()
        for delivery_item in delivery_items:
            delivery_item_form = DeliveryItemsEditForm()
            delivery_item_form.id = delivery_item.id
            delivery_item_form.delivery_id = delivery_item.delivery_id
            delivery_item_form.uid = delivery_item.uid
            # delivery_item_form.supplier_cid = delivery_item.supplier_cid
            # delivery_item_form.supplier_company_name = delivery_item.supplier_company_name
            delivery_item_form.custom_production_brand = delivery_item.custom_production_brand
            delivery_item_form.custom_production_model = delivery_item.custom_production_model
            delivery_item_form.production_id = delivery_item.production_id
            delivery_item_form.production_brand = delivery_item.production_brand
            delivery_item_form.production_model = delivery_item.production_model
            delivery_item_form.production_sku = delivery_item.production_sku
            delivery_item_form.quantity = delivery_item.quantity
            delivery_item_form.unit_price = delivery_item.unit_price
            delivery_item_form.rack_id = delivery_item.rack_id
            delivery_item_form.note = delivery_item.note
            delivery_item_form.type_tax = delivery_item.type_tax
            form.delivery_items.append_entry(delivery_item_form)

        # 内嵌表单货架选项
        for item_form in form.delivery_items:
            item_form.rack_id.choices = get_rack_choices(form.warehouse_id.data, option_type='update')
        # 渲染页面
        return render_template(
            template_name,
            delivery_id=delivery_id,
            form=form,
            **document_info
        )

    # 处理编辑请求
    if request.method == 'POST':
        # 修改仓库 - 不做校验
        if form.warehouse_changed.data:
            form.warehouse_changed.data = ''
            return render_template(
                template_name,
                form=form,
                **document_info
            )
        # 增删数据行不需要校验表单

        # 表单新增空行
        if form.data_line_add.data is not None:
            if form.delivery_items.max_entries and len(
                    form.delivery_items.entries) >= form.delivery_items.max_entries:
                flash('最多创建%s条记录' % form.delivery_items.max_entries, 'danger')
            else:
                form.delivery_items.append_entry()
                # 内嵌表单货架选项
                for item_form in form.delivery_items:
                    item_form.rack_id.choices = get_rack_choices(form.warehouse_id.data, option_type='update')

            return render_template(
                template_name,
                delivery_id=delivery_id,
                form=form,
                **document_info
            )
        # 表单删除一行
        if form.data_line_del.data is not None:
            if form.delivery_items.min_entries and len(
                    form.delivery_items.entries) <= form.delivery_items.min_entries:
                flash('最少保留%s条记录' % form.delivery_items.min_entries, 'danger')
            else:
                data_line_index = form.data_line_del.data
                form.delivery_items.entries.pop(data_line_index)

            return render_template(
                template_name,
                delivery_id=delivery_id,
                form=form,
                **document_info
            )

        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Edit Failure'), 'danger')
            # flash(form.errors, 'danger')
            # flash(form.delivery_items.errors, 'danger')
            return render_template(
                template_name,
                delivery_id=delivery_id,
                form=form,
                **document_info
            )
        # 表单校验成功

        # 获取明细
        delivery_items = get_delivery_items_rows(delivery_id=delivery_id)
        delivery_items_ids = [item.id for item in delivery_items]

        # 数据新增、数据删除、数据修改

        delivery_items_ids_new = []
        amount_delivery = 0
        for delivery_item in form.delivery_items.entries:
            # 错误
            if delivery_item.form.id.data and delivery_item.form.id.data not in delivery_items_ids:
                continue

            delivery_item_data = {
                'delivery_id': delivery_id,
                'uid': form.uid.data,
                'customer_cid': form.customer_cid.data,
                'customer_company_name': get_customer_row_by_id(form.customer_cid.data).company_name,
                'custom_production_brand': delivery_item.form.custom_production_brand.data,
                'custom_production_model': delivery_item.form.custom_production_model.data,
                'production_id': delivery_item.form.production_id.data,
                'production_brand': delivery_item.form.production_brand.data,
                'production_model': delivery_item.form.production_model.data,
                'production_sku': delivery_item.form.production_sku.data,
                'quantity': delivery_item.form.quantity.data,
                'unit_price': delivery_item.form.unit_price.data,
                'warehouse_id': form.warehouse_id.data,
                'rack_id': delivery_item.form.rack_id.data,
                'note': delivery_item.form.note.data,
                'type_tax': form.type_tax.data,
            }

            if not delivery_item.form.id.data:
                # 新增
                add_delivery_items(delivery_item_data)
                amount_delivery += delivery_item_data['quantity'] * delivery_item_data['unit_price']
            else:
                # 修改
                edit_delivery_items(delivery_item.form.id.data, delivery_item_data)
                amount_delivery += delivery_item_data['quantity'] * delivery_item_data['unit_price']
                delivery_items_ids_new.append(delivery_item.form.id.data)
        # 删除
        delivery_items_ids_del = list(set(delivery_items_ids) - set(delivery_items_ids_new))
        for delivery_items_id in delivery_items_ids_del:
            delete_delivery_items(delivery_items_id)

        # 更新销售出货
        current_time = datetime.utcnow()
        delivery_data = {
            'uid': form.uid.data,
            'customer_cid': form.customer_cid.data,
            'customer_contact_id': form.customer_contact_id.data,
            'type_tax': form.type_tax.data,
            'amount_production': amount_delivery,
            'amount_delivery': amount_delivery,
            'warehouse_id': form.warehouse_id.data,
            'update_time': current_time,
        }
        result = edit_delivery(delivery_id, delivery_data)

        # 编辑操作成功
        if result:
            flash(_('Edit Success'), 'success')
            return redirect(request.args.get('next') or url_for('delivery.lists'))
        # 编辑操作失败
        else:
            flash(_('Edit Failure'), 'danger')
            return render_template(
                template_name,
                delivery_id=delivery_id,
                form=form,
                **document_info
            )


@bp_delivery.route('/<int:delivery_id>/info.html')
@login_required
def info(delivery_id):
    """
    出货详情
    :param delivery_id:
    :return:
    """
    delivery_info = get_delivery_row_by_id(delivery_id)
    # 检查资源是否存在
    if not delivery_info:
        abort(404)
    # 检查资源是否删除
    if delivery_info.status_delete == STATUS_DEL_OK:
        abort(410)

    delivery_print_date = time_utc_to_local(delivery_info.update_time).strftime('%Y-%m-%d')
    delivery_code = '%s%s' % (g.ENQUIRIES_PREFIX, time_utc_to_local(delivery_info.create_time).strftime('%y%m%d%H%M%S'))

    # 获取客户公司信息
    customer_info = get_customer_row_by_id(delivery_info.customer_cid)

    # 获取客户联系方式
    customer_contact_info = get_customer_contact_row_by_id(delivery_info.customer_contact_id)

    # 获取出货人员信息
    user_info = get_user_row_by_id(delivery_info.uid)

    delivery_items = get_delivery_items_rows(delivery_id=delivery_id)

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('delivery info')

    template_name = 'delivery/info.html'

    return render_template(
        template_name,
        delivery_id=delivery_id,
        delivery_info=delivery_info,
        customer_info=customer_info,
        customer_contact_info=customer_contact_info,
        user_info=user_info,
        delivery_items=delivery_items,
        delivery_print_date=delivery_print_date,
        delivery_code=delivery_code,
        **document_info
    )


@bp_delivery.route('/<int:delivery_id>/preview.html')
@login_required
def preview(delivery_id):
    """
    打印预览
    :param delivery_id:
    :return:
    """
    delivery_info = get_delivery_row_by_id(delivery_id)
    # 检查资源是否存在
    if not delivery_info:
        abort(404)
    # 检查资源是否删除
    if delivery_info.status_delete == STATUS_DEL_OK:
        abort(410)

    delivery_print_date = time_utc_to_local(delivery_info.update_time).strftime('%Y-%m-%d')
    delivery_code = '%s%s' % (g.ENQUIRIES_PREFIX, time_utc_to_local(delivery_info.create_time).strftime('%y%m%d%H%M%S'))

    # 获取客户公司信息
    customer_info = get_customer_row_by_id(delivery_info.customer_cid)

    # 获取客户联系方式
    customer_contact_info = get_customer_contact_row_by_id(delivery_info.customer_contact_id)

    # 获取出货人员信息
    user_info = get_user_row_by_id(delivery_info.uid)

    delivery_items = get_delivery_items_rows(delivery_id=delivery_id)

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('delivery preview')

    template_name = 'delivery/preview.html'

    return render_template(
        template_name,
        delivery_id=delivery_id,
        delivery_info=delivery_info,
        customer_info=customer_info,
        customer_contact_info=customer_contact_info,
        user_info=user_info,
        delivery_items=delivery_items,
        delivery_print_date=delivery_print_date,
        delivery_code=delivery_code,
        **document_info
    )


@bp_delivery.route('/<int:delivery_id>.pdf')
@login_required
def pdf(delivery_id):
    """
    文件下载
    :param delivery_id:
    :return:
    """
    delivery_info = get_delivery_row_by_id(delivery_id)
    # 检查资源是否存在
    if not delivery_info:
        abort(404)
    # 检查资源是否删除
    if delivery_info.status_delete == STATUS_DEL_OK:
        abort(410)

    delivery_print_date = time_utc_to_local(delivery_info.update_time).strftime('%Y-%m-%d')
    delivery_code = '%s%s' % (g.ENQUIRIES_PREFIX, time_utc_to_local(delivery_info.create_time).strftime('%y%m%d%H%M%S'))

    # 获取客户公司信息
    customer_info = get_customer_row_by_id(delivery_info.customer_cid)

    # 获取客户联系方式
    customer_contact_info = get_customer_contact_row_by_id(delivery_info.customer_contact_id)

    # 获取出货人员信息
    user_info = get_user_row_by_id(delivery_info.uid)

    delivery_items = get_delivery_items_rows(delivery_id=delivery_id)

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('delivery pdf')

    template_name = 'delivery/pdf.html'

    html = render_template(
        template_name,
        delivery_id=delivery_id,
        delivery_info=delivery_info,
        customer_info=customer_info,
        customer_contact_info=customer_contact_info,
        user_info=user_info,
        delivery_items=delivery_items,
        delivery_print_date=delivery_print_date,
        delivery_code=delivery_code,
        **document_info
    )
    # return html
    return render_pdf(
        html=HTML(string=html),
        stylesheets=[CSS(string='@page {size:A4; margin:35px;}')],
        download_filename='销售出货.pdf'.encode('utf-8')
    )


@bp_delivery.route('/ajax/del', methods=['GET', 'POST'])
@login_required
def ajax_delete():
    """
    销售出货删除
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
    delivery_id = request.args.get('delivery_id', 0, type=int)
    if not delivery_id:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查删除权限
    delivery_item_del_permission = DeliveryItemDelPermission(delivery_id)
    if not delivery_item_del_permission.can():
        ext_msg = _('Permission Denied')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    delivery_info = get_delivery_row_by_id(delivery_id)
    # 检查资源是否存在
    if not delivery_info:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)
    # 检查资源是否删除
    if delivery_info.status_delete == STATUS_DEL_OK:
        ext_msg = _('Already deleted')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_success_msg)

    current_time = datetime.utcnow()
    delivery_data = {
        'status_delete': STATUS_DEL_OK,
        'delete_time': current_time,
        'update_time': current_time,
    }
    result = edit_delivery(delivery_id, delivery_data)
    if result:
        # 发送删除信号
        signal_data = {
            'delivery_id': delivery_id,
            'status_delete': STATUS_DEL_OK,
            'current_time': current_time,
        }
        signal_delivery_status_delete.send(app, **signal_data)

        ajax_success_msg['msg'] = _('Del Success')
        return jsonify(ajax_success_msg)
    else:
        ajax_failure_msg['msg'] = _('Del Failure')
        return jsonify(ajax_failure_msg)
