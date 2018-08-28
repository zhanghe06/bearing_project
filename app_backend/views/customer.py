#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: customer.py
@time: 2018-03-16 09:59
"""

from __future__ import unicode_literals

import json
from copy import copy
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
from app_backend.api.customer import (
    get_customer_pagination,
    get_customer_row_by_id,
    add_customer,
    edit_customer,
    get_customer_rows,
    customer_middleman_stats,
    customer_end_user_stats,
)
from app_backend.api.production_sensitive import count_production_sensitive
from app_backend.api.user import (
    get_user_rows,
    get_user_choices)
from app_backend.api.quotation import count_quotation
from app_backend.forms.customer import (
    CustomerSearchForm,
    CustomerAddForm,
    CustomerEditForm,
)
from app_backend.models.bearing_project import Customer
from app_backend.permissions import (
    permission_customer_section_add,
    permission_customer_section_search,
    permission_customer_section_export,
    permission_customer_section_stats,
    CustomerItemGetPermission,
    CustomerItemEditPermission,
    CustomerItemDelPermission,
)
from app_backend.signals.customer import signal_customer_status_delete
from app_common.maps.default import default_choices_int, default_choice_option_int
from app_common.maps.status_delete import (
    STATUS_DEL_OK,
    STATUS_DEL_NO)
from app_common.maps.type_company import TYPE_COMPANY_CHOICES
from app_common.maps.type_role import (
    TYPE_ROLE_SALES,
)
from app_common.tools import json_default

# 定义蓝图
bp_customer = Blueprint('customer', __name__, url_prefix='/customer')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
PER_PAGE_BACKEND_MODAL = app.config.get('PER_PAGE_BACKEND_MODAL', 10)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


def get_sales_user_list():
    sales_user_list = copy(default_choices_int)
    user_list = get_user_rows(**{'role_id': TYPE_ROLE_SALES})
    sales_user_list.extend([(0, '-')])
    sales_user_list.extend([(user.id, user.name) for user in user_list])
    return sales_user_list


@bp_customer.route('/lists.html', methods=['GET', 'POST'])
@login_required
@permission_customer_section_search.require(http_exception=403)
def lists():
    """
    客户列表
    :return:
    """
    template_name = 'customer/lists.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('customer lists')

    # 搜索条件
    form = CustomerSearchForm(request.form)
    form.owner_uid.choices = get_sales_user_list()
    # app.logger.info('')

    search_condition = [
        Customer.status_delete == STATUS_DEL_NO,
    ]
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Search Failure'), 'danger')
            # 单独处理csrf_token
            if hasattr(form, 'csrf_token') and getattr(form, 'csrf_token').errors:
                map(lambda x: flash(x, 'danger'), form.csrf_token.errors)
        else:
            if form.company_name.data:
                search_condition.append(Customer.company_name.like('%%%s%%' % form.company_name.data))
            if form.company_type.data != default_choice_option_int:
                search_condition.append(Customer.company_type == form.company_type.data)
            if form.owner_uid.data != default_choice_option_int:
                search_condition.append(Customer.owner_uid == form.owner_uid.data)
            if form.start_create_time.data:
                search_condition.append(Customer.create_time >= form.start_create_time.data)
            if form.end_create_time.data:
                search_condition.append(Customer.create_time <= form.end_create_time.data)
        # 处理导出
        if form.op.data == 1:
            # 检查导出权限
            if not permission_customer_section_export.can():
                abort(403)
            column_names = Customer.__table__.columns.keys()
            query_sets = get_customer_rows(*search_condition)

            return excel.make_response_from_query_sets(
                query_sets=query_sets,
                column_names=column_names,
                file_type='csv',
                file_name='%s.csv' % _('customer lists')
            )
        # 批量删除
        if form.op.data == 2:
            customer_ids = request.form.getlist('customer_id')
            # 检查删除权限
            permitted = True
            for customer_id in customer_ids:
                # 明细权限
                customer_item_del_permission = CustomerItemDelPermission(customer_id)
                if not customer_item_del_permission.can():
                    ext_msg = _('Permission Denied')
                    flash(_('Del Failure, %(ext_msg)s', ext_msg=ext_msg), 'danger')
                    permitted = False
                    break
                # 检查是否正在使用
                # 报价、订单、敏感型号
                if count_quotation(**{'cid': customer_id, 'status_delete': STATUS_DEL_NO}):
                    ext_msg = _('Currently In Use')
                    flash(_('Del Failure, %(ext_msg)s', ext_msg=ext_msg), 'danger')
                    permitted = False
                    break
                if count_production_sensitive(**{'cid': customer_id, 'status_delete': STATUS_DEL_NO}):
                    ext_msg = _('Currently In Use')
                    flash(_('Del Failure, %(ext_msg)s', ext_msg=ext_msg), 'danger')
                    permitted = False
                    break
            if permitted:
                result_total = True
                for customer_id in customer_ids:
                    current_time = datetime.utcnow()
                    customer_data = {
                        'status_delete': STATUS_DEL_OK,
                        'delete_time': current_time,
                        'update_time': current_time,
                    }
                    result = edit_customer(customer_id, customer_data)
                    if result:
                        # 发送删除信号
                        signal_data = {
                            'customer_id': customer_id,
                            'status_delete': STATUS_DEL_OK,
                            'current_time': current_time,
                        }
                        signal_customer_status_delete.send(app, **signal_data)
                    result_total = result_total and result
                if result_total:
                    flash(_('Del Success'), 'success')
                else:
                    flash(_('Del Failure'), 'danger')

    # 翻页数据
    pagination = get_customer_pagination(form.page.data, PER_PAGE_BACKEND, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )


@bp_customer.route('/search.html', methods=['GET', 'POST'])
@login_required
@permission_customer_section_search.require(http_exception=403)
def search():
    """
    客户搜索
    :return:
    """
    template_name = 'customer/search_modal.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('Customer Search')

    # 搜索条件
    form = CustomerSearchForm(request.form)
    form.owner_uid.choices = get_sales_user_list()
    # app.logger.info('')

    search_condition = [
        Customer.status_delete == STATUS_DEL_NO,
    ]
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Search Failure'), 'danger')
            # 单独处理csrf_token
            if hasattr(form, 'csrf_token') and getattr(form, 'csrf_token').errors:
                map(lambda x: flash(x, 'danger'), form.csrf_token.errors)
        else:
            if form.company_type.data != default_choice_option_int:
                search_condition.append(Customer.company_type == form.company_type.data)
            if form.company_name.data:
                search_condition.append(Customer.company_name.like('%%%s%%' % form.company_name.data))
    # 翻页数据
    pagination = get_customer_pagination(form.page.data, PER_PAGE_BACKEND_MODAL, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )


@bp_customer.route('/<int:customer_id>/info.html')
@login_required
def info(customer_id):
    """
    客户详情
    :param customer_id:
    :return:
    """
    # 检查读取权限
    customer_item_get_permission = CustomerItemGetPermission(customer_id)
    if not customer_item_get_permission.can():
        abort(403)
    # 详情数据
    customer_info = get_customer_row_by_id(customer_id)
    # 检查资源是否存在
    if not customer_info:
        abort(404)
    # 检查资源是否删除
    if customer_info.status_delete == STATUS_DEL_OK:
        abort(410)
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('customer info')
    # 渲染模板
    return render_template('customer/info.html', customer_info=customer_info, **document_info)


@bp_customer.route('/add.html', methods=['GET', 'POST'])
@login_required
# @permission_customer_section_add.require(http_exception=403)
def add():
    """
    创建客户
    :return:
    """
    template_name = 'customer/add.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('customer add')

    # 加载创建表单
    form = CustomerAddForm(request.form)

    form.company_type.choices = TYPE_COMPANY_CHOICES
    form.owner_uid.choices = get_user_choices()
    form.owner_uid.data = current_user.id

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
        # 表单校验失败
        if not form.validate_on_submit():
            flash(form.errors, 'danger')
            flash(_('Add Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                **document_info
            )

        # 表单校验成功
        current_time = datetime.utcnow()
        customer_data = {
            'company_name': form.company_name.data,
            'company_address': form.company_address.data,
            'company_site': form.company_site.data,
            'company_tel': form.company_tel.data,
            'company_fax': form.company_fax.data,
            'company_email': form.company_email.data,
            'company_type': form.company_type.data,
            'owner_uid': form.owner_uid.data,
            'create_time': current_time,
            'update_time': current_time,
        }
        result = add_customer(customer_data)
        # 创建操作成功
        if result:
            flash(_('Add Success'), 'success')
            return redirect(request.args.get('next') or url_for('customer.edit', customer_id=result))
        # 创建操作失败
        else:
            flash(_('Add Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                **document_info
            )


@bp_customer.route('/<int:customer_id>/edit.html', methods=['GET', 'POST'])
@login_required
def edit(customer_id):
    """
    客户编辑
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

    template_name = 'customer/edit.html'

    # 加载编辑表单
    form = CustomerEditForm(request.form)

    form.company_type.choices = TYPE_COMPANY_CHOICES
    form.owner_uid.choices = get_user_choices()

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('customer edit')

    # 进入编辑页面
    if request.method == 'GET':
        # 表单赋值
        form.id.data = customer_info.id
        form.company_name.data = customer_info.company_name
        form.company_address.data = customer_info.company_address
        form.company_site.data = customer_info.company_site
        form.company_tel.data = customer_info.company_tel
        form.company_fax.data = customer_info.company_fax
        form.company_email.data = customer_info.company_email
        form.company_type.data = customer_info.company_type
        form.owner_uid.data = customer_info.owner_uid
        form.create_time.data = customer_info.create_time
        form.update_time.data = customer_info.update_time
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
        if customer_id != form.id.data or not form.validate_on_submit():
            flash(_('Edit Failure'), 'danger')
            # flash(form.errors, 'danger')
            return render_template(
                template_name,
                customer_id=customer_id,
                form=form,
                **document_info
            )
        # 表单校验成功
        current_time = datetime.utcnow()
        customer_data = {
            'company_name': form.company_name.data,
            'company_address': form.company_address.data,
            'company_site': form.company_site.data,
            'company_tel': form.company_tel.data,
            'company_fax': form.company_fax.data,
            'company_email': form.company_email.data,
            'company_type': form.company_type.data,
            'owner_uid': form.owner_uid.data,
            'update_time': current_time,
        }
        result = edit_customer(customer_id, customer_data)
        # 编辑操作成功
        if result:
            flash(_('Edit Success'), 'success')
            return redirect(request.args.get('next') or url_for('customer.lists'))
        # 编辑操作失败
        else:
            flash(_('Edit Failure'), 'danger')
            return render_template(
                template_name,
                customer_id=customer_id,
                form=form,
                **document_info
            )


@bp_customer.route('/ajax/del', methods=['GET', 'POST'])
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
    # 检查是否正在使用
    # 报价、订单、敏感型号
    if count_quotation(**{'cid': customer_id, 'status_delete': STATUS_DEL_NO}):
        ext_msg = _('Currently In Use')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)
    if count_production_sensitive(**{'cid': customer_id, 'status_delete': STATUS_DEL_NO}):
        ext_msg = _('Currently In Use')
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

        # 发送删除信号
        signal_data = {
            'customer_id': customer_id,
            'status_delete': STATUS_DEL_OK,
            'current_time': current_time,
        }
        signal_customer_status_delete.send(app, **signal_data)

        ajax_success_msg['msg'] = _('Del Success')
        return jsonify(ajax_success_msg)
    else:
        ajax_failure_msg['msg'] = _('Del Failure')
        return jsonify(ajax_failure_msg)


@bp_customer.route('/ajax/stats', methods=['GET', 'POST'])
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


@bp_customer.route('/stats.html')
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


@bp_customer.route('/<int:customer_id>/stats.html')
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
