#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: customer_contact.py
@time: 2018-03-16 10:03
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
from flask_login import login_required

from app_backend import (
    app,
    excel,
)
from app_backend.api.customer import (
    get_customer_pagination,
    get_customer_row_by_id,
    add_customer,
    edit_customer,
    get_customer_rows,
    customer_middleman_stats,
    customer_end_user_stats,
)
from app_backend.api.customer_contact import (
    get_customer_contact_pagination,
    get_customer_contact_row_by_id,
    add_customer_contact,
    edit_customer_contact,
    get_customer_contact_rows,
    delete_customer_contact,
)
from app_backend.api.user import (
    get_user_rows
)
from app_backend.forms.customer import (
    CustomerSearchForm,
    CustomerAddForm,
    CustomerEditForm,
)
from app_backend.forms.customer_contact import (
    CustomerContactSearchForm,
    # CustomerContactAddForm,
    CustomerContactEditForm,
    CustomerContactItemEditForm)
from app_backend.models.bearing_project import Customer, CustomerContact
from app_backend.permissions.customer import (
    permission_customer_section_add,
    permission_customer_section_search,
    permission_customer_section_export,
    permission_customer_section_stats,
    CustomerItemGetPermission,
    CustomerItemEditPermission,
    CustomerItemDelPermission,
)
from app_common.maps.default import default_search_choices_int, default_search_choice_option_int
from app_common.maps.status_delete import (
    STATUS_DEL_OK,
    STATUS_DEL_NO)
from app_common.maps.type_role import (
    TYPE_ROLE_SALES,
)
from app_common.tools import json_default

# 定义蓝图
bp_customer_contact = Blueprint('customer_contact', __name__, url_prefix='/customer/contact')

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


@bp_customer_contact.route('/lists.html', methods=['GET', 'POST'])
@login_required
@permission_customer_section_search.require(http_exception=403)
def lists():
    """
    客户联系方式列表
    :return:
    """
    template_name = 'customer/contact/lists.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('customer contact lists')

    # 搜索条件
    form = CustomerContactSearchForm(request.form)
    # app.logger.info('')

    search_condition = [
        CustomerContact.status_delete == STATUS_DEL_NO,
    ]
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Search Failure'), 'danger')
            # 单独处理csrf_token
            if hasattr(form, 'csrf_token') and getattr(form, 'csrf_token').errors:
                map(lambda x: flash(x, 'danger'), form.csrf_token.errors)
        else:
            if form.customer_cid.data and form.customer_company_name.data:
                search_condition.append(CustomerContact.cid == form.customer_cid.data)
            if form.customer_contact_name.data:
                search_condition.append(CustomerContact.name == form.customer_contact_name.data)
            if form.address.data:
                search_condition.append(CustomerContact.address.like('%%%s%%' % form.address.data))
            if form.mobile.data:
                search_condition.append(CustomerContact.mobile == form.mobile.data)

        # 处理导出
        if form.op.data == 1:
            # 检查导出权限
            if not permission_customer_section_export.can():
                abort(403)
            column_names = CustomerContact.__table__.columns.keys()
            query_sets = get_customer_rows(*search_condition)

            return excel.make_response_from_query_sets(
                query_sets=query_sets,
                column_names=column_names,
                file_type='csv',
                file_name='%s.csv' % _('customer contact lists')
            )
    # 翻页数据
    pagination = get_customer_contact_pagination(form.page.data, PER_PAGE_BACKEND, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )


@bp_customer_contact.route('/<int:customer_id>.html', methods=['GET', 'POST'])
@login_required
def edit(customer_id):
    """
    联系方式
    注意 contact_name name 对换
    """
    # 检查编辑权限
    customer_item_edit_permission = CustomerItemEditPermission(customer_id)
    if not customer_item_edit_permission.can():
        abort(403)

    customer_info = get_customer_row_by_id(customer_id)
    # 检查资源是否存在
    if not customer_info:
        abort(404)
    # 检查资源是否删除
    if customer_info.status_delete == STATUS_DEL_OK:
        abort(410)

    template_name = 'customer/contact/edit.html'

    # 加载编辑表单
    form = CustomerContactEditForm(request.form)
    form.cid.choices = customer_id
    form.company_name.choices = customer_info.company_name

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('customer contact edit')

    # 进入编辑页面
    if request.method == 'GET':
        # 获取明细
        customer_contact_items = get_customer_contact_rows(cid=customer_id)
        # 表单赋值
        form.cid.data = customer_info.id
        form.company_name.data = customer_info.company_name
        # form.quotation_items = quotation_items
        while len(form.customer_contact_items) > 0:
            form.customer_contact_items.pop_entry()
        for customer_contact_item in customer_contact_items:
            customer_contact_item_form = CustomerContactItemEditForm()
            customer_contact_item_form.id = customer_contact_item.id
            customer_contact_item_form.cid = customer_contact_item.cid
            customer_contact_item_form.contact_name = customer_contact_item.name
            customer_contact_item_form.salutation = customer_contact_item.salutation
            customer_contact_item_form.mobile = customer_contact_item.mobile
            customer_contact_item_form.tel = customer_contact_item.tel
            customer_contact_item_form.fax = customer_contact_item.fax
            customer_contact_item_form.email = customer_contact_item.email
            customer_contact_item_form.address = customer_contact_item.address
            customer_contact_item_form.note = customer_contact_item.note
            customer_contact_item_form.status_default = customer_contact_item.status_default
            form.customer_contact_items.append_entry(customer_contact_item_form)
        if not customer_contact_items:
            form.customer_contact_items.append_entry()
        # 渲染页面
        return render_template(
            template_name,
            customer_id=customer_id,
            form=form,
            **document_info
        )

    # 处理编辑请求
    if request.method == 'POST':
        # 增删数据行不需要校验表单

        # 表单新增空行
        if form.data_line_add.data is not None:
            if form.customer_contact_items.max_entries and len(
                    form.customer_contact_items.entries) >= form.customer_contact_items.max_entries:
                flash('最多创建%s条记录' % form.customer_contact_items.max_entries, 'danger')
            else:
                form.customer_contact_items.append_entry()

            return render_template(
                template_name,
                customer_id=customer_id,
                form=form,
                **document_info
            )
        # 表单删除一行
        if form.data_line_del.data is not None:
            if form.customer_contact_items.min_entries and len(
                    form.customer_contact_items.entries) <= form.customer_contact_items.min_entries:
                flash('最少保留%s条记录' % form.customer_contact_items.min_entries, 'danger')
            else:
                data_line_index = form.data_line_del.data
                form.customer_contact_items.entries.pop(data_line_index)

            return render_template(
                template_name,
                customer_id=customer_id,
                form=form,
                **document_info
            )

        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Edit Failure'), 'danger')
            # flash(form.errors, 'danger')
            # flash(form.customer_contact_items.errors, 'danger')
            return render_template(
                template_name,
                customer_id=customer_id,
                form=form,
                **document_info
            )
        # 表单校验成功

        # 获取明细
        customer_contact_items = get_customer_contact_rows(cid=customer_id)
        customer_contact_items_ids = [item.id for item in customer_contact_items]

        # 数据新增、数据删除、数据修改

        customer_contact_items_ids_new = []
        result = True
        for customer_contact_item in form.customer_contact_items.entries:
            # 错误
            if customer_contact_item.form.id.data and customer_contact_item.form.id.data not in customer_contact_items_ids:
                continue

            customer_contact_item_data = {
                'cid': customer_id,
                'name': customer_contact_item.form.contact_name.data,
                'salutation': customer_contact_item.form.salutation.data,
                'mobile': customer_contact_item.form.mobile.data,
                'tel': customer_contact_item.form.tel.data,
                'fax': customer_contact_item.form.fax.data,
                'email': customer_contact_item.form.email.data,
                'address': customer_contact_item.form.address.data,
                'note': customer_contact_item.form.note.data,
                'status_default': customer_contact_item.form.status_default.data,
            }

            if not customer_contact_item.form.id.data:
                # 新增
                result = result and add_customer_contact(customer_contact_item_data)
            else:
                # 修改
                result = result and edit_customer_contact(customer_contact_item.form.id.data, customer_contact_item_data)
                customer_contact_items_ids_new.append(customer_contact_item.form.id.data)
        # 删除
        customer_contact_items_ids_del = list(set(customer_contact_items_ids) - set(customer_contact_items_ids_new))
        for customer_contact_items_id in customer_contact_items_ids_del:
            result = result and delete_customer_contact(customer_contact_items_id)

        # 编辑操作成功
        if result:
            flash(_('Edit Success'), 'success')
            return redirect(request.args.get('next') or url_for('customer_contact.lists'))
        # 编辑操作失败
        else:
            flash(_('Edit Failure'), 'danger')
            return render_template(
                template_name,
                customer_id=customer_id,
                form=form,
                **document_info
            )


@bp_customer_contact.route('/search.html', methods=['GET', 'POST'])
@login_required
@permission_customer_section_search.require(http_exception=403)
def search():
    """
    客户联系方式搜索
    :return:
    """
    template_name = 'customer/contact/search_modal.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('Customer Contact Search')

    # 搜索条件
    form = CustomerContactSearchForm(request.form)
    # app.logger.info('')

    search_condition = [
        CustomerContact.status_delete == STATUS_DEL_NO,
    ]
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Search Failure'), 'danger')
            # flash(form.errors, 'danger')
            # 单独处理csrf_token
            if hasattr(form, 'csrf_token') and getattr(form, 'csrf_token').errors:
                map(lambda x: flash(x, 'danger'), form.csrf_token.errors)
        else:
            if form.customer_cid.data:
                search_condition.append(CustomerContact.cid == form.customer_cid.data)
            if form.customer_contact_name.data:
                search_condition.append(CustomerContact.name.like('%%%s%%' % form.customer_contact_name.data))
    # 翻页数据
    pagination = get_customer_contact_pagination(form.page.data, PER_PAGE_BACKEND_MODAL, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )


@bp_customer_contact.route('/ajax/del', methods=['GET', 'POST'])
@login_required
def ajax_delete():
    """
    客户删除
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
    customer_id = request.args.get('customer_id', 0, type=int)
    if not customer_id:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查删除权限
    customer_item_del_permission = CustomerItemDelPermission(customer_id)
    if not customer_item_del_permission.can():
        ext_msg = _('Permission Denied')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    customer_info = get_customer_row_by_id(customer_id)
    # 检查资源是否存在
    if not customer_info:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)
    # 检查资源是否删除
    if customer_info.status_delete == STATUS_DEL_OK:
        ext_msg = _('Already deleted')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    current_time = datetime.utcnow()
    customer_data = {
        'status_delete': STATUS_DEL_OK,
        'delete_time': current_time,
        'update_time': current_time,
    }
    result = edit_customer(customer_id, customer_data)
    if result:
        ajax_success_msg['msg'] = _('Del Success')
        return jsonify(ajax_success_msg)
    else:
        ajax_failure_msg['msg'] = _('Del Failure')
        return jsonify(ajax_failure_msg)


@bp_customer_contact.route('/ajax/stats', methods=['GET', 'POST'])
@login_required
def ajax_stats():
    """
    获取客户统计
    :return:
    """
    time_based = request.args.get('time_based', 'hour')
    result_customer_middleman = customer_middleman_stats(time_based)
    result_customer_end_user = customer_end_user_stats(time_based)

    line_chart_data = {
        'labels': [label for label, _ in result_customer_middleman],
        'datasets': [
            {
                'label': '同行',
                'backgroundColor': 'rgba(220,220,220,0.5)',
                'borderColor': 'rgba(220,220,220,1)',
                'pointBackgroundColor': 'rgba(220,220,220,1)',
                'pointBorderColor': '#fff',
                'pointBorderWidth': 2,
                'data': [data for _, data in result_customer_middleman]
            },
            {
                'label': '终端',
                'backgroundColor': 'rgba(151,187,205,0.5)',
                'borderColor': 'rgba(151,187,205,1)',
                'pointBackgroundColor': 'rgba(151,187,205,1)',
                'pointBorderColor': '#fff',
                'pointBorderWidth': 2,
                'data': [data for _, data in result_customer_end_user]
            }
        ]
    }
    return json.dumps(line_chart_data, default=json_default)


@bp_customer_contact.route('/stats.html')
@login_required
@permission_customer_section_stats.require(http_exception=403)
def stats():
    """
    客户统计
    :return:
    """
    # 统计数据
    time_based = request.args.get('time_based', 'hour')
    if time_based not in ['hour', 'date', 'month']:
        abort(404)
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('customer stats')
    # 渲染模板
    return render_template(
        'customer/stats.html',
        time_based=time_based,
        **document_info
    )


@bp_customer_contact.route('/<int:customer_id>/stats.html')
@login_required
@permission_customer_section_stats.require(http_exception=403)
def stats_item(customer_id):
    """
    客户统计明细
    :param customer_id:
    :return:
    """
    customer_info = get_customer_row_by_id(customer_id)
    # 检查资源是否存在
    if not customer_info:
        abort(404)
    # 检查资源是否删除
    if customer_info.status_delete == STATUS_DEL_OK:
        abort(410)

    # 统计数据
    customer_stats_item_info = get_customer_row_by_id(customer_id)
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('customer stats item')
    # 渲染模板
    return render_template(
        'customer/stats_item.html',
        customer_stats_item_info=customer_stats_item_info,
        **document_info
    )
