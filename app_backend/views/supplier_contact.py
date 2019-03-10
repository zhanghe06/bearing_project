#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: supplier_contact.py
@time: 2018-07-17 15:08
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
from app_backend.api.supplier import (
    get_supplier_pagination,
    get_supplier_row_by_id,
    add_supplier,
    edit_supplier,
    get_supplier_rows,
    supplier_middleman_stats,
    supplier_end_user_stats,
)
from app_backend.api.supplier_contact import (
    get_supplier_contact_pagination,
    get_supplier_contact_row_by_id,
    add_supplier_contact,
    edit_supplier_contact,
    get_supplier_contact_rows,
    delete_supplier_contact,
)
from app_backend.api.user import (
    get_user_rows
)
from app_backend.forms.supplier import (
    SupplierSearchForm,
    SupplierAddForm,
    SupplierEditForm,
)
from app_backend.forms.supplier_contact import (
    SupplierContactSearchForm,
    # SupplierContactAddForm,
    SupplierContactEditForm,
    SupplierContactItemEditForm)
from app_backend.models.bearing_project import Supplier, SupplierContact
from app_backend.permissions import (
    permission_supplier_section_add,
    permission_supplier_section_search,
    permission_supplier_section_export,
    permission_supplier_section_stats,
    SupplierItemGetPermission,
    SupplierItemEditPermission,
    SupplierItemDelPermission,
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
bp_supplier_contact = Blueprint('supplier_contact', __name__, url_prefix='/supplier/contact')

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


@bp_supplier_contact.route('/lists.html', methods=['GET', 'POST'])
@login_required
@permission_supplier_section_search.require(http_exception=403)
def lists():
    """
    渠道联系方式列表
    :return:
    """
    template_name = 'supplier/contact/lists.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('supplier contact lists')

    # 搜索条件
    form = SupplierContactSearchForm(request.form)
    # app.logger.info('')

    search_condition = [
        SupplierContact.status_delete == STATUS_DEL_NO,
    ]
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Search Failure'), 'danger')
            # 单独处理csrf_token
            if hasattr(form, 'csrf_token') and getattr(form, 'csrf_token').errors:
                map(lambda x: flash(x, 'danger'), form.csrf_token.errors)
        else:
            if form.supplier_cid.data and form.supplier_company_name.data:
                search_condition.append(SupplierContact.cid == form.supplier_cid.data)
            if form.supplier_contact_name.data:
                search_condition.append(SupplierContact.name == form.supplier_contact_name.data)
            if form.address.data:
                search_condition.append(SupplierContact.address.like('%%%s%%' % form.address.data))
            if form.mobile.data:
                search_condition.append(SupplierContact.mobile == form.mobile.data)

        # 处理导出
        if form.op.data == 1:
            # 检查导出权限
            if not permission_supplier_section_export.can():
                abort(403)
            column_names = SupplierContact.__table__.columns.keys()
            query_sets = get_supplier_rows(*search_condition)

            return excel.make_response_from_query_sets(
                query_sets=query_sets,
                column_names=column_names,
                file_type='csv',
                file_name='%s.csv' % _('supplier contact lists')
            )
    # 翻页数据
    pagination = get_supplier_contact_pagination(form.page.data, PER_PAGE_BACKEND, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )


@bp_supplier_contact.route('/<int:supplier_id>.html', methods=['GET', 'POST'])
@login_required
def edit(supplier_id):
    """
    联系方式
    注意 contact_name name 对换
    """
    # 检查编辑权限
    # supplier_item_edit_permission = SupplierItemEditPermission(supplier_id)
    # if not supplier_item_edit_permission.can():
    #     abort(403)

    supplier_info = get_supplier_row_by_id(supplier_id)
    # 检查资源是否存在
    if not supplier_info:
        abort(404)
    # 检查资源是否删除
    if supplier_info.status_delete == STATUS_DEL_OK:
        abort(410)

    template_name = 'supplier/contact/edit.html'

    # 加载编辑表单
    form = SupplierContactEditForm(request.form)
    form.cid.choices = supplier_id
    form.company_name.choices = supplier_info.company_name

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('supplier contact edit')

    # 进入编辑页面
    if request.method == 'GET':
        # 获取明细
        supplier_contact_items = get_supplier_contact_rows(cid=supplier_id)
        # 表单赋值
        form.cid.data = supplier_info.id
        form.company_name.data = supplier_info.company_name
        # form.quotation_items = quotation_items
        while len(form.supplier_contact_items) > 0:
            form.supplier_contact_items.pop_entry()
        for supplier_contact_item in supplier_contact_items:
            supplier_contact_item_form = SupplierContactItemEditForm()
            supplier_contact_item_form.id = supplier_contact_item.id
            supplier_contact_item_form.cid = supplier_contact_item.cid
            supplier_contact_item_form.contact_name = supplier_contact_item.name
            supplier_contact_item_form.salutation = supplier_contact_item.salutation
            supplier_contact_item_form.mobile = supplier_contact_item.mobile
            supplier_contact_item_form.tel = supplier_contact_item.tel
            supplier_contact_item_form.fax = supplier_contact_item.fax
            supplier_contact_item_form.email = supplier_contact_item.email
            supplier_contact_item_form.address = supplier_contact_item.address
            supplier_contact_item_form.note = supplier_contact_item.note
            supplier_contact_item_form.status_default = supplier_contact_item.status_default
            form.supplier_contact_items.append_entry(supplier_contact_item_form)
        if not supplier_contact_items:
            form.supplier_contact_items.append_entry()
        # 渲染页面
        return render_template(
            template_name,
            supplier_id=supplier_id,
            form=form,
            **document_info
        )

    # 处理编辑请求
    if request.method == 'POST':
        # 增删数据行不需要校验表单

        # 表单新增空行
        if form.data_line_add.data is not None:
            if form.supplier_contact_items.max_entries and len(
                    form.supplier_contact_items.entries) >= form.supplier_contact_items.max_entries:
                flash('最多创建%s条记录' % form.supplier_contact_items.max_entries, 'danger')
            else:
                form.supplier_contact_items.append_entry()

            return render_template(
                template_name,
                supplier_id=supplier_id,
                form=form,
                **document_info
            )
        # 表单删除一行
        if form.data_line_del.data is not None:
            if form.supplier_contact_items.min_entries and len(
                    form.supplier_contact_items.entries) <= form.supplier_contact_items.min_entries:
                flash('最少保留%s条记录' % form.supplier_contact_items.min_entries, 'danger')
            else:
                data_line_index = form.data_line_del.data
                form.supplier_contact_items.entries.pop(data_line_index)

            return render_template(
                template_name,
                supplier_id=supplier_id,
                form=form,
                **document_info
            )

        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Edit Failure'), 'danger')
            # flash(form.errors, 'danger')
            # flash(form.supplier_contact_items.errors, 'danger')
            return render_template(
                template_name,
                supplier_id=supplier_id,
                form=form,
                **document_info
            )
        # 表单校验成功

        # 获取明细
        supplier_contact_items = get_supplier_contact_rows(cid=supplier_id)
        supplier_contact_items_ids = [item.id for item in supplier_contact_items]

        # 数据新增、数据删除、数据修改

        supplier_contact_items_ids_new = []
        result = True
        for supplier_contact_item in form.supplier_contact_items.entries:
            # 错误
            if supplier_contact_item.form.id.data and supplier_contact_item.form.id.data not in supplier_contact_items_ids:
                continue

            supplier_contact_item_data = {
                'cid': supplier_id,
                'name': supplier_contact_item.form.contact_name.data,
                'salutation': supplier_contact_item.form.salutation.data,
                'mobile': supplier_contact_item.form.mobile.data,
                'tel': supplier_contact_item.form.tel.data,
                'fax': supplier_contact_item.form.fax.data,
                'email': supplier_contact_item.form.email.data,
                'address': supplier_contact_item.form.address.data,
                'note': supplier_contact_item.form.note.data,
                'status_default': supplier_contact_item.form.status_default.data,
            }

            if not supplier_contact_item.form.id.data:
                # 新增
                result = result and add_supplier_contact(supplier_contact_item_data)
            else:
                # 修改
                result = result and edit_supplier_contact(supplier_contact_item.form.id.data, supplier_contact_item_data)
                supplier_contact_items_ids_new.append(supplier_contact_item.form.id.data)
        # 删除
        supplier_contact_items_ids_del = list(set(supplier_contact_items_ids) - set(supplier_contact_items_ids_new))
        for supplier_contact_items_id in supplier_contact_items_ids_del:
            result = result and delete_supplier_contact(supplier_contact_items_id)

        # 编辑操作成功
        if result:
            flash(_('Edit Success'), 'success')
            return redirect(request.args.get('next') or url_for('supplier_contact.lists'))
        # 编辑操作失败
        else:
            flash(_('Edit Failure'), 'danger')
            return render_template(
                template_name,
                supplier_id=supplier_id,
                form=form,
                **document_info
            )


@bp_supplier_contact.route('/search.html', methods=['GET', 'POST'])
@login_required
@permission_supplier_section_search.require(http_exception=403)
def search():
    """
    渠道联系方式搜索
    :return:
    """
    template_name = 'supplier/contact/search_modal.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('Supplier Contact Search')

    # 搜索条件
    form = SupplierContactSearchForm(request.form)
    # app.logger.info('')

    search_condition = [
        SupplierContact.status_delete == STATUS_DEL_NO,
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
            if form.supplier_cid.data:
                search_condition.append(SupplierContact.cid == form.supplier_cid.data)
            if form.supplier_contact_name.data:
                search_condition.append(SupplierContact.name.like('%%%s%%' % form.supplier_contact_name.data))
    # 翻页数据
    pagination = get_supplier_contact_pagination(form.page.data, PER_PAGE_BACKEND_MODAL, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )


@bp_supplier_contact.route('/ajax/del', methods=['GET', 'POST'])
@login_required
def ajax_delete():
    """
    渠道删除
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
    supplier_id = request.args.get('supplier_id', 0, type=int)
    if not supplier_id:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查删除权限
    supplier_item_del_permission = SupplierItemDelPermission(supplier_id)
    if not supplier_item_del_permission.can():
        ext_msg = _('Permission Denied')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    supplier_info = get_supplier_row_by_id(supplier_id)
    # 检查资源是否存在
    if not supplier_info:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)
    # 检查资源是否删除
    if supplier_info.status_delete == STATUS_DEL_OK:
        ext_msg = _('Already deleted')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    current_time = datetime.utcnow()
    supplier_data = {
        'status_delete': STATUS_DEL_OK,
        'delete_time': current_time,
        'update_time': current_time,
    }
    result = edit_supplier(supplier_id, supplier_data)
    if result:
        ajax_success_msg['msg'] = _('Del Success')
        return jsonify(ajax_success_msg)
    else:
        ajax_failure_msg['msg'] = _('Del Failure')
        return jsonify(ajax_failure_msg)


@bp_supplier_contact.route('/ajax/stats', methods=['GET', 'POST'])
@login_required
def ajax_stats():
    """
    获取渠道统计
    :return:
    """
    time_based = request.args.get('time_based', 'hour')
    result_supplier_middleman = supplier_middleman_stats(time_based)
    result_supplier_end_user = supplier_end_user_stats(time_based)

    line_chart_data = {
        'labels': [label for label, _ in result_supplier_middleman],
        'datasets': [
            {
                'label': '同行',
                'backgroundColor': 'rgba(220,220,220,0.5)',
                'borderColor': 'rgba(220,220,220,1)',
                'pointBackgroundColor': 'rgba(220,220,220,1)',
                'pointBorderColor': '#fff',
                'pointBorderWidth': 2,
                'data': [data for _, data in result_supplier_middleman]
            },
            {
                'label': '终端',
                'backgroundColor': 'rgba(151,187,205,0.5)',
                'borderColor': 'rgba(151,187,205,1)',
                'pointBackgroundColor': 'rgba(151,187,205,1)',
                'pointBorderColor': '#fff',
                'pointBorderWidth': 2,
                'data': [data for _, data in result_supplier_end_user]
            }
        ]
    }
    return json.dumps(line_chart_data, default=json_default)


@bp_supplier_contact.route('/stats.html')
@login_required
@permission_supplier_section_stats.require(http_exception=403)
def stats():
    """
    渠道统计
    :return:
    """
    # 统计数据
    time_based = request.args.get('time_based', 'hour')
    if time_based not in ['hour', 'date', 'month']:
        abort(404)
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('supplier stats')
    # 渲染模板
    return render_template(
        'supplier/stats.html',
        time_based=time_based,
        **document_info
    )


@bp_supplier_contact.route('/<int:supplier_id>/stats.html')
@login_required
@permission_supplier_section_stats.require(http_exception=403)
def stats_item(supplier_id):
    """
    渠道统计明细
    :param supplier_id:
    :return:
    """
    supplier_info = get_supplier_row_by_id(supplier_id)
    # 检查资源是否存在
    if not supplier_info:
        abort(404)
    # 检查资源是否删除
    if supplier_info.status_delete == STATUS_DEL_OK:
        abort(410)

    # 统计数据
    supplier_stats_item_info = get_supplier_row_by_id(supplier_id)
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('supplier stats item')
    # 渲染模板
    return render_template(
        'supplier/stats_item.html',
        supplier_stats_item_info=supplier_stats_item_info,
        **document_info
    )
