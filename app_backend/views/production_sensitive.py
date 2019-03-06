#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: production_sensitive_sensitive.py
@time: 2018-08-14 14:55
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
from flask_login import login_required
from six import text_type

from app_backend import app
from app_backend import excel
from app_backend.api.customer import get_customer_row_by_id
from app_backend.api.production_sensitive import (
    get_production_sensitive_pagination,
    get_production_sensitive_row_by_id,
    add_production_sensitive,
    edit_production_sensitive,
    get_distinct_production_sensitive_brand,
    # production_sensitive_current_stats,
    # production_sensitive_former_stats,
)
from app_backend.api.production_sensitive import (
    get_production_sensitive_rows,
)
from app_backend.api.user import get_user_choices
from app_backend.forms.production_sensitive import (
    ProductionSensitiveSearchForm,
    ProductionSensitiveAddForm,
    ProductionSensitiveEditForm,
)
from app_backend.forms.production import ProductionSelectForm
from app_backend.models.bearing_project import ProductionSensitive
from app_backend.permissions import (
    permission_production_section_add,
    permission_production_section_search,
    permission_production_section_export,
    permission_production_section_stats,
    permission_role_administrator,
)
from app_common.maps.default import default_search_choices_str, default_search_choice_option_str
from app_common.maps.status_delete import (
    STATUS_DEL_OK,
    STATUS_DEL_NO,
)
from app_common.maps.type_role import TYPE_ROLE_MANAGER
from app_common.tools import json_default

# 定义蓝图
bp_production_sensitive = Blueprint('production_sensitive', __name__, url_prefix='/production_sensitive')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
PER_PAGE_BACKEND_MODAL = app.config.get('PER_PAGE_BACKEND_MODAL', 10)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


def get_production_sensitive_brand_choices():
    production_sensitive_brand_list = copy(default_search_choices_str)
    distinct_brand = get_distinct_production_sensitive_brand(status_delete=STATUS_DEL_NO)
    production_sensitive_brand_list.extend([(brand, brand) for brand in distinct_brand])
    return production_sensitive_brand_list


@bp_production_sensitive.route('/lists.html', methods=['GET', 'POST'])
@login_required
@permission_production_section_search.require(http_exception=403)
def lists():
    """
    敏感产品列表
    :return:
    """
    template_name = 'production/sensitive/lists.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('production sensitive lists')

    # 搜索条件
    form = ProductionSensitiveSearchForm(request.form)
    form.production_brand.choices = get_production_sensitive_brand_choices()
    # app.logger.info('')

    search_condition = [
        ProductionSensitive.status_delete == STATUS_DEL_NO,
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
                search_condition.append(ProductionSensitive.customer_cid == form.customer_cid.data)
            if form.production_brand.data != default_search_choice_option_str:
                search_condition.append(ProductionSensitive.production_brand == form.production_brand.data)
            if form.production_model.data:
                search_condition.append(ProductionSensitive.production_model.like('%%%s%%' % form.production_model.data))
        # 处理导出
        if form.op.data == 1:
            # 检查导出权限
            if not permission_production_section_export.can():
                abort(403)
            column_names = ProductionSensitive.__table__.columns.keys()
            query_sets = get_production_sensitive_rows(*search_condition)

            return excel.make_response_from_query_sets(
                query_sets=query_sets,
                column_names=column_names,
                file_type='csv',
                file_name='%s.csv' % _('production sensitive lists')
            )
        # 批量删除
        if form.op.data == 2:
            production_sensitive_ids = request.form.getlist('production_sensitive_id')
            # 检查删除权限
            if not permission_role_administrator.can():
                ext_msg = _('Permission Denied')
                flash(_('Del Failure, %(ext_msg)s', ext_msg=ext_msg), 'danger')
            else:
                result_total = True
                for production_sensitive_id in production_sensitive_ids:
                    current_time = datetime.utcnow()
                    production_sensitive_data = {
                        'status_delete': STATUS_DEL_OK,
                        'delete_time': current_time,
                        'update_time': current_time,
                    }
                    result = edit_production_sensitive(production_sensitive_id, production_sensitive_data)
                    result_total = result_total and result
                if result_total:
                    flash(_('Del Success'), 'success')
                else:
                    flash(_('Del Failure'), 'danger')
    # 翻页数据
    pagination = get_production_sensitive_pagination(form.page.data, PER_PAGE_BACKEND, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )


@bp_production_sensitive.route('/add.html', methods=['GET', 'POST'])
@login_required
# @permission_production_sensitive_section_add.require(http_exception=403)
def add():
    """
    创建敏感产品
    :return:
    """
    template_name = 'production/sensitive/add.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('production sensitive add')

    # 加载创建表单
    form = ProductionSensitiveAddForm(request.form)

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
        production_sensitive_data = {
            'customer_cid': form.customer_cid.data,
            'customer_company_name': get_customer_row_by_id(form.customer_cid.data).company_name,
            'production_id': form.production_id.data,
            'production_brand': form.production_brand.data.upper(),
            'production_model': form.production_model.data.upper(),
            'production_sku': form.production_sku.data,
            'note': form.note.data,
            'create_time': current_time,
            'update_time': current_time,
        }
        result = add_production_sensitive(production_sensitive_data)
        # 创建操作成功
        if result:
            flash(_('Add Success'), 'success')
            return redirect(request.args.get('next') or url_for('production_sensitive.lists'))
        # 创建操作失败
        else:
            flash(_('Add Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                **document_info
            )


@bp_production_sensitive.route('/<int:production_sensitive_id>/edit.html', methods=['GET', 'POST'])
@login_required
# @permission_role_administrator.require(http_exception=403)
def edit(production_sensitive_id):
    """
    敏感产品编辑
    """
    production_sensitive_info = get_production_sensitive_row_by_id(production_sensitive_id)
    # 检查资源是否存在
    if not production_sensitive_info:
        abort(404)
    # 检查资源是否删除
    if production_sensitive_info.status_delete == STATUS_DEL_OK:
        abort(410)

    template_name = 'production/sensitive/edit.html'

    # 加载编辑表单
    form = ProductionSensitiveEditForm(request.form)

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('production sensitive edit')

    # 进入编辑页面
    if request.method == 'GET':
        # 表单赋值
        form.id.data = production_sensitive_info.id
        form.customer_cid.data = production_sensitive_info.customer_cid
        form.customer_company_name.data = production_sensitive_info.customer_company_name
        form.production_id.data = production_sensitive_info.production_id
        form.production_brand.data = production_sensitive_info.production_brand
        form.production_model.data = production_sensitive_info.production_model
        form.production_sku.data = production_sensitive_info.production_sku
        form.note.data = production_sensitive_info.note
        form.create_time.data = production_sensitive_info.create_time
        form.update_time.data = production_sensitive_info.update_time
        # 渲染页面
        return render_template(
            template_name,
            production_sensitive_id=production_sensitive_id,
            form=form,
            **document_info
        )

    # 处理编辑请求
    if request.method == 'POST':
        # 表单校验失败
        if production_sensitive_id != form.id.data or not form.validate_on_submit():
            flash(_('Edit Failure'), 'danger')
            return render_template(
                template_name,
                production_sensitive_id=production_sensitive_id,
                form=form,
                **document_info
            )
        # 表单校验成功
        current_time = datetime.utcnow()
        production_sensitive_data = {
            'customer_cid': form.customer_cid.data,
            'customer_company_name': get_customer_row_by_id(form.customer_cid.data).company_name,
            'production_id': form.production_id.data,
            'production_brand': form.production_brand.data.upper(),
            'production_model': form.production_model.data.upper(),
            'production_sku': form.production_sku.data,
            'note': form.note.data,
            'update_time': current_time,
        }
        result = edit_production_sensitive(production_sensitive_id, production_sensitive_data)
        # 编辑操作成功
        if result:
            flash(_('Edit Success'), 'success')
            return redirect(request.args.get('next') or url_for('production_sensitive.lists'))
        # 编辑操作失败
        else:
            flash(_('Edit Failure'), 'danger')
            return render_template(
                template_name,
                production_sensitive_id=production_sensitive_id,
                form=form,
                **document_info
            )


@bp_production_sensitive.route('/ajax/del', methods=['GET', 'POST'])
@login_required
def ajax_delete():
    """
    敏感产品删除
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
    production_sensitive_id = request.args.get('production_sensitive_id', 0, type=int)
    if not production_sensitive_id:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查删除权限
    if not permission_role_administrator.can():
        ext_msg = _('Permission Denied')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    production_sensitive_info = get_production_sensitive_row_by_id(production_sensitive_id)
    # 检查资源是否存在
    if not production_sensitive_info:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)
    # 检查资源是否删除
    if production_sensitive_info.status_delete == STATUS_DEL_OK:
        ext_msg = _('Already deleted')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    current_time = datetime.utcnow()
    production_data = {
        'status_delete': STATUS_DEL_OK,
        'delete_time': current_time,
        'update_time': current_time,
    }
    result = edit_production_sensitive(production_sensitive_id, production_data)
    if result:
        ajax_success_msg['msg'] = _('Del Success')
        return jsonify(ajax_success_msg)
    else:
        ajax_failure_msg['msg'] = _('Del Failure')
        return jsonify(ajax_failure_msg)
