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

from app_backend.forms.quotation import QuoteItemEditForm
from app_backend import (
    app,
    excel,
)
from app_backend.api.quotation import (
    get_quote_pagination,
    get_quote_row_by_id,
    add_quote,
    edit_quote,
    get_quote_rows,
    get_distinct_quote_uid,
    get_distinct_quote_cid,
    quote_total_stats,
    quote_order_stats,
    get_quote_user_list_choices, get_quote_customer_list_choices)

from app_backend.api.quotation_item import get_quote_item_rows, add_quote_item, edit_quote_item, delete_quote_item
from wtforms.fields import FieldList, FormField
from app_backend.forms.quotation import (
    QuoteSearchForm,
    QuoteAddForm,
    QuoteEditForm,
)
from app_backend.models.bearing_project import Quote
from app_backend.permissions import (
    permission_quote_section_add,
    permission_quote_section_search,
    permission_quote_section_export,
    permission_quote_section_stats,
    QuoteItemGetPermission,
    QuoteItemEditPermission,
    QuoteItemDelPermission,
)
from app_common.maps.default import default_choices_int, default_choice_option_int
from app_common.maps.status_delete import (
    STATUS_DEL_OK,
    STATUS_DEL_NO)
from app_common.maps.type_role import (
    TYPE_ROLE_SALES,
)
from app_common.tools import json_default

# 定义蓝图
bp_quote = Blueprint('quote', __name__, url_prefix='/quote')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


@bp_quote.route('/lists.html', methods=['GET', 'POST'])
@bp_quote.route('/lists/<int:page>.html', methods=['GET', 'POST'])
@login_required
@permission_quote_section_search.require(http_exception=403)
def lists(page=1):
    """
    报价列表
    :param page:
    :return:
    """
    template_name = 'quotation/lists.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('quote lists')

    # 搜索条件
    form = QuoteSearchForm(request.form)
    form.uid.choices = get_quote_user_list_choices()
    form.cid.choices = get_quote_customer_list_choices(form.uid.data)
    # app.logger.info('')

    search_condition = [
        Quote.status_delete == STATUS_DEL_NO,
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
                search_condition.append(Quote.uid == form.uid.data)
            if form.cid.data != default_choice_option_int:
                search_condition.append(Quote.cid == form.cid.data)
            if form.start_create_time.data:
                search_condition.append(Quote.create_time >= form.start_create_time.data)
            if form.end_create_time.data:
                search_condition.append(Quote.create_time <= form.end_create_time.data)
        # 处理导出
        if form.op.data == 1:
            # 检查导出权限
            if not permission_quote_section_export.can():
                abort(403)
            column_names = Quote.__table__.columns.keys()
            query_sets = get_quote_rows(*search_condition)

            return excel.make_response_from_query_sets(
                query_sets=query_sets,
                column_names=column_names,
                file_type='csv',
                file_name='%s.csv' % _('quote lists')
            )
    # 翻页数据
    pagination = get_quote_pagination(page, PER_PAGE_BACKEND, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )


@bp_quote.route('/<int:quote_id>/info.html')
@login_required
def info(quote_id):
    """
    报价详情
    :param quote_id:
    :return:
    """
    # 检查读取权限
    quote_item_get_permission = QuoteItemGetPermission(quote_id)
    if not quote_item_get_permission.can():
        abort(403)
    # 详情数据
    quote_info = get_quote_row_by_id(quote_id)
    # 检查资源是否存在
    if not quote_info:
        abort(404)
    # 检查资源是否删除
    if quote_info.status_delete == STATUS_DEL_OK:
        abort(410)

    template_name = 'quotation/info.html'

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('quote info')

    # 获取明细
    quote_items = get_quote_item_rows(quote_id=quote_id)

    # 渲染模板
    return render_template(
        template_name,
        quote_info=quote_info,
        quote_items=quote_items,
        **document_info
    )


@bp_quote.route('/add.html', methods=['GET', 'POST'])
@login_required
@permission_quote_section_add.require(http_exception=403)
def add():
    """
    创建报价
    :return:
    """
    template_name = 'quotation/add.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('quote add')

    # 加载创建表单
    form = QuoteAddForm(request.form)
    form.uid.choices = get_quote_user_list_choices()
    form.uid.data = current_user.id
    form.cid.choices = get_quote_customer_list_choices(current_user.id)

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
            if form.quote_items.max_entries and len(form.quote_items.entries) >= form.quote_items.max_entries:
                flash('最多创建%s条记录' % form.quote_items.max_entries, 'danger')
            else:
                form.quote_items.append_entry()

            return render_template(
                template_name,
                form=form,
                **document_info
            )
        # 表单删除一行
        if form.data_line_del.data is not None:
            if form.quote_items.min_entries and len(form.quote_items.entries) <= form.quote_items.min_entries:
                flash('最少保留%s条记录' % form.quote_items.min_entries, 'danger')
            else:
                data_line_index = form.data_line_del.data
                form.quote_items.entries.pop(data_line_index)

            return render_template(
                template_name,
                form=form,
                **document_info
            )

        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Add Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                **document_info
            )

        # 表单校验成功

        quote_data = {
            'uid': form.uid.data,
            'cid': form.cid.data,
        }
        quote_id = add_quote(quote_data)

        amount_quote = 0
        for quote_item in form.quote_items.entries:

            quote_item_data = {
                'quote_id': quote_id,
                'product_id': quote_item.form.product_id.data,
                'product_brand': quote_item.form.product_brand.data,
                'product_model': quote_item.form.product_model.data,
                'product_sku': quote_item.form.product_sku.data,
                'quantity': quote_item.form.quantity.data,
                'unit_price': quote_item.form.unit_price.data,
            }

            # 新增
            add_quote_item(quote_item_data)
            amount_quote += quote_item_data['quantity'] * quote_item_data['unit_price']

        quote_data = {
            'amount_quote': amount_quote,
        }
        result = edit_quote(quote_id, quote_data)


        # todo 事务

        # 明细保存
        # 总表保存


        # 创建操作成功
        if result:
            flash(_('Add Success'), 'success')
            return redirect(request.args.get('next') or url_for('quote.lists'))
        # 创建操作失败
        else:
            flash(_('Add Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                **document_info
            )


@bp_quote.route('/<int:quote_id>/edit.html', methods=['GET', 'POST'])
@login_required
def edit(quote_id):
    """
    报价编辑
    """
    # 检查编辑权限
    quote_item_edit_permission = QuoteItemEditPermission(quote_id)
    if not quote_item_edit_permission.can():
        abort(403)

    quote_info = get_quote_row_by_id(quote_id)
    # 检查资源是否存在
    if not quote_info:
        abort(404)
    # 检查资源是否删除
    if quote_info.status_delete == STATUS_DEL_OK:
        abort(410)

    template_name = 'quotation/edit.html'

    # 加载编辑表单
    form = QuoteEditForm(request.form)
    form.uid.choices = get_quote_user_list_choices()
    form.cid.choices = get_quote_customer_list_choices(current_user.id)

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('quote edit')

    # 进入编辑页面
    if request.method == 'GET':
        # 获取明细
        quote_items = get_quote_item_rows(quote_id=quote_id)
        # 表单赋值
        form.uid.data = quote_info.uid
        form.cid.data = quote_info.cid
        # form.quote_items = quote_items
        while len(form.quote_items) > 0:
            form.quote_items.pop_entry()
        for quote_item in quote_items:
            quote_item_form = QuoteItemEditForm()
            quote_item_form.id = quote_item.id
            quote_item_form.quote_id = quote_item.quote_id
            quote_item_form.product_id = quote_item.product_id
            quote_item_form.product_brand = quote_item.product_brand
            quote_item_form.product_model = quote_item.product_model
            quote_item_form.product_sku = quote_item.product_sku
            quote_item_form.product_note = quote_item.product_note
            quote_item_form.quantity = quote_item.quantity
            quote_item_form.unit_price = quote_item.unit_price
            form.quote_items.append_entry(quote_item_form)
        # 渲染页面
        return render_template(
            template_name,
            quote_id=quote_id,
            form=form,
            **document_info
        )

    # 处理编辑请求
    if request.method == 'POST':
        # 增删数据行不需要校验表单

        # 表单新增空行
        if form.data_line_add.data is not None:
            if form.quote_items.max_entries and len(form.quote_items.entries) >= form.quote_items.max_entries:
                flash('最多创建%s条记录' % form.quote_items.max_entries, 'danger')
            else:
                form.quote_items.append_entry()

            return render_template(
                template_name,
                quote_id=quote_id,
                form=form,
                **document_info
            )
        # 表单删除一行
        if form.data_line_del.data is not None:
            if form.quote_items.min_entries and len(form.quote_items.entries) <= form.quote_items.min_entries:
                flash('最少保留%s条记录' % form.quote_items.min_entries, 'danger')
            else:
                data_line_index = form.data_line_del.data
                form.quote_items.entries.pop(data_line_index)

            return render_template(
                template_name,
                quote_id=quote_id,
                form=form,
                **document_info
            )

        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Edit Failure'), 'danger')
            flash(form.quote_items.errors, 'danger')
            return render_template(
                template_name,
                quote_id=quote_id,
                form=form,
                **document_info
            )
        # 表单校验成功

        # 获取明细
        quote_items = get_quote_item_rows(quote_id=quote_id)
        quote_items_ids = [item.id for item in quote_items]

        # 数据新增、数据删除、数据修改

        quote_items_ids_new = []
        amount_quote = 0
        for quote_item in form.quote_items.entries:
            # 错误
            if quote_item.form.id.data and quote_item.form.id.data not in quote_items_ids:
                continue

            quote_item_data = {
                'quote_id': quote_id,
                'product_id': quote_item.form.product_id.data,
                'product_brand': quote_item.form.product_brand.data,
                'product_model': quote_item.form.product_model.data,
                'product_sku': quote_item.form.product_sku.data,
                'quantity': quote_item.form.quantity.data,
                'unit_price': quote_item.form.unit_price.data,
            }

            # 新增
            if not quote_item.form.id.data:
                add_quote_item(quote_item_data)
                amount_quote += quote_item_data['quantity'] * quote_item_data['unit_price']
                continue
            # 修改
            edit_quote_item(quote_item.form.id.data, quote_item_data)
            amount_quote += quote_item_data['quantity'] * quote_item_data['unit_price']
            quote_items_ids_new.append(quote_item.form.id.data)
        # 删除
        quote_items_ids_del = list(set(quote_items_ids) - set(quote_items_ids_new))
        for quote_items_id in quote_items_ids_del:
            delete_quote_item(quote_items_id)

        # 更新总价
        quote_data = {
            'amount_quote': amount_quote,
        }
        result = edit_quote(quote_id, quote_data)

        # 编辑操作成功
        if result:
            flash(_('Edit Success'), 'success')
            return redirect(request.args.get('next') or url_for('quote.lists'))
        # 编辑操作失败
        else:
            flash(_('Edit Failure'), 'danger')
            return render_template(
                template_name,
                quote_id=quote_id,
                form=form,
                **document_info
            )


@bp_quote.route('/<int:quote_id>/preview.html')
@login_required
def preview(quote_id):
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('quote edit')

    template_name = 'quotation/preview.html'

    return render_template(
        template_name,
        quote_id=quote_id,
        **document_info
    )


@bp_quote.route('/ajax/del', methods=['GET', 'POST'])
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
        ajax_failure_msg['msg'] = _('Del Failure')  # Method Not Allowed
        return jsonify(ajax_failure_msg)

    # 检查请求参数
    quote_id = request.args.get('quote_id', 0, type=int)
    if not quote_id:
        ajax_failure_msg['msg'] = _('Del Failure')  # ID does not exist
        return jsonify(ajax_failure_msg)

    # 检查删除权限
    quote_item_del_permission = QuoteItemDelPermission(quote_id)
    if not quote_item_del_permission.can():
        ajax_failure_msg['msg'] = _('Del Failure')  # Permission Denied
        return jsonify(ajax_failure_msg)

    quote_info = get_quote_row_by_id(quote_id)
    # 检查资源是否存在
    if not quote_info:
        ajax_failure_msg['msg'] = _('Del Failure')  # ID does not exist
        return jsonify(ajax_failure_msg)
    # 检查资源是否删除
    if quote_info.status_delete == STATUS_DEL_OK:
        ajax_success_msg['msg'] = _('Del Success')  # Already deleted
        return jsonify(ajax_success_msg)

    current_time = datetime.utcnow()
    quote_data = {
        'status_delete': STATUS_DEL_OK,
        'delete_time': current_time,
        'update_time': current_time,
    }
    result = edit_quote(quote_id, quote_data)
    if result:
        ajax_success_msg['msg'] = _('Del Success')
        return jsonify(ajax_success_msg)
    else:
        ajax_failure_msg['msg'] = _('Del Failure')
        return jsonify(ajax_failure_msg)


@bp_quote.route('/ajax/stats', methods=['GET', 'POST'])
@login_required
def ajax_stats():
    """
    获取报价统计
    :return:
    """
    time_based = request.args.get('time_based', 'hour')
    result_quote_middleman = quote_middleman_stats(time_based)
    result_quote_end_user = quote_end_user_stats(time_based)

    line_chart_data = {
        'labels': [label for label, _ in result_quote_middleman],
        'datasets': [
            {
                'label': '同行',
                'backgroundColor': 'rgba(220,220,220,0.5)',
                'borderColor': 'rgba(220,220,220,1)',
                'pointBackgroundColor': 'rgba(220,220,220,1)',
                'pointBorderColor': '#fff',
                'pointBorderWidth': 2,
                'data': [data for _, data in result_quote_middleman]
            },
            {
                'label': '终端',
                'backgroundColor': 'rgba(151,187,205,0.5)',
                'borderColor': 'rgba(151,187,205,1)',
                'pointBackgroundColor': 'rgba(151,187,205,1)',
                'pointBorderColor': '#fff',
                'pointBorderWidth': 2,
                'data': [data for _, data in result_quote_end_user]
            }
        ]
    }
    return json.dumps(line_chart_data, default=json_default)


@bp_quote.route('/stats.html')
@login_required
@permission_quote_section_stats.require(http_exception=403)
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
    document_info['TITLE'] = _('quote stats')
    # 渲染模板
    return render_template(
        'quote/stats.html',
        time_based=time_based,
        **document_info
    )


@bp_quote.route('/<int:quote_id>/stats.html')
@login_required
@permission_quote_section_stats.require(http_exception=403)
def stats_item(quote_id):
    """
    报价统计明细
    :param quote_id:
    :return:
    """
    quote_info = get_quote_row_by_id(quote_id)
    # 检查资源是否存在
    if not quote_info:
        abort(404)
    # 检查资源是否删除
    if quote_info.status_delete == STATUS_DEL_OK:
        abort(410)

    # 统计数据
    quote_stats_item_info = get_quote_row_by_id(quote_id)
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('quote stats item')
    # 渲染模板
    return render_template(
        'quote/stats_item.html',
        quote_stats_item_info=quote_stats_item_info,
        **document_info
    )
