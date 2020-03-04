#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: purchase.py
@time: 2018-08-31 15:41
"""

from __future__ import unicode_literals

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
    g)
from flask_babel import gettext as _
from flask_login import login_required, current_user
from flask_weasyprint import render_pdf, HTML, CSS
from werkzeug import exceptions

from app_backend import (
    app,
    excel,
)
from app_backend.api.purchase import add_purchase, get_purchase_user_list_choices, get_purchase_rows, \
    get_purchase_pagination, edit_purchase, get_purchase_row_by_id, audit_purchase, cancel_audit_purchase
from app_backend.api.purchase_items import add_purchase_items, edit_purchase_items, get_purchase_items_rows, \
    delete_purchase_items
from app_backend.api.rack import get_rack_choices
from app_backend.api.supplier import get_supplier_row_by_id
from app_backend.api.supplier_contact import get_supplier_contact_row_by_id
from app_backend.api.user import get_user_choices, get_user_row_by_id
from app_backend.api.warehouse import get_warehouse_choices
from app_backend.forms.purchase import PurchaseAddForm
from app_backend.forms.purchase import PurchaseSearchForm, PurchaseEditForm, PurchaseItemsEditForm
from app_backend.models.model_bearing import Purchase
from app_backend.permissions.buyer_purchase import (
    permission_purchase_section_export,
    permission_purchase_section_del,
    permission_purchase_section_audit, permission_purchase_section_search, permission_purchase_section_add,
    permission_purchase_section_edit, permission_purchase_section_get, permission_purchase_section_print)
from app_backend.signals.purchase import signal_purchase_status_delete
from app_common.maps.default import DEFAULT_SEARCH_CHOICES_INT_OPTION
from app_common.maps.operations import OPERATION_EXPORT, OPERATION_DELETE
from app_common.maps.status_audit import STATUS_AUDIT_NO, STATUS_AUDIT_OK
from app_common.maps.status_delete import (
    STATUS_DEL_OK,
    STATUS_DEL_NO)
# 定义蓝图
from app_common.tools.date_time import time_utc_to_local

bp_purchase = Blueprint('purchase', __name__, url_prefix='/purchase')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


@bp_purchase.route('/lists.html', methods=['GET', 'POST'])
@login_required
@permission_purchase_section_search.require(http_exception=403)
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
            if form.uid.data != DEFAULT_SEARCH_CHOICES_INT_OPTION:
                search_condition.append(Purchase.uid == form.uid.data)
            if form.supplier_cid.data and form.supplier_company_name.data:
                search_condition.append(Purchase.supplier_cid == form.supplier_cid.data)
            if form.start_create_time.data:
                search_condition.append(Purchase.create_time >= form.start_create_time.data)
            if form.end_create_time.data:
                search_condition.append(Purchase.create_time <= form.end_create_time.data)
        # 处理导出
        if form.op.data == OPERATION_EXPORT:
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
        if form.op.data == OPERATION_DELETE:
            # 检查删除权限
            if not permission_purchase_section_del.can():
                abort(403)
            purchase_ids = request.form.getlist('purchase_id')
            # 检查删除权限
            permitted = True
            for purchase_id in purchase_ids:
                # TODO 资源删除权限验证
                if False:
                    ext_msg = _('Permission Denied')
                    flash(_('Del Failure, %(ext_msg)s', ext_msg=ext_msg), 'danger')
                    permitted = False
                    break
            if permitted:
                result_total = True
                for purchase_id in purchase_ids:
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
@permission_purchase_section_add.require(http_exception=403)
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
    form.warehouse_id.choices = get_warehouse_choices(option_type='create')
    # 内嵌表单货架选项
    for item_form in form.purchase_items:
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
            if form.purchase_items.max_entries and len(
                    form.purchase_items.entries) >= form.purchase_items.max_entries:
                flash('最多创建%s条记录' % form.purchase_items.max_entries, 'danger')
            else:
                form.purchase_items.append_entry()
                # 内嵌表单货架选项
                for item_form in form.purchase_items:
                    item_form.rack_id.choices = get_rack_choices(form.warehouse_id.data, option_type='create')

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
            'warehouse_id': form.warehouse_id.data,
            'create_time': current_time,
            'update_time': current_time,
        }
        purchase_id = add_purchase(purchase_data)

        amount_purchase = 0
        for purchase_item in form.purchase_items.entries:
            current_time = datetime.utcnow()
            purchase_item_data = {
                'purchase_id': purchase_id,
                'uid': form.uid.data,
                'supplier_cid': form.supplier_cid.data,
                'supplier_company_name': get_supplier_row_by_id(form.supplier_cid.data).company_name,
                'production_id': purchase_item.form.production_id.data,
                'production_brand': purchase_item.form.production_brand.data,
                'production_model': purchase_item.form.production_model.data,
                'production_sku': purchase_item.form.production_sku.data,
                'warehouse_id': form.warehouse_id.data,
                'rack_id': purchase_item.form.rack_id.data,
                'note': purchase_item.form.note.data,
                'quantity': purchase_item.form.quantity.data,
                'unit_price': purchase_item.form.unit_price.data,
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


@bp_purchase.route('/<int:purchase_id>/edit.html', methods=['GET', 'POST'])
@login_required
@permission_purchase_section_edit.require(http_exception=403)
def edit(purchase_id):
    """
    采购进货编辑
    """
    # 检查编辑权限
    # enquiry_item_edit_permission = EnquiryItemEditPermission(enquiry_id)
    # if not enquiry_item_edit_permission.can():
    #     abort(403)

    purchase_info = get_purchase_row_by_id(purchase_id)
    # 检查资源是否存在
    if not purchase_info:
        abort(404)
    # 检查资源是否删除
    if purchase_info.status_delete == STATUS_DEL_OK:
        abort(410)
    # 检查资源是否核准
    if purchase_info.status_audit == STATUS_AUDIT_OK:
        resource = _('Purchase')
        abort(exceptions.Locked.code,
              _('The %(resource)s has been approved, it cannot be modified', resource=resource))

    template_name = 'purchase/edit.html'

    # 加载编辑表单
    form = PurchaseEditForm(request.form)
    form.uid.choices = get_user_choices()
    form.warehouse_id.choices = get_warehouse_choices(option_type='update')
    # 内嵌表单货架选项
    for item_form in form.purchase_items:
        item_form.rack_id.choices = get_rack_choices(form.warehouse_id.data, option_type='update')

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('purchase edit')

    # 进入编辑页面
    if request.method == 'GET':
        # 获取明细
        purchase_items = get_purchase_items_rows(purchase_id=purchase_id)
        # 表单赋值
        form.uid.data = purchase_info.uid
        form.supplier_cid.data = purchase_info.supplier_cid
        form.supplier_contact_id.data = purchase_info.supplier_contact_id
        form.type_tax.data = purchase_info.type_tax
        form.warehouse_id.data = purchase_info.warehouse_id
        form.amount_purchase.data = purchase_info.amount_purchase
        # form.buyer_order_items = buyer_order_items
        while len(form.purchase_items) > 0:
            form.purchase_items.pop_entry()
        for purchase_item in purchase_items:
            purchase_item_form = PurchaseItemsEditForm()
            purchase_item_form.id = purchase_item.id
            purchase_item_form.purchase_id = purchase_item.purchase_id
            purchase_item_form.uid = purchase_item.uid
            purchase_item_form.production_id = purchase_item.production_id
            purchase_item_form.production_brand = purchase_item.production_brand
            purchase_item_form.production_model = purchase_item.production_model
            purchase_item_form.production_sku = purchase_item.production_sku
            purchase_item_form.quantity = purchase_item.quantity
            purchase_item_form.unit_price = purchase_item.unit_price
            purchase_item_form.rack_id = purchase_item.rack_id
            purchase_item_form.note = purchase_item.note
            purchase_item_form.type_tax = purchase_item.type_tax
            form.purchase_items.append_entry(purchase_item_form)

        # 内嵌表单货架选项
        for item_form in form.purchase_items:
            item_form.rack_id.choices = get_rack_choices(form.warehouse_id.data, option_type='update')
        # 渲染页面
        return render_template(
            template_name,
            purchase_id=purchase_id,
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
            if form.purchase_items.max_entries and len(
                    form.purchase_items.entries) >= form.purchase_items.max_entries:
                flash('最多创建%s条记录' % form.purchase_items.max_entries, 'danger')
            else:
                form.purchase_items.append_entry()
                # 内嵌表单货架选项
                for item_form in form.purchase_items:
                    item_form.rack_id.choices = get_rack_choices(form.warehouse_id.data, option_type='update')

            return render_template(
                template_name,
                purchase_id=purchase_id,
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
                purchase_id=purchase_id,
                form=form,
                **document_info
            )

        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Edit Failure'), 'danger')
            # flash(form.errors, 'danger')
            # flash(form.purchase_items.errors, 'danger')
            return render_template(
                template_name,
                purchase_id=purchase_id,
                form=form,
                **document_info
            )
        # 表单校验成功

        # 获取明细
        purchase_items = get_purchase_items_rows(purchase_id=purchase_id)
        purchase_items_ids = [item.id for item in purchase_items]

        # 数据新增、数据删除、数据修改

        purchase_items_ids_new = []
        amount_purchase = 0
        for purchase_item in form.purchase_items.entries:
            # 错误
            if purchase_item.form.id.data and purchase_item.form.id.data not in purchase_items_ids:
                continue

            purchase_item_data = {
                'purchase_id': purchase_id,
                'uid': form.uid.data,
                'supplier_cid': form.supplier_cid.data,
                'supplier_company_name': get_supplier_row_by_id(form.supplier_cid.data).company_name,
                'production_id': purchase_item.form.production_id.data,
                'production_brand': purchase_item.form.production_brand.data,
                'production_model': purchase_item.form.production_model.data,
                'production_sku': purchase_item.form.production_sku.data,
                'quantity': purchase_item.form.quantity.data,
                'unit_price': purchase_item.form.unit_price.data,
                'warehouse_id': form.warehouse_id.data,
                'rack_id': purchase_item.form.rack_id.data,
                'note': purchase_item.form.note.data,
                'type_tax': form.type_tax.data,
            }

            if not purchase_item.form.id.data:
                # 新增
                add_purchase_items(purchase_item_data)
                amount_purchase += purchase_item_data['quantity'] * purchase_item_data['unit_price']
            else:
                # 修改
                edit_purchase_items(purchase_item.form.id.data, purchase_item_data)
                amount_purchase += purchase_item_data['quantity'] * purchase_item_data['unit_price']
                purchase_items_ids_new.append(purchase_item.form.id.data)
        # 删除
        purchase_items_ids_del = list(set(purchase_items_ids) - set(purchase_items_ids_new))
        for purchase_items_id in purchase_items_ids_del:
            delete_purchase_items(purchase_items_id)

        # 更新销售出货
        current_time = datetime.utcnow()
        purchase_data = {
            'uid': form.uid.data,
            'supplier_cid': form.supplier_cid.data,
            'supplier_contact_id': form.supplier_contact_id.data,
            'type_tax': form.type_tax.data,
            'amount_production': amount_purchase,
            'amount_purchase': amount_purchase,
            'warehouse_id': form.warehouse_id.data,
            'update_time': current_time,
        }
        result = edit_purchase(purchase_id, purchase_data)

        # 编辑操作成功
        if result:
            flash(_('Edit Success'), 'success')
            return redirect(request.args.get('next') or url_for('purchase.lists'))
        # 编辑操作失败
        else:
            flash(_('Edit Failure'), 'danger')
            return render_template(
                template_name,
                purchase_id=purchase_id,
                form=form,
                **document_info
            )


@bp_purchase.route('/<int:purchase_id>/info.html')
@login_required
@permission_purchase_section_get.require(http_exception=403)
def info(purchase_id):
    """
    出货详情
    :param purchase_id:
    :return:
    """
    purchase_info = get_purchase_row_by_id(purchase_id)
    # 检查资源是否存在
    if not purchase_info:
        abort(404)
    # 检查资源是否删除
    if purchase_info.status_delete == STATUS_DEL_OK:
        abort(410)

    purchase_print_date = time_utc_to_local(purchase_info.update_time).strftime('%Y-%m-%d')
    purchase_code = '%s%s' % (g.ENQUIRIES_PREFIX, time_utc_to_local(purchase_info.create_time).strftime('%y%m%d%H%M%S'))

    # 获取渠道公司信息
    supplier_info = get_supplier_row_by_id(purchase_info.supplier_cid)

    # 获取渠道联系方式
    supplier_contact_info = get_supplier_contact_row_by_id(purchase_info.supplier_contact_id)

    # 获取进货人员信息
    user_info = get_user_row_by_id(purchase_info.uid)

    purchase_items = get_purchase_items_rows(purchase_id=purchase_id)

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('purchase info')

    template_name = 'purchase/info.html'

    return render_template(
        template_name,
        purchase_id=purchase_id,
        purchase_info=purchase_info,
        supplier_info=supplier_info,
        supplier_contact_info=supplier_contact_info,
        user_info=user_info,
        purchase_items=purchase_items,
        purchase_print_date=purchase_print_date,
        purchase_code=purchase_code,
        **document_info
    )


@bp_purchase.route('/<int:purchase_id>/preview.html')
@login_required
@permission_purchase_section_print.require(http_exception=403)
def preview(purchase_id):
    """
    打印预览
    :param purchase_id:
    :return:
    """
    purchase_info = get_purchase_row_by_id(purchase_id)
    # 检查资源是否存在
    if not purchase_info:
        abort(404)
    # 检查资源是否删除
    if purchase_info.status_delete == STATUS_DEL_OK:
        abort(410)

    purchase_print_date = time_utc_to_local(purchase_info.update_time).strftime('%Y-%m-%d')
    purchase_code = '%s%s' % (g.ENQUIRIES_PREFIX, time_utc_to_local(purchase_info.create_time).strftime('%y%m%d%H%M%S'))

    # 获取渠道公司信息
    supplier_info = get_supplier_row_by_id(purchase_info.supplier_cid)

    # 获取渠道联系方式
    supplier_contact_info = get_supplier_contact_row_by_id(purchase_info.supplier_contact_id)

    # 获取进货人员信息
    user_info = get_user_row_by_id(purchase_info.uid)

    purchase_items = get_purchase_items_rows(purchase_id=purchase_id)

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('purchase preview')

    template_name = 'purchase/preview.html'

    return render_template(
        template_name,
        purchase_id=purchase_id,
        purchase_info=purchase_info,
        supplier_info=supplier_info,
        supplier_contact_info=supplier_contact_info,
        user_info=user_info,
        purchase_items=purchase_items,
        purchase_print_date=purchase_print_date,
        purchase_code=purchase_code,
        **document_info
    )


@bp_purchase.route('/<int:purchase_id>.pdf')
@login_required
@permission_purchase_section_print.require(http_exception=403)
def pdf(purchase_id):
    """
    文件下载
    :param purchase_id:
    :return:
    """
    purchase_info = get_purchase_row_by_id(purchase_id)
    # 检查资源是否存在
    if not purchase_info:
        abort(404)
    # 检查资源是否删除
    if purchase_info.status_delete == STATUS_DEL_OK:
        abort(410)

    purchase_print_date = time_utc_to_local(purchase_info.update_time).strftime('%Y-%m-%d')
    purchase_code = '%s%s' % (g.ENQUIRIES_PREFIX, time_utc_to_local(purchase_info.create_time).strftime('%y%m%d%H%M%S'))

    # 获取渠道公司信息
    supplier_info = get_supplier_row_by_id(purchase_info.supplier_cid)

    # 获取渠道联系方式
    supplier_contact_info = get_supplier_contact_row_by_id(purchase_info.supplier_contact_id)

    # 获取进货人员信息
    user_info = get_user_row_by_id(purchase_info.uid)

    purchase_items = get_purchase_items_rows(purchase_id=purchase_id)

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('purchase pdf')

    template_name = 'purchase/pdf.html'

    html = render_template(
        template_name,
        purchase_id=purchase_id,
        purchase_info=purchase_info,
        supplier_info=supplier_info,
        supplier_contact_info=supplier_contact_info,
        user_info=user_info,
        purchase_items=purchase_items,
        purchase_print_date=purchase_print_date,
        purchase_code=purchase_code,
        **document_info
    )
    # return html
    return render_pdf(
        html=HTML(string=html),
        stylesheets=[CSS(string='@page {size:A4; margin:35px;}')],
        download_filename='销售出货.pdf'.encode('utf-8')
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

    # 检查删除权限
    if not permission_purchase_section_del.can():
        ext_msg = _('Permission Denied')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

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


@bp_purchase.route('/ajax/audit', methods=['GET', 'POST'])
@login_required
def ajax_audit():
    """
    销售进货审核
    :return:
    """
    ajax_success_msg = AJAX_SUCCESS_MSG.copy()
    ajax_failure_msg = AJAX_FAILURE_MSG.copy()

    # 检查审核权限
    if not permission_purchase_section_audit.can():
        ext_msg = _('Permission Denied')
        ajax_failure_msg['msg'] = _('Audit Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查请求方法
    if not (request.method == 'GET' and request.is_xhr):
        ext_msg = _('Method Not Allowed')
        ajax_failure_msg['msg'] = _('Audit Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查请求参数
    purchase_id = request.args.get('purchase_id', 0, type=int)
    audit_status = request.args.get('audit_status', 0, type=int)
    if not purchase_id:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Audit Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)
    if audit_status not in [STATUS_AUDIT_NO, STATUS_AUDIT_OK]:
        ext_msg = _('Status not exist')
        ajax_failure_msg['msg'] = _('Audit Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    purchase_info = get_purchase_row_by_id(purchase_id)
    # 检查资源是否存在
    if not purchase_info:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Audit Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)
    # 检查资源是否删除
    if purchase_info.status_delete == STATUS_DEL_OK:
        ext_msg = _('Already deleted')
        ajax_failure_msg['msg'] = _('Audit Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)
    # 检查审核状态是否变化
    if purchase_info.status_audit == audit_status:
        ext_msg = _('Already audited')
        ajax_failure_msg['msg'] = _('Audit Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    try:
        if audit_status == STATUS_AUDIT_OK:
            result = audit_purchase(purchase_id)
        else:
            result = cancel_audit_purchase(purchase_id)
        if result:
            ajax_success_msg['msg'] = _('Audit Success')
            return jsonify(ajax_success_msg)
        else:
            ajax_failure_msg['msg'] = _('Audit Failure')
            return jsonify(ajax_failure_msg)
    except Exception as e:
        ajax_failure_msg['msg'] = e.message
        return jsonify(ajax_failure_msg)
