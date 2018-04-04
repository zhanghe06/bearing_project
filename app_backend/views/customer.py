#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: customer.py
@time: 2018-03-16 09:59
"""

from __future__ import unicode_literals

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
from flask_login import login_required, current_user
from app_backend import excel
from app_backend import app
from app_backend.api.customer import (
    get_customer_pagination,
    get_customer_row_by_id,
    add_customer,
    edit_customer,
    get_customer_rows,
)
from app_backend.api.user import (
    get_user_rows
)
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
    CustomerItemPrintPermission,
)
from app_common.maps.status_delete import (
    STATUS_DEL_OK,
)
from app_common.maps.type_role import (
    TYPE_ROLE_SALES
)
from app_common.maps.default import default_choices, default_choice_option
from flask_babel import gettext as _, ngettext

# 定义蓝图
bp_customer = Blueprint('customer', __name__, url_prefix='/customer')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


def get_sales_user_list():
    sales_user_list = copy(default_choices)
    user_list = get_user_rows(**{'role_id': TYPE_ROLE_SALES})
    sales_user_list.extend([(0, '-')])
    sales_user_list.extend([(user.id, user.name) for user in user_list])
    return sales_user_list


@bp_customer.route('/lists.html', methods=['GET', 'POST'])
@bp_customer.route('/lists/<int:page>.html', methods=['GET', 'POST'])
@login_required
@permission_customer_section_search.require(http_exception=403)
def lists(page=1):
    """
    客户列表
    :param page:
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

    search_condition = []
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Search Failure'), 'danger')
            # 单独处理csrf_token
            if hasattr(form, 'csrf_token') and getattr(form, 'csrf_token').errors:
                map(lambda x: flash(x, 'danger'), form.csrf_token.errors)
        else:
            if form.company_name.data:
                search_condition.append(Customer.company_name == form.company_name.data)
            if form.company_type.data != default_choice_option:
                search_condition.append(Customer.company_type == form.company_type.data)
            if form.owner_uid.data != default_choice_option:
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
    # 翻页数据
    pagination = get_customer_pagination(page, PER_PAGE_BACKEND, *search_condition)

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
@permission_customer_section_add.require(http_exception=403)
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
            'company_type': form.company_type.data,
            'owner_uid': form.owner_uid.data,
            'status_delete': form.status_delete.data,
            'delete_time': form.delete_time.data,
            'create_time': current_time,
            'update_time': current_time,
        }
        result = add_customer(customer_data)
        # 创建操作成功
        if result:
            flash(_('Add Success'), 'success')
            return redirect(request.args.get('next') or url_for('customer.lists'))
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

    template_name = 'customer/edit.html'

    # 加载编辑表单
    form = CustomerEditForm(request.form)

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('customer edit')

    # 进入编辑页面
    if request.method == 'GET':
        # 表单赋值
        form.company_name.data = customer_info.company_name
        form.company_address.data = customer_info.company_address
        form.company_site.data = customer_info.company_site
        form.company_tel.data = customer_info.company_tel
        form.company_fax.data = customer_info.company_fax
        form.company_type.data = customer_info.company_type
        form.owner_uid.data = customer_info.owner_uid
        form.status_delete.data = customer_info.status_delete
        form.delete_time.data = customer_info.delete_time
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
        if not form.validate_on_submit():
            flash(_('Edit Failure'), 'danger')
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
            'company_type': form.company_type.data,
            'owner_uid': form.owner_uid.data,
            'status_delete': form.status_delete.data,
            'delete_time': form.delete_time.data,
            'create_time': current_time,
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
        ajax_failure_msg['msg'] = _('Del Failure')  # Method Not Allowed
        return jsonify(ajax_failure_msg)

    # 检查请求参数
    customer_id = request.args.get('customer_id', 0, type=int)
    if not customer_id:
        ajax_failure_msg['msg'] = _('Del Failure')  # ID does not exist
        return jsonify(ajax_failure_msg)

    # 检查删除权限
    customer_item_del_permission = CustomerItemDelPermission(customer_id)
    if not customer_item_del_permission.can():
        ajax_failure_msg['msg'] = _('Del Failure')  # Permission Denied
        return jsonify(ajax_failure_msg)

    customer_info = get_customer_row_by_id(customer_id)
    # 检查资源是否存在
    if not customer_info:
        ajax_failure_msg['msg'] = _('Del Failure')  # ID does not exist
        return jsonify(ajax_failure_msg)
    # 检查资源是否删除
    if customer_info.status_delete == STATUS_DEL_OK:
        ajax_success_msg['msg'] = _('Del Success')  # Already deleted
        return jsonify(ajax_success_msg)

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


@bp_customer.route('/stats.html')
@bp_customer.route('/stats/<int:page>.html')
@login_required
@permission_customer_section_stats.require(http_exception=403)
def stats(page=1):
    """
    客户统计
    :param page:
    :return:
    """
    # 获取当前用户角色（销售统计自己的客户，经理统计所属销售的客户）
    # 统计数据
    customer_stats_info = get_customer_pagination(page, PER_PAGE_BACKEND)
    # 翻页数据
    pagination = get_customer_pagination(page, PER_PAGE_BACKEND)
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('customer stats')
    # 渲染模板
    return render_template(
        'customer/stats.html',
        customer_stats_info=customer_stats_info,
        pagination=pagination,
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
