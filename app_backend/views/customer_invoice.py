#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: customer_invoice.py
@time: 2018-07-17 14:51
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

from app_backend.api.customer import get_customer_row_by_id
from app_backend.api.customer_invoice import get_customer_invoice_rows, get_customer_invoice_pagination, \
    get_customer_invoice_row_by_id, edit_customer_invoice, add_customer_invoice
from app_backend.models.bearing_project import CustomerInvoice

from app_backend.forms.customer_invoice import (
    CustomerInvoiceSearchForm,
    # CustomerInvoiceAddForm,
    # CustomerInvoiceEditForm,
    # CustomerInvoiceItemEditForm,
    CustomerInvoiceEditForm)

from app_backend import (
    app,
    excel,
)

# 定义蓝图
from app_backend.permissions import permission_customer_section_export, CustomerItemDelPermission
from app_common.maps.status_delete import STATUS_DEL_NO, STATUS_DEL_OK

bp_customer_invoice = Blueprint('customer_invoice', __name__, url_prefix='/customer/invoice')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


@bp_customer_invoice.route('/lists.html', methods=['GET', 'POST'])
@bp_customer_invoice.route('/lists/<int:page>.html', methods=['GET', 'POST'])
@login_required
def lists(page=1):
    template_name = 'customer/invoice/lists.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('customer invoice lists')

    # 搜索条件
    form = CustomerInvoiceSearchForm(request.form)
    # app.logger.info('')

    search_condition = [
        CustomerInvoice.status_delete == STATUS_DEL_NO,
    ]
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Search Failure'), 'danger')
            # 单独处理csrf_token
            if hasattr(form, 'csrf_token') and getattr(form, 'csrf_token').errors:
                map(lambda x: flash(x, 'danger'), form.csrf_token.errors)
        else:
            if form.cid.data and form.company_name.data:
                search_condition.append(CustomerInvoice.cid == form.cid.data)
            if form.company_tax_id.data:
                search_condition.append(CustomerInvoice.contact_name == form.company_tax_id.data)
        # 处理导出
        if form.op.data == 1:
            # 检查导出权限
            if not permission_customer_section_export.can():
                abort(403)
            column_names = CustomerInvoice.__table__.columns.keys()
            query_sets = get_customer_invoice_rows(*search_condition)

            return excel.make_response_from_query_sets(
                query_sets=query_sets,
                column_names=column_names,
                file_type='csv',
                file_name='%s.csv' % _('customer invoice lists')
            )
    # 翻页数据
    pagination = get_customer_invoice_pagination(page, PER_PAGE_BACKEND, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )


@bp_customer_invoice.route('/add.html', methods=['GET', 'POST'])
@login_required
def add():
    return jsonify({})


@bp_customer_invoice.route('/<int:customer_id>.html', methods=['GET', 'POST'])
@login_required
def edit(customer_id):
    """
    客户开票资料编辑
    """
    # 检查编辑权限
    # customer_item_edit_permission = CustomerItemEditPermission(customer_id)
    # if not customer_item_edit_permission.can():
    #     abort(403)

    customer_info = get_customer_row_by_id(customer_id)
    # 检查资源是否存在
    if not customer_info:
        abort(404)
    # 检查资源是否删除
    if customer_info.status_delete == STATUS_DEL_OK:
        abort(410)

    customer_invoice_info = get_customer_invoice_row_by_id(customer_id)

    template_name = 'customer/invoice/edit.html'

    # 加载编辑表单
    form = CustomerInvoiceEditForm(request.form)

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('customer invoice edit')

    # 进入编辑页面
    if request.method == 'GET':
        current_time = datetime.utcnow()
        # 表单赋值
        form.cid.data = customer_id
        form.company_name.data = getattr(customer_invoice_info, 'company_name', customer_info.company_name)
        form.company_address.data = getattr(customer_invoice_info, 'company_address', '')
        form.company_tel.data = getattr(customer_invoice_info, 'company_tel', '')
        form.company_bank_name.data = getattr(customer_invoice_info, 'company_bank_name', '')
        form.company_bank_account.data = getattr(customer_invoice_info, 'company_bank_account', '')
        form.create_time.data = getattr(customer_invoice_info, 'create_time', current_time)
        form.update_time.data = getattr(customer_invoice_info, 'update_time', current_time)
        # 渲染页面
        return render_template(
            template_name,
            customer_id=customer_id,
            form=form,
            **document_info
        )

    # 处理编辑请求
    if request.method == 'POST':
        # 表单校验失败
        if customer_id != form.cid.data or not form.validate_on_submit():
            flash(_('Edit Failure'), 'danger')
            flash(form.errors, 'danger')
            return render_template(
                template_name,
                customer_id=customer_id,
                form=form,
                **document_info
            )
        # 表单校验成功
        current_time = datetime.utcnow()
        customer_invoice_data = {
            'company_name': form.company_name.data,
            'company_tax_id': form.company_tax_id.data,
            'company_address': form.company_address.data,
            'company_tel': form.company_tel.data,
            'company_bank_name': form.company_bank_name.data,
            'company_bank_account': form.company_bank_account.data,
            'update_time': current_time,
        }
        if customer_invoice_info:
            # 修改
            result = edit_customer_invoice(customer_id, customer_invoice_data)
        else:
            # 创建
            customer_invoice_data['cid'] = customer_id
            result = add_customer_invoice(customer_invoice_data)
        # 编辑操作成功
        if result:
            flash(_('Edit Success'), 'success')
            return redirect(request.args.get('next') or url_for('customer_invoice.lists'))
        # 编辑操作失败
        else:
            flash(_('Edit Failure'), 'danger')
            return render_template(
                template_name,
                customer_id=customer_id,
                form=form,
                **document_info
            )


@bp_customer_invoice.route('/stats.html', methods=['GET', 'POST'])
@login_required
def stats():
    return jsonify({})


@bp_customer_invoice.route('/preview.html', methods=['GET', 'POST'])
@login_required
def preview():
    return jsonify({})
