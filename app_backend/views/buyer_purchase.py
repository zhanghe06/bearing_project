#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: buyer_purchase.py
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

# 定义蓝图
from app_backend.api.purchase import add_purchase
from app_backend.api.user import get_user_choices
from app_backend.forms.purchase import PurchaseAddForm
from app_common.maps.status_order import STATUS_ORDER_CHOICES

bp_buyer_purchase = Blueprint('buyer_purchase', __name__, url_prefix='/buyer/purchase')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


@bp_buyer_purchase.route('/lists.html', methods=['GET', 'POST'])
@bp_buyer_purchase.route('/lists/<int:page>.html', methods=['GET', 'POST'])
@login_required
def lists(page=1):
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
            if form.cid.data and form.company_name.data:
                search_condition.append(Quotation.cid == form.cid.data)
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


@bp_buyer_purchase.route('/add.html', methods=['GET', 'POST'])
@login_required
def add():
    """
    采购入库
    :return:
    """
    # return jsonify({})
    template_name = 'buyer/purchase/add.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('buyer purchase add')

    # 加载创建表单
    form = PurchaseAddForm(request.form)
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

        # 创建采购入库
        current_time = datetime.utcnow()
        purchase_data = {
            'uid': form.uid.data,
            'cid': form.cid.data,
            'contact_id': form.contact_id.data,
            'status_order': form.status_order.data,
            'expiry_date': (datetime.utcnow() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'create_time': current_time,
            'update_time': current_time,
        }
        purchase_id = add_purchase(purchase_data)

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
            add_quotation_item(quotation_item_data)
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
