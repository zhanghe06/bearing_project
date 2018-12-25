#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: quotation.py
@time: 2018-03-16 09:59
"""

from __future__ import unicode_literals

import json
from datetime import datetime, timedelta

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

from app_backend.api.catalogue import get_catalogue_choices
from app_backend.api.customer import get_customer_choices, get_customer_row_by_id
from app_backend.api.customer_contact import get_customer_contact_row_by_id
from app_backend.api.user import get_user_choices, get_user_row_by_id
from app_backend.forms.production import ProductionSelectForm
from app_backend.forms.quotation import QuotationItemEditForm
from app_backend import (
    app,
    excel,
)
from app_backend.api.quotation import (
    get_quotation_pagination,
    get_quotation_row_by_id,
    add_quotation,
    edit_quotation,
    get_quotation_rows,
    get_distinct_quotation_uid,
    get_distinct_quotation_cid,
    quotation_total_stats,
    quotation_order_stats,
    get_quotation_user_list_choices, get_quotation_customer_list_choices)

from app_backend.api.quotation_items import get_quotation_items_rows, add_quotation_items, edit_quotation_items, \
    delete_quotation_items
from wtforms.fields import FieldList, FormField
from app_backend.forms.quotation import (
    QuotationSearchForm,
    QuotationAddForm,
    QuotationEditForm,
)
from app_backend.models.bearing_project import Quotation
from app_backend.permissions import (
    permission_quotation_section_add,
    permission_quotation_section_search,
    permission_quotation_section_export,
    permission_quotation_section_stats,
    QuotationItemGetPermission,
    QuotationItemEditPermission,
    QuotationItemDelPermission,
)
from app_backend.signals.quotation import signal_quotation_status_delete
from app_common.maps.default import default_choices_int, default_choice_option_int
from app_common.maps.status_delete import (
    STATUS_DEL_OK,
    STATUS_DEL_NO)
from app_common.maps.status_order import STATUS_ORDER_CHOICES
from app_common.maps.type_role import (
    TYPE_ROLE_SALES,
)
from app_common.tools import json_default

# 定义蓝图
from app_common.tools.date_time import time_utc_to_local

bp_quotation = Blueprint('quotation', __name__, url_prefix='/quotation')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


@bp_quotation.route('/lists.html', methods=['GET', 'POST'])
@login_required
@permission_quotation_section_search.require(http_exception=403)
def lists():
    """
    报价列表
    :return:
    """
    template_name = 'quotation/lists.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('quotation lists')

    # 搜索条件
    form = QuotationSearchForm(request.form)
    form.uid.choices = get_quotation_user_list_choices()
    # app.logger.info('')

    search_condition = [
        Quotation.status_delete == STATUS_DEL_NO,
    ]
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Search Failure'), 'danger')
            # 单独处理csrf_token
            if hasattr(form, 'csrf_token') and getattr(form, 'csrf_token').errors:
                map(lambda x: flash(x, 'danger'), form.csrf_token.errors)
        else:
            if form.uid.data != default_choice_option_int:
                search_condition.append(Quotation.uid == form.uid.data)
            if form.customer_cid.data and form.customer_company_name.data:
                search_condition.append(Quotation.cid == form.customer_cid.data)
            if form.start_create_time.data:
                search_condition.append(Quotation.create_time >= form.start_create_time.data)
            if form.end_create_time.data:
                search_condition.append(Quotation.create_time <= form.end_create_time.data)
        # 处理导出
        if form.op.data == 1:
            # 检查导出权限
            if not permission_quotation_section_export.can():
                abort(403)
            column_names = Quotation.__table__.columns.keys()
            query_sets = get_quotation_rows(*search_condition)

            return excel.make_response_from_query_sets(
                query_sets=query_sets,
                column_names=column_names,
                file_type='csv',
                file_name='%s.csv' % _('quotation lists')
            )
        # 批量删除
        if form.op.data == 2:
            quotation_ids = request.form.getlist('quotation_id')
            # 检查删除权限
            permitted = True
            for quotation_id in quotation_ids:
                quotation_item_del_permission = QuotationItemDelPermission(quotation_id)
                if not quotation_item_del_permission.can():
                    ext_msg = _('Permission Denied')
                    flash(_('Del Failure, %(ext_msg)s', ext_msg=ext_msg), 'danger')
                    permitted = False
                    break
            if permitted:
                result_total = True
                for quotation_id in quotation_ids:
                    current_time = datetime.utcnow()
                    quotation_data = {
                        'status_delete': STATUS_DEL_OK,
                        'delete_time': current_time,
                        'update_time': current_time,
                    }
                    result = edit_quotation(quotation_id, quotation_data)
                    if result:
                        # 发送删除信号
                        signal_data = {
                            'quotation_id': quotation_id,
                            'status_delete': STATUS_DEL_OK,
                            'current_time': current_time,
                        }
                        signal_quotation_status_delete.send(app, **signal_data)
                    result_total = result_total and result
                if result_total:
                    flash(_('Del Success'), 'success')
                else:
                    flash(_('Del Failure'), 'danger')
    # 翻页数据
    pagination = get_quotation_pagination(form.page.data, PER_PAGE_BACKEND, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )


@bp_quotation.route('/<int:quotation_id>/info.html')
@login_required
def info(quotation_id):
    """
    报价详情
    :param quotation_id:
    :return:
    """
    # 检查读取权限
    quotation_item_get_permission = QuotationItemGetPermission(quotation_id)
    if not quotation_item_get_permission.can():
        abort(403)
    # 详情数据
    quotation_info = get_quotation_row_by_id(quotation_id)
    # 检查资源是否存在
    if not quotation_info:
        abort(404)
    # 检查资源是否删除
    if quotation_info.status_delete == STATUS_DEL_OK:
        abort(410)

    # 公司信息
    company_info = get_customer_row_by_id(quotation_info.cid)

    template_name = 'quotation/info.html'

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('quotation info')

    # 获取明细
    quotation_items = get_quotation_items_rows(quotation_id=quotation_id)

    # 渲染模板
    return render_template(
        template_name,
        quotation_info=quotation_info,
        quotation_items=quotation_items,
        company_info=company_info,
        **document_info
    )


@bp_quotation.route('/add.html', methods=['GET', 'POST'])
@login_required
@permission_quotation_section_add.require(http_exception=403)
def add():
    """
    创建报价
    :return:
    """
    template_name = 'quotation/add.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('quotation add')

    # 加载创建表单
    form = QuotationAddForm(request.form)
    form.uid.choices = get_user_choices()
    form.uid.data = current_user.id
    # form.contact_id.choices = default_choices_int
    form.status_order.choices = STATUS_ORDER_CHOICES

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
            if form.quotation_items.max_entries and len(
                    form.quotation_items.entries) >= form.quotation_items.max_entries:
                flash('最多创建%s条记录' % form.quotation_items.max_entries, 'danger')
            else:
                form.quotation_items.append_entry()

            return render_template(
                template_name,
                form=form,
                **document_info
            )
        # 表单删除一行
        if form.data_line_del.data is not None:
            if form.quotation_items.min_entries and len(
                    form.quotation_items.entries) <= form.quotation_items.min_entries:
                flash('最少保留%s条记录' % form.quotation_items.min_entries, 'danger')
            else:
                data_line_index = form.data_line_del.data
                form.quotation_items.entries.pop(data_line_index)

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

        # 创建报价
        current_time = datetime.utcnow()
        quotation_data = {
            'uid': form.uid.data,
            'cid': form.cid.data,
            'contact_id': form.contact_id.data,
            'delivery_way': form.delivery_way.data,
            'note': form.note.data,
            'status_order': form.status_order.data,
            'expiry_date': (datetime.utcnow() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'create_time': current_time,
            'update_time': current_time,
        }
        quotation_id = add_quotation(quotation_data)

        amount_quotation = 0
        for quotation_item in form.quotation_items.entries:
            current_time = datetime.utcnow()
            quotation_item_data = {
                'quotation_id': quotation_id,
                'uid': form.uid.data,
                'enquiry_cid': form.cid.data,
                'enquiry_company_name': get_customer_row_by_id(form.cid.data).company_name,
                'enquiry_production_model': quotation_item.form.enquiry_production_model.data,
                'enquiry_quantity': quotation_item.form.enquiry_quantity.data,
                'production_id': quotation_item.form.production_id.data,
                'production_brand': quotation_item.form.production_brand.data,
                'production_model': quotation_item.form.production_model.data,
                'production_sku': quotation_item.form.production_sku.data,
                'note': quotation_item.form.note.data,
                'delivery_time': quotation_item.form.delivery_time.data,
                'quantity': quotation_item.form.quantity.data,
                'unit_price': quotation_item.form.unit_price.data,
                'status_ordered': quotation_item.form.status_ordered.data,
                'create_time': current_time,
                'update_time': current_time,
            }

            # 新增
            add_quotation_items(quotation_item_data)
            amount_quotation += (quotation_item_data['quantity'] or 0) * (quotation_item_data['unit_price'] or 0)

        # 更新报价
        quotation_data = {
            'amount_production': amount_quotation,
            'amount_quotation': amount_quotation,
            'update_time': current_time,
        }
        result = edit_quotation(quotation_id, quotation_data)

        # todo 事务

        # 明细保存
        # 总表保存

        # 创建操作成功
        if result:
            flash(_('Add Success'), 'success')
            return redirect(request.args.get('next') or url_for('quotation.lists'))
        # 创建操作失败
        else:
            flash(_('Add Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                **document_info
            )


@bp_quotation.route('/<int:quotation_id>/edit.html', methods=['GET', 'POST'])
@login_required
def edit(quotation_id):
    """
    报价编辑
    """
    # 检查编辑权限
    # quotation_item_edit_permission = QuotationItemEditPermission(quotation_id)
    # if not quotation_item_edit_permission.can():
    #     abort(403)

    quotation_info = get_quotation_row_by_id(quotation_id)
    # 检查资源是否存在
    if not quotation_info:
        abort(404)
    # 检查资源是否删除
    if quotation_info.status_delete == STATUS_DEL_OK:
        abort(410)

    template_name = 'quotation/edit.html'

    # 加载编辑表单
    form = QuotationEditForm(request.form)
    form.uid.choices = get_user_choices()
    form.status_order.choices = STATUS_ORDER_CHOICES

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('quotation edit')

    # 进入编辑页面
    if request.method == 'GET':
        # 获取明细
        quotation_items = get_quotation_items_rows(quotation_id=quotation_id)
        # 表单赋值
        form.uid.data = quotation_info.uid
        form.cid.data = quotation_info.cid
        form.contact_id.data = quotation_info.contact_id
        form.delivery_way.data = quotation_info.delivery_way
        form.note.data = quotation_info.note
        form.status_order.data = quotation_info.status_order
        form.amount_quotation.data = quotation_info.amount_quotation
        # form.quotation_items = quotation_items
        while len(form.quotation_items) > 0:
            form.quotation_items.pop_entry()
        for quotation_item in quotation_items:
            quotation_item_form = QuotationItemEditForm()
            quotation_item_form.id = quotation_item.id
            quotation_item_form.quotation_id = quotation_item.quotation_id
            quotation_item_form.uid = quotation_item.uid
            quotation_item_form.enquiry_production_model = quotation_item.enquiry_production_model
            quotation_item_form.enquiry_quantity = quotation_item.enquiry_quantity
            quotation_item_form.production_id = quotation_item.production_id
            quotation_item_form.production_brand = quotation_item.production_brand
            quotation_item_form.production_model = quotation_item.production_model
            quotation_item_form.production_sku = quotation_item.production_sku
            quotation_item_form.note = quotation_item.note
            quotation_item_form.quantity = quotation_item.quantity
            quotation_item_form.unit_price = quotation_item.unit_price
            quotation_item_form.delivery_time = quotation_item.delivery_time
            quotation_item_form.status_ordered = quotation_item.status_ordered
            form.quotation_items.append_entry(quotation_item_form)
        # 渲染页面
        return render_template(
            template_name,
            quotation_id=quotation_id,
            form=form,
            **document_info
        )

    # 处理编辑请求
    if request.method == 'POST':
        # 增删数据行不需要校验表单

        # 表单新增空行
        if form.data_line_add.data is not None:
            if form.quotation_items.max_entries and len(
                    form.quotation_items.entries) >= form.quotation_items.max_entries:
                flash('最多创建%s条记录' % form.quotation_items.max_entries, 'danger')
            else:
                form.quotation_items.append_entry()

            return render_template(
                template_name,
                quotation_id=quotation_id,
                form=form,
                **document_info
            )
        # 表单删除一行
        if form.data_line_del.data is not None:
            if form.quotation_items.min_entries and len(
                    form.quotation_items.entries) <= form.quotation_items.min_entries:
                flash('最少保留%s条记录' % form.quotation_items.min_entries, 'danger')
            else:
                data_line_index = form.data_line_del.data
                form.quotation_items.entries.pop(data_line_index)

            return render_template(
                template_name,
                quotation_id=quotation_id,
                form=form,
                **document_info
            )

        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Edit Failure'), 'danger')
            # flash(form.errors, 'danger')
            # flash(form.quotation_items.errors, 'danger')
            return render_template(
                template_name,
                quotation_id=quotation_id,
                form=form,
                **document_info
            )
        # 表单校验成功

        # 获取明细
        quotation_items = get_quotation_items_rows(quotation_id=quotation_id)
        quotation_items_ids = [item.id for item in quotation_items]

        # 数据新增、数据删除、数据修改

        quotation_items_ids_new = []
        amount_quotation = 0
        for quotation_item in form.quotation_items.entries:
            # 错误
            if quotation_item.form.id.data and quotation_item.form.id.data not in quotation_items_ids:
                continue

            quotation_item_data = {
                'quotation_id': quotation_id,
                'uid': form.uid.data,
                'enquiry_cid': form.cid.data,
                'enquiry_company_name': get_customer_row_by_id(form.cid.data).company_name,
                'enquiry_production_model': quotation_item.form.enquiry_production_model.data,
                'enquiry_quantity': quotation_item.form.enquiry_quantity.data,
                'production_id': quotation_item.form.production_id.data,
                'production_brand': quotation_item.form.production_brand.data,
                'production_model': quotation_item.form.production_model.data,
                'production_sku': quotation_item.form.production_sku.data,
                'note': quotation_item.form.note.data,
                'delivery_time': quotation_item.form.delivery_time.data,
                'quantity': quotation_item.form.quantity.data,
                'unit_price': quotation_item.form.unit_price.data,
                'status_ordered': quotation_item.form.status_ordered.data,
            }

            if not quotation_item.form.id.data:
                # 新增
                add_quotation_items(quotation_item_data)
                amount_quotation += quotation_item_data['quantity'] * quotation_item_data['unit_price']
            else:
                # 修改
                edit_quotation_items(quotation_item.form.id.data, quotation_item_data)
                amount_quotation += quotation_item_data['quantity'] * quotation_item_data['unit_price']
                quotation_items_ids_new.append(quotation_item.form.id.data)
        # 删除
        quotation_items_ids_del = list(set(quotation_items_ids) - set(quotation_items_ids_new))
        for quotation_items_id in quotation_items_ids_del:
            delete_quotation_items(quotation_items_id)

        # 更新报价
        current_time = datetime.utcnow()
        quotation_data = {
            'cid': form.cid.data,
            'uid': form.uid.data,
            'contact_id': form.contact_id.data,
            'delivery_way': form.delivery_way.data,
            'note': form.note.data,
            'status_order': form.status_order.data,
            'amount_production': amount_quotation,
            'amount_quotation': amount_quotation,
            'update_time': current_time,
        }
        result = edit_quotation(quotation_id, quotation_data)

        # 编辑操作成功
        if result:
            flash(_('Edit Success'), 'success')
            return redirect(request.args.get('next') or url_for('quotation.lists'))
        # 编辑操作失败
        else:
            flash(_('Edit Failure'), 'danger')
            return render_template(
                template_name,
                quotation_id=quotation_id,
                form=form,
                **document_info
            )


@bp_quotation.route('/<int:quotation_id>/preview.html')
@login_required
def preview(quotation_id):
    """
    打印预览
    :param quotation_id:
    :return:
    """
    quotation_info = get_quotation_row_by_id(quotation_id)
    # 检查资源是否存在
    if not quotation_info:
        abort(404)
    # 检查资源是否删除
    if quotation_info.status_delete == STATUS_DEL_OK:
        abort(410)

    quotation_print_date = time_utc_to_local(quotation_info.update_time).strftime('%Y-%m-%d')
    quotation_code = '%s%s' % (g.QUOTATION_PREFIX, time_utc_to_local(quotation_info.create_time).strftime('%y%m%d%H%M%S'))

    # 获取客户公司信息
    customer_info = get_customer_row_by_id(quotation_info.cid)

    # 获取客户联系方式
    customer_contact_info = get_customer_contact_row_by_id(quotation_info.contact_id)

    # 获取报价人员信息
    user_info = get_user_row_by_id(quotation_info.uid)

    quotation_items = get_quotation_items_rows(quotation_id=quotation_id)

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('quotation edit')

    template_name = 'quotation/preview.html'

    return render_template(
        template_name,
        quotation_id=quotation_id,
        quotation_info=quotation_info,
        customer_info=customer_info,
        customer_contact_info=customer_contact_info,
        user_info=user_info,
        quotation_items=quotation_items,
        quotation_print_date=quotation_print_date,
        quotation_code=quotation_code,
        **document_info
    )


@bp_quotation.route('/<int:quotation_id>.pdf')
@login_required
def pdf(quotation_id):
    """
    文件下载
    :param quotation_id:
    :return:
    """
    quotation_info = get_quotation_row_by_id(quotation_id)
    # 检查资源是否存在
    if not quotation_info:
        abort(404)
    # 检查资源是否删除
    if quotation_info.status_delete == STATUS_DEL_OK:
        abort(410)

    quotation_print_date = time_utc_to_local(quotation_info.update_time).strftime('%Y-%m-%d')
    quotation_code = '%s%s' % (g.QUOTATION_PREFIX, time_utc_to_local(quotation_info.create_time).strftime('%y%m%d%H%M%S'))

    # 获取客户公司信息
    customer_info = get_customer_row_by_id(quotation_info.cid)

    # 获取客户联系方式
    customer_contact_info = get_customer_contact_row_by_id(quotation_info.contact_id)

    # 获取报价人员信息
    user_info = get_user_row_by_id(quotation_info.uid)

    quotation_items = get_quotation_items_rows(quotation_id=quotation_id)

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('quotation edit')

    template_name = 'quotation/pdf.html'

    html = render_template(
        template_name,
        quotation_id=quotation_id,
        quotation_info=quotation_info,
        customer_info=customer_info,
        customer_contact_info=customer_contact_info,
        user_info=user_info,
        quotation_items=quotation_items,
        quotation_print_date=quotation_print_date,
        quotation_code=quotation_code,
        **document_info
    )
    # return html
    return render_pdf(
        html=HTML(string=html),
        stylesheets=[CSS(string='@page {size:A4; margin:35px;}')],
        download_filename='报价单.pdf'.encode('utf-8')
    )


@bp_quotation.route('/ajax/del', methods=['GET', 'POST'])
@login_required
def ajax_delete():
    """
    报价删除
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
    quotation_id = request.args.get('quotation_id', 0, type=int)
    if not quotation_id:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查删除权限
    quotation_item_del_permission = QuotationItemDelPermission(quotation_id)
    if not quotation_item_del_permission.can():
        ext_msg = _('Permission Denied')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    quotation_info = get_quotation_row_by_id(quotation_id)
    # 检查资源是否存在
    if not quotation_info:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)
    # 检查资源是否删除
    if quotation_info.status_delete == STATUS_DEL_OK:
        ext_msg = _('Already deleted')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_success_msg)

    current_time = datetime.utcnow()
    quotation_data = {
        'status_delete': STATUS_DEL_OK,
        'delete_time': current_time,
        'update_time': current_time,
    }
    result = edit_quotation(quotation_id, quotation_data)
    if result:
        # 发送删除信号
        signal_data = {
            'quotation_id': quotation_id,
            'status_delete': STATUS_DEL_OK,
            'current_time': current_time,
        }
        signal_quotation_status_delete.send(app, **signal_data)

        ajax_success_msg['msg'] = _('Del Success')
        return jsonify(ajax_success_msg)
    else:
        ajax_failure_msg['msg'] = _('Del Failure')
        return jsonify(ajax_failure_msg)


# @bp_quotation.route('/ajax/stats', methods=['GET', 'POST'])
# @login_required
# def ajax_stats():
#     """
#     获取报价统计
#     :return:
#     """
#     time_based = request.args.get('time_based', 'hour')
#     result_quotation_middleman = quotation_middleman_stats(time_based)
#     result_quotation_end_user = quotation_end_user_stats(time_based)
#
#     line_chart_data = {
#         'labels': [label for label, _ in result_quotation_middleman],
#         'datasets': [
#             {
#                 'label': '同行',
#                 'backgroundColor': 'rgba(220,220,220,0.5)',
#                 'borderColor': 'rgba(220,220,220,1)',
#                 'pointBackgroundColor': 'rgba(220,220,220,1)',
#                 'pointBorderColor': '#fff',
#                 'pointBorderWidth': 2,
#                 'data': [data for _, data in result_quotation_middleman]
#             },
#             {
#                 'label': '终端',
#                 'backgroundColor': 'rgba(151,187,205,0.5)',
#                 'borderColor': 'rgba(151,187,205,1)',
#                 'pointBackgroundColor': 'rgba(151,187,205,1)',
#                 'pointBorderColor': '#fff',
#                 'pointBorderWidth': 2,
#                 'data': [data for _, data in result_quotation_end_user]
#             }
#         ]
#     }
#     return json.dumps(line_chart_data, default=json_default)


@bp_quotation.route('/stats.html')
@login_required
@permission_quotation_section_stats.require(http_exception=403)
def stats():
    """
    报价统计
    :return:
    """
    # 统计数据
    time_based = request.args.get('time_based', 'hour')
    if time_based not in ['hour', 'date', 'month']:
        abort(404)
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('quotation stats')
    # 渲染模板
    return render_template(
        'quotation/stats.html',
        time_based=time_based,
        **document_info
    )


@bp_quotation.route('/<int:quotation_id>/stats.html')
@login_required
@permission_quotation_section_stats.require(http_exception=403)
def stats_item(quotation_id):
    """
    报价统计明细
    :param quotation_id:
    :return:
    """
    quotation_info = get_quotation_row_by_id(quotation_id)
    # 检查资源是否存在
    if not quotation_info:
        abort(404)
    # 检查资源是否删除
    if quotation_info.status_delete == STATUS_DEL_OK:
        abort(410)

    # 统计数据
    quotation_stats_item_info = get_quotation_row_by_id(quotation_id)
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('quotation stats item')
    # 渲染模板
    return render_template(
        'quotation/stats_item.html',
        quotation_stats_item_info=quotation_stats_item_info,
        **document_info
    )
