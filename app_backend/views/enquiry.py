#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: enquiry.py
@time: 2018-09-13 10:08
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
# from app_backend.api.customer import get_customer_choices, get_customer_row_by_id
# from app_backend.api.customer_contact import get_customer_contact_row_by_id
from app_backend.api.supplier import get_supplier_row_by_id
from app_backend.api.supplier_contact import get_supplier_contact_row_by_id
from app_backend.api.user import get_user_choices, get_user_row_by_id
from app_backend.forms.production import ProductionSelectForm
from app_backend.forms.enquiry import EnquiryItemEditForm
from app_backend import (
    app,
    excel,
)
from app_backend.api.enquiry import (
    get_enquiry_pagination,
    get_enquiry_row_by_id,
    add_enquiry,
    edit_enquiry,
    get_enquiry_rows,
    get_distinct_enquiry_uid,
    get_distinct_enquiry_cid,
    enquiry_total_stats,
    enquiry_order_stats,
    get_enquiry_user_list_choices, get_enquiry_customer_list_choices)

from app_backend.api.enquiry_items import get_enquiry_items_rows, add_enquiry_items, edit_enquiry_items, \
    delete_enquiry_items
from wtforms.fields import FieldList, FormField
from app_backend.forms.enquiry import (
    EnquirySearchForm,
    EnquiryAddForm,
    EnquiryEditForm,
)
from app_backend.models.bearing_project import Enquiry
from app_backend.permissions import (
    permission_enquiry_section_add,
    permission_enquiry_section_search,
    permission_enquiry_section_export,
    permission_enquiry_section_stats,
    EnquiryItemGetPermission,
    EnquiryItemEditPermission,
    EnquiryItemDelPermission,
)
from app_backend.signals.enquiry import signal_enquiry_status_delete
from app_common.maps.default import default_search_choices_int, default_search_choice_option_int
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

bp_enquiry = Blueprint('enquiry', __name__, url_prefix='/enquiry')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


@bp_enquiry.route('/lists.html', methods=['GET', 'POST'])
@login_required
@permission_enquiry_section_search.require(http_exception=403)
def lists():
    """
    询价列表
    :return:
    """
    template_name = 'enquiry/lists.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('enquiry lists')

    # 搜索条件
    form = EnquirySearchForm(request.form)
    form.uid.choices = get_enquiry_user_list_choices()
    # app.logger.info('')

    search_condition = [
        Enquiry.status_delete == STATUS_DEL_NO,
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
                search_condition.append(Enquiry.uid == form.uid.data)
            if form.supplier_cid.data and form.supplier_company_name.data:
                search_condition.append(Enquiry.supplier_cid == form.supplier_cid.data)
            if form.start_create_time.data:
                search_condition.append(Enquiry.create_time >= form.start_create_time.data)
            if form.end_create_time.data:
                search_condition.append(Enquiry.create_time <= form.end_create_time.data)
        # 处理导出
        if form.op.data == 1:
            # 检查导出权限
            if not permission_enquiry_section_export.can():
                abort(403)
            column_names = Enquiry.__table__.columns.keys()
            query_sets = get_enquiry_rows(*search_condition)

            return excel.make_response_from_query_sets(
                query_sets=query_sets,
                column_names=column_names,
                file_type='csv',
                file_name='%s.csv' % _('enquiry lists')
            )
        # 批量删除
        if form.op.data == 2:
            enquiry_ids = request.form.getlist('enquiry_id')
            # 检查删除权限
            permitted = True
            for enquiry_id in enquiry_ids:
                enquiry_item_del_permission = EnquiryItemDelPermission(enquiry_id)
                if not enquiry_item_del_permission.can():
                    ext_msg = _('Permission Denied')
                    flash(_('Del Failure, %(ext_msg)s', ext_msg=ext_msg), 'danger')
                    permitted = False
                    break
            if permitted:
                result_total = True
                for enquiry_id in enquiry_ids:
                    current_time = datetime.utcnow()
                    enquiry_data = {
                        'status_delete': STATUS_DEL_OK,
                        'delete_time': current_time,
                        'update_time': current_time,
                    }
                    result = edit_enquiry(enquiry_id, enquiry_data)
                    if result:
                        # 发送删除信号
                        signal_data = {
                            'enquiry_id': enquiry_id,
                            'status_delete': STATUS_DEL_OK,
                            'current_time': current_time,
                        }
                        signal_enquiry_status_delete.send(app, **signal_data)
                    result_total = result_total and result
                if result_total:
                    flash(_('Del Success'), 'success')
                else:
                    flash(_('Del Failure'), 'danger')
    # 翻页数据
    pagination = get_enquiry_pagination(form.page.data, PER_PAGE_BACKEND, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )


@bp_enquiry.route('/<int:enquiry_id>/info.html')
@login_required
def info(enquiry_id):
    """
    询价详情
    :param enquiry_id:
    :return:
    """
    # 检查读取权限
    enquiry_item_get_permission = EnquiryItemGetPermission(enquiry_id)
    if not enquiry_item_get_permission.can():
        abort(403)
    # 详情数据
    enquiry_info = get_enquiry_row_by_id(enquiry_id)
    # 检查资源是否存在
    if not enquiry_info:
        abort(404)
    # 检查资源是否删除
    if enquiry_info.status_delete == STATUS_DEL_OK:
        abort(410)

    # 公司信息
    company_info = get_supplier_row_by_id(enquiry_info.supplier_cid)

    template_name = 'enquiry/info.html'

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('enquiry info')

    # 获取明细
    enquiry_items = get_enquiry_items_rows(enquiry_id=enquiry_id)

    # 渲染模板
    return render_template(
        template_name,
        enquiry_info=enquiry_info,
        enquiry_items=enquiry_items,
        company_info=company_info,
        **document_info
    )


@bp_enquiry.route('/add.html', methods=['GET', 'POST'])
@login_required
@permission_enquiry_section_add.require(http_exception=403)
def add():
    """
    创建询价
    :return:
    """
    template_name = 'enquiry/add.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('enquiry add')

    # 加载创建表单
    form = EnquiryAddForm(request.form)
    form.uid.choices = get_user_choices()
    form.uid.data = current_user.id
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
            if form.enquiry_items.max_entries and len(
                    form.enquiry_items.entries) >= form.enquiry_items.max_entries:
                flash('最多创建%s条记录' % form.enquiry_items.max_entries, 'danger')
            else:
                form.enquiry_items.append_entry()

            return render_template(
                template_name,
                form=form,
                **document_info
            )
        # 表单删除一行
        if form.data_line_del.data is not None:
            if form.enquiry_items.min_entries and len(
                    form.enquiry_items.entries) <= form.enquiry_items.min_entries:
                flash('最少保留%s条记录' % form.enquiry_items.min_entries, 'danger')
            else:
                data_line_index = form.data_line_del.data
                form.enquiry_items.entries.pop(data_line_index)

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

        # 创建询价
        current_time = datetime.utcnow()
        enquiry_data = {
            'uid': form.uid.data,
            'supplier_cid': form.supplier_cid.data,
            'supplier_contact_id': form.supplier_contact_id.data,
            'status_order': form.status_order.data,
            'expiry_date': (datetime.utcnow() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'create_time': current_time,
            'update_time': current_time,
        }
        enquiry_id = add_enquiry(enquiry_data)

        amount_enquiry = 0
        for enquiry_item in form.enquiry_items.entries:
            current_time = datetime.utcnow()
            enquiry_item_data = {
                'enquiry_id': enquiry_id,
                'uid': form.uid.data,
                'supplier_cid': form.supplier_cid.data,
                'supplier_company_name': get_supplier_row_by_id(form.supplier_cid.data).company_name,
                'enquiry_production_model': enquiry_item.form.enquiry_production_model.data,
                'enquiry_quantity': enquiry_item.form.enquiry_quantity.data,
                'production_id': enquiry_item.form.production_id.data,
                'production_brand': enquiry_item.form.production_brand.data,
                'production_model': enquiry_item.form.production_model.data,
                'production_sku': enquiry_item.form.production_sku.data,
                'note': enquiry_item.form.note.data,
                'delivery_time': enquiry_item.form.delivery_time.data,
                'quantity': enquiry_item.form.quantity.data,
                'unit_price': enquiry_item.form.unit_price.data,
                'status_ordered': enquiry_item.form.status_ordered.data,
                'create_time': current_time,
                'update_time': current_time,
            }

            # 新增
            add_enquiry_items(enquiry_item_data)
            amount_enquiry += (enquiry_item_data['quantity'] or 0) * (enquiry_item_data['unit_price'] or 0)

        # 更新询价
        enquiry_data = {
            'amount_production': amount_enquiry,
            'amount_enquiry': amount_enquiry,
            'update_time': current_time,
        }
        result = edit_enquiry(enquiry_id, enquiry_data)

        # todo 事务

        # 明细保存
        # 总表保存

        # 创建操作成功
        if result:
            flash(_('Add Success'), 'success')
            return redirect(request.args.get('next') or url_for('enquiry.lists'))
        # 创建操作失败
        else:
            flash(_('Add Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                **document_info
            )


@bp_enquiry.route('/<int:enquiry_id>/edit.html', methods=['GET', 'POST'])
@login_required
def edit(enquiry_id):
    """
    询价编辑
    """
    # 检查编辑权限
    # enquiry_item_edit_permission = EnquiryItemEditPermission(enquiry_id)
    # if not enquiry_item_edit_permission.can():
    #     abort(403)

    enquiry_info = get_enquiry_row_by_id(enquiry_id)
    # 检查资源是否存在
    if not enquiry_info:
        abort(404)
    # 检查资源是否删除
    if enquiry_info.status_delete == STATUS_DEL_OK:
        abort(410)

    template_name = 'enquiry/edit.html'

    # 加载编辑表单
    form = EnquiryEditForm(request.form)
    form.uid.choices = get_user_choices()
    form.status_order.choices = STATUS_ORDER_CHOICES

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('enquiry edit')

    # 进入编辑页面
    if request.method == 'GET':
        # 获取明细
        enquiry_items = get_enquiry_items_rows(enquiry_id=enquiry_id)
        # 表单赋值
        form.uid.data = enquiry_info.uid
        form.supplier_cid.data = enquiry_info.supplier_cid
        form.supplier_contact_id.data = enquiry_info.supplier_contact_id
        form.status_order.data = enquiry_info.status_order
        form.amount_enquiry.data = enquiry_info.amount_enquiry
        # form.enquiry_items = enquiry_items
        while len(form.enquiry_items) > 0:
            form.enquiry_items.pop_entry()
        for enquiry_item in enquiry_items:
            enquiry_item_form = EnquiryItemEditForm()
            enquiry_item_form.id = enquiry_item.id
            enquiry_item_form.enquiry_id = enquiry_item.enquiry_id
            enquiry_item_form.uid = enquiry_item.uid
            enquiry_item_form.enquiry_production_model = enquiry_item.enquiry_production_model
            enquiry_item_form.enquiry_quantity = enquiry_item.enquiry_quantity
            enquiry_item_form.production_id = enquiry_item.production_id
            enquiry_item_form.production_brand = enquiry_item.production_brand
            enquiry_item_form.production_model = enquiry_item.production_model
            enquiry_item_form.production_sku = enquiry_item.production_sku
            enquiry_item_form.note = enquiry_item.note
            enquiry_item_form.quantity = enquiry_item.quantity
            enquiry_item_form.unit_price = enquiry_item.unit_price
            enquiry_item_form.delivery_time = enquiry_item.delivery_time
            enquiry_item_form.status_ordered = enquiry_item.status_ordered
            form.enquiry_items.append_entry(enquiry_item_form)
        # 渲染页面
        return render_template(
            template_name,
            enquiry_id=enquiry_id,
            form=form,
            **document_info
        )

    # 处理编辑请求
    if request.method == 'POST':
        # 增删数据行不需要校验表单

        # 表单新增空行
        if form.data_line_add.data is not None:
            if form.enquiry_items.max_entries and len(
                    form.enquiry_items.entries) >= form.enquiry_items.max_entries:
                flash('最多创建%s条记录' % form.enquiry_items.max_entries, 'danger')
            else:
                form.enquiry_items.append_entry()

            return render_template(
                template_name,
                enquiry_id=enquiry_id,
                form=form,
                **document_info
            )
        # 表单删除一行
        if form.data_line_del.data is not None:
            if form.enquiry_items.min_entries and len(
                    form.enquiry_items.entries) <= form.enquiry_items.min_entries:
                flash('最少保留%s条记录' % form.enquiry_items.min_entries, 'danger')
            else:
                data_line_index = form.data_line_del.data
                form.enquiry_items.entries.pop(data_line_index)

            return render_template(
                template_name,
                enquiry_id=enquiry_id,
                form=form,
                **document_info
            )

        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Edit Failure'), 'danger')
            # flash(form.errors, 'danger')
            # flash(form.enquiry_items.errors, 'danger')
            return render_template(
                template_name,
                enquiry_id=enquiry_id,
                form=form,
                **document_info
            )
        # 表单校验成功

        # 获取明细
        enquiry_items = get_enquiry_items_rows(enquiry_id=enquiry_id)
        enquiry_items_ids = [item.id for item in enquiry_items]

        # 数据新增、数据删除、数据修改

        enquiry_items_ids_new = []
        amount_enquiry = 0
        for enquiry_item in form.enquiry_items.entries:
            # 错误
            if enquiry_item.form.id.data and enquiry_item.form.id.data not in enquiry_items_ids:
                continue

            enquiry_item_data = {
                'enquiry_id': enquiry_id,
                'uid': form.uid.data,
                'supplier_cid': form.supplier_cid.data,
                'supplier_company_name': get_supplier_row_by_id(form.supplier_cid.data).company_name,
                'enquiry_production_model': enquiry_item.form.enquiry_production_model.data,
                'enquiry_quantity': enquiry_item.form.enquiry_quantity.data,
                'production_id': enquiry_item.form.production_id.data,
                'production_brand': enquiry_item.form.production_brand.data,
                'production_model': enquiry_item.form.production_model.data,
                'production_sku': enquiry_item.form.production_sku.data,
                'note': enquiry_item.form.note.data,
                'delivery_time': enquiry_item.form.delivery_time.data,
                'quantity': enquiry_item.form.quantity.data,
                'unit_price': enquiry_item.form.unit_price.data,
                'status_ordered': enquiry_item.form.status_ordered.data,
            }

            if not enquiry_item.form.id.data:
                # 新增
                add_enquiry_items(enquiry_item_data)
                amount_enquiry += enquiry_item_data['quantity'] * enquiry_item_data['unit_price']
            else:
                # 修改
                edit_enquiry_items(enquiry_item.form.id.data, enquiry_item_data)
                amount_enquiry += enquiry_item_data['quantity'] * enquiry_item_data['unit_price']
                enquiry_items_ids_new.append(enquiry_item.form.id.data)
        # 删除
        enquiry_items_ids_del = list(set(enquiry_items_ids) - set(enquiry_items_ids_new))
        for enquiry_items_id in enquiry_items_ids_del:
            delete_enquiry_items(enquiry_items_id)

        # 更新询价
        current_time = datetime.utcnow()
        enquiry_data = {
            'supplier_cid': form.supplier_cid.data,
            'uid': form.uid.data,
            'supplier_contact_id': form.supplier_contact_id.data,
            'status_order': form.status_order.data,
            'amount_production': amount_enquiry,
            'amount_enquiry': amount_enquiry,
            'update_time': current_time,
        }
        result = edit_enquiry(enquiry_id, enquiry_data)

        # 编辑操作成功
        if result:
            flash(_('Edit Success'), 'success')
            return redirect(request.args.get('next') or url_for('enquiry.lists'))
        # 编辑操作失败
        else:
            flash(_('Edit Failure'), 'danger')
            return render_template(
                template_name,
                enquiry_id=enquiry_id,
                form=form,
                **document_info
            )


@bp_enquiry.route('/<int:enquiry_id>/preview.html')
@login_required
def preview(enquiry_id):
    """
    打印预览
    :param enquiry_id:
    :return:
    """
    enquiry_info = get_enquiry_row_by_id(enquiry_id)
    # 检查资源是否存在
    if not enquiry_info:
        abort(404)
    # 检查资源是否删除
    if enquiry_info.status_delete == STATUS_DEL_OK:
        abort(410)

    enquiry_print_date = time_utc_to_local(enquiry_info.update_time).strftime('%Y-%m-%d')
    enquiry_code = '%s%s' % (g.ENQUIRIES_PREFIX, time_utc_to_local(enquiry_info.create_time).strftime('%y%m%d%H%M%S'))

    # 获取渠道公司信息
    supplier_info = get_supplier_row_by_id(enquiry_info.supplier_cid)

    # 获取渠道联系方式
    supplier_contact_info = get_supplier_contact_row_by_id(enquiry_info.supplier_contact_id)

    # 获取询价人员信息
    user_info = get_user_row_by_id(enquiry_info.uid)

    enquiry_items = get_enquiry_items_rows(enquiry_id=enquiry_id)

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('enquiry edit')

    template_name = 'enquiry/preview.html'

    return render_template(
        template_name,
        enquiry_id=enquiry_id,
        enquiry_info=enquiry_info,
        supplier_info=supplier_info,
        supplier_contact_info=supplier_contact_info,
        user_info=user_info,
        enquiry_items=enquiry_items,
        enquiry_print_date=enquiry_print_date,
        enquiry_code=enquiry_code,
        **document_info
    )


@bp_enquiry.route('/<int:enquiry_id>.pdf')
@login_required
def pdf(enquiry_id):
    """
    文件下载
    :param enquiry_id:
    :return:
    """
    enquiry_info = get_enquiry_row_by_id(enquiry_id)
    # 检查资源是否存在
    if not enquiry_info:
        abort(404)
    # 检查资源是否删除
    if enquiry_info.status_delete == STATUS_DEL_OK:
        abort(410)

    enquiry_print_date = time_utc_to_local(enquiry_info.update_time).strftime('%Y-%m-%d')
    enquiry_code = '%s%s' % (g.ENQUIRIES_PREFIX, time_utc_to_local(enquiry_info.create_time).strftime('%y%m%d%H%M%S'))

    # 获取客户公司信息
    supplier_info = get_supplier_row_by_id(enquiry_info.supplier_cid)

    # 获取客户联系方式
    supplier_contact_info = get_supplier_contact_row_by_id(enquiry_info.supplier_contact_id)

    # 获取询价人员信息
    user_info = get_user_row_by_id(enquiry_info.uid)

    enquiry_items = get_enquiry_items_rows(enquiry_id=enquiry_id)

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('enquiry edit')

    template_name = 'enquiry/pdf.html'

    html = render_template(
        template_name,
        enquiry_id=enquiry_id,
        enquiry_info=enquiry_info,
        supplier_info=supplier_info,
        supplier_contact_info=supplier_contact_info,
        user_info=user_info,
        enquiry_items=enquiry_items,
        enquiry_print_date=enquiry_print_date,
        enquiry_code=enquiry_code,
        **document_info
    )
    # return html
    return render_pdf(
        html=HTML(string=html),
        stylesheets=[CSS(string='@page {size:A4; margin:35px;}')],
        download_filename='询价单.pdf'.encode('utf-8')
    )


@bp_enquiry.route('/ajax/del', methods=['GET', 'POST'])
@login_required
def ajax_delete():
    """
    询价删除
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
    enquiry_id = request.args.get('enquiry_id', 0, type=int)
    if not enquiry_id:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查删除权限
    enquiry_item_del_permission = EnquiryItemDelPermission(enquiry_id)
    if not enquiry_item_del_permission.can():
        ext_msg = _('Permission Denied')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    enquiry_info = get_enquiry_row_by_id(enquiry_id)
    # 检查资源是否存在
    if not enquiry_info:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)
    # 检查资源是否删除
    if enquiry_info.status_delete == STATUS_DEL_OK:
        ext_msg = _('Already deleted')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_success_msg)

    current_time = datetime.utcnow()
    enquiry_data = {
        'status_delete': STATUS_DEL_OK,
        'delete_time': current_time,
        'update_time': current_time,
    }
    result = edit_enquiry(enquiry_id, enquiry_data)
    if result:
        # 发送删除信号
        signal_data = {
            'enquiry_id': enquiry_id,
            'status_delete': STATUS_DEL_OK,
            'current_time': current_time,
        }
        signal_enquiry_status_delete.send(app, **signal_data)

        ajax_success_msg['msg'] = _('Del Success')
        return jsonify(ajax_success_msg)
    else:
        ajax_failure_msg['msg'] = _('Del Failure')
        return jsonify(ajax_failure_msg)


@bp_enquiry.route('/ajax/stats', methods=['GET', 'POST'])
@login_required
def ajax_stats():
    """
    获取询价统计
    :return:
    """
    time_based = request.args.get('time_based', 'hour')
    result_enquiry_middleman = enquiry_middleman_stats(time_based)
    result_enquiry_end_user = enquiry_end_user_stats(time_based)

    line_chart_data = {
        'labels': [label for label, _ in result_enquiry_middleman],
        'datasets': [
            {
                'label': '同行',
                'backgroundColor': 'rgba(220,220,220,0.5)',
                'borderColor': 'rgba(220,220,220,1)',
                'pointBackgroundColor': 'rgba(220,220,220,1)',
                'pointBorderColor': '#fff',
                'pointBorderWidth': 2,
                'data': [data for _, data in result_enquiry_middleman]
            },
            {
                'label': '终端',
                'backgroundColor': 'rgba(151,187,205,0.5)',
                'borderColor': 'rgba(151,187,205,1)',
                'pointBackgroundColor': 'rgba(151,187,205,1)',
                'pointBorderColor': '#fff',
                'pointBorderWidth': 2,
                'data': [data for _, data in result_enquiry_end_user]
            }
        ]
    }
    return json.dumps(line_chart_data, default=json_default)


@bp_enquiry.route('/stats.html')
@login_required
@permission_enquiry_section_stats.require(http_exception=403)
def stats():
    """
    询价统计
    :return:
    """
    # 统计数据
    time_based = request.args.get('time_based', 'hour')
    if time_based not in ['hour', 'date', 'month']:
        abort(404)
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('enquiry stats')
    # 渲染模板
    return render_template(
        'enquiry/stats.html',
        time_based=time_based,
        **document_info
    )


@bp_enquiry.route('/<int:enquiry_id>/stats.html')
@login_required
@permission_enquiry_section_stats.require(http_exception=403)
def stats_item(enquiry_id):
    """
    询价统计明细
    :param enquiry_id:
    :return:
    """
    enquiry_info = get_enquiry_row_by_id(enquiry_id)
    # 检查资源是否存在
    if not enquiry_info:
        abort(404)
    # 检查资源是否删除
    if enquiry_info.status_delete == STATUS_DEL_OK:
        abort(410)

    # 统计数据
    enquiry_stats_item_info = get_enquiry_row_by_id(enquiry_id)
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('enquiry stats item')
    # 渲染模板
    return render_template(
        'enquiry/stats_item.html',
        enquiry_stats_item_info=enquiry_stats_item_info,
        **document_info
    )
