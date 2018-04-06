#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: product.py
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
from flask_login import login_required

from app_backend import app
from app_backend import excel
from app_backend.api.product import (
    get_product_pagination,
    get_product_row_by_id,
    add_product,
    edit_product,
    # product_current_stats,
    # product_former_stats,
)
from app_backend.api.product import (
    get_product_rows,
    get_distinct_brand,
)
from app_backend.forms.product import (
    ProductSearchForm,
    ProductAddForm,
    ProductEditForm,
)
from app_backend.models.bearing_project import Product
from app_backend.permissions import (
    permission_product_section_add,
    permission_product_section_search,
    permission_product_section_export,
    permission_product_section_stats,
    permission_role_administrator,
)
from app_common.maps.default import default_choices_str, default_choice_option_str
from app_common.maps.status_delete import (
    STATUS_DEL_OK,
)
from app_common.maps.type_role import TYPE_ROLE_MANAGER
from app_common.tools import json_default

# 定义蓝图
bp_product = Blueprint('product', __name__, url_prefix='/product')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


def get_product_brand_choices():
    product_brand_list = copy(default_choices_str)
    distinct_brand = get_distinct_brand()
    product_brand_list.extend([(brand, brand) for brand in distinct_brand])
    return product_brand_list


@bp_product.route('/lists.html', methods=['GET', 'POST'])
@bp_product.route('/lists/<int:page>.html', methods=['GET', 'POST'])
@login_required
@permission_product_section_search.require(http_exception=403)
def lists(page=1):
    """
    产品列表
    :param page:
    :return:
    """
    template_name = 'product/lists.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('product lists')

    # 搜索条件
    form = ProductSearchForm(request.form)
    form.product_brand.choices = get_product_brand_choices()
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
            if form.product_brand.data != default_choice_option_str:
                search_condition.append(Product.product_brand == form.product_brand.data)
            if form.product_model.data:
                search_condition.append(Product.product_model == form.product_model.data)
        # 处理导出
        if form.op.data == 1:
            # 检查导出权限
            if not permission_product_section_export.can():
                abort(403)
            column_names = Product.__table__.columns.keys()
            query_sets = get_product_rows(*search_condition)

            return excel.make_response_from_query_sets(
                query_sets=query_sets,
                column_names=column_names,
                file_type='csv',
                file_name='%s.csv' % _('product lists')
            )
    # 翻页数据
    pagination = get_product_pagination(page, PER_PAGE_BACKEND, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )


@bp_product.route('/<int:product_id>/info.html')
@login_required
def info(product_id):
    """
    产品详情
    :param product_id:
    :return:
    """
    # 详情数据
    product_info = get_product_row_by_id(product_id)
    # 检查资源是否存在
    if not product_info:
        abort(404)
    # 检查资源是否删除
    if product_info.status_delete == STATUS_DEL_OK:
        abort(410)
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('product info')
    # 渲染模板
    return render_template('product/info.html', product_info=product_info, **document_info)


@bp_product.route('/add.html', methods=['GET', 'POST'])
@login_required
@permission_product_section_add.require(http_exception=403)
def add():
    """
    创建产品
    :return:
    """
    template_name = 'product/add.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('product add')

    # 加载创建表单
    form = ProductAddForm(request.form)

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
        product_data = {
            'product_brand': form.product_brand.data,
            'product_model': form.product_model.data,
            'note': form.note.data,
            'create_time': current_time,
            'update_time': current_time,
        }
        result = add_product(product_data)
        # 创建操作成功
        if result:
            flash(_('Add Success'), 'success')
            return redirect(request.args.get('next') or url_for('product.lists'))
        # 创建操作失败
        else:
            flash(_('Add Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                **document_info
            )


@bp_product.route('/<int:product_id>/edit.html', methods=['GET', 'POST'])
@login_required
@permission_role_administrator.require(http_exception=403)
def edit(product_id):
    """
    产品编辑
    """
    product_info = get_product_row_by_id(product_id)
    # 检查资源是否存在
    if not product_info:
        abort(404)
    # 检查资源是否删除
    if product_info.status_delete == STATUS_DEL_OK:
        abort(410)

    template_name = 'product/edit.html'

    # 加载编辑表单
    form = ProductEditForm(request.form)

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('product edit')

    # 进入编辑页面
    if request.method == 'GET':
        # 表单赋值
        form.product_brand.data = product_info.product_brand
        form.product_model.data = product_info.product_model
        form.note.data = product_info.note
        form.create_time.data = product_info.create_time
        form.update_time.data = product_info.update_time
        # 渲染页面
        return render_template(
            template_name,
            product_id=product_id,
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
                product_id=product_id,
                form=form,
                **document_info
            )
        # 表单校验成功
        current_time = datetime.utcnow()
        product_data = {
            'product_brand': form.product_brand.data,
            'product_model': form.product_model.data,
            'note': form.note.data,
            'update_time': current_time,
        }
        result = edit_product(product_id, product_data)
        # 编辑操作成功
        if result:
            flash(_('Edit Success'), 'success')
            return redirect(request.args.get('next') or url_for('product.lists'))
        # 编辑操作失败
        else:
            flash(_('Edit Failure'), 'danger')
            return render_template(
                template_name,
                product_id=product_id,
                form=form,
                **document_info
            )


@bp_product.route('/ajax/del', methods=['GET', 'POST'])
@login_required
def ajax_delete():
    """
    产品删除
    :return:
    """
    ajax_success_msg = AJAX_SUCCESS_MSG.copy()
    ajax_failure_msg = AJAX_FAILURE_MSG.copy()

    # 检查请求方法
    if not (request.method == 'GET' and request.is_xhr):
        ajax_failure_msg['msg'] = _('Del Failure')  # Method Not Allowed
        return jsonify(ajax_failure_msg)

    # 检查请求参数
    product_id = request.args.get('product_id', 0, type=int)
    if not product_id:
        ajax_failure_msg['msg'] = _('Del Failure')  # ID does not exist
        return jsonify(ajax_failure_msg)

    # 检查删除权限
    if not permission_role_administrator.can():
        ajax_failure_msg['msg'] = _('Del Failure')  # Permission Denied
        return jsonify(ajax_failure_msg)

    product_info = get_product_row_by_id(product_id)
    # 检查资源是否存在
    if not product_info:
        ajax_failure_msg['msg'] = _('Del Failure')  # ID does not exist
        return jsonify(ajax_failure_msg)
    # 检查资源是否删除
    if product_info.status_delete == STATUS_DEL_OK:
        ajax_success_msg['msg'] = _('Del Success')  # Already deleted
        return jsonify(ajax_success_msg)

    current_time = datetime.utcnow()
    product_data = {
        'status_delete': STATUS_DEL_OK,
        'delete_time': current_time,
        'update_time': current_time,
    }
    result = edit_product(product_id, product_data)
    if result:
        ajax_success_msg['msg'] = _('Del Success')
        return jsonify(ajax_success_msg)
    else:
        ajax_failure_msg['msg'] = _('Del Failure')
        return jsonify(ajax_failure_msg)


# @bp_product.route('/ajax/stats', methods=['GET', 'POST'])
# @login_required
# def ajax_stats():
#     """
#     获取产品统计
#     :return:
#     """
#     time_based = request.args.get('time_based', 'hour')
#     result_product_current = product_current_stats(time_based)
#     result_product_former = product_former_stats(time_based)
#
#     line_chart_data = {
#         'labels': [label for label, _ in result_product_current],
#         'datasets': [
#             {
#                 'label': '在职',
#                 'backgroundColor': 'rgba(220,220,220,0.5)',
#                 'borderColor': 'rgba(220,220,220,1)',
#                 'pointBackgroundColor': 'rgba(220,220,220,1)',
#                 'pointBorderColor': '#fff',
#                 'pointBorderWidth': 2,
#                 'data': [data for _, data in result_product_current]
#             },
#             {
#                 'label': '离职',
#                 'backgroundColor': 'rgba(151,187,205,0.5)',
#                 'borderColor': 'rgba(151,187,205,1)',
#                 'pointBackgroundColor': 'rgba(151,187,205,1)',
#                 'pointBorderColor': '#fff',
#                 'pointBorderWidth': 2,
#                 'data': [data for _, data in result_product_former]
#             }
#         ]
#     }
#     return json.dumps(line_chart_data, default=json_default)
#
#
# @bp_product.route('/stats.html')
# @login_required
# @permission_product_section_stats.require(http_exception=403)
# def stats():
#     """
#     产品统计
#     :return:
#     """
#     # 统计数据
#     time_based = request.args.get('time_based', 'hour')
#     if time_based not in ['hour', 'date', 'month']:
#         abort(404)
#     # 文档信息
#     document_info = DOCUMENT_INFO.copy()
#     document_info['TITLE'] = _('product stats')
#     # 渲染模板
#     return render_template(
#         'product/stats.html',
#         time_based=time_based,
#         **document_info
#     )
#
#
# @bp_product.route('/<int:product_id>/stats.html')
# @login_required
# @permission_product_section_stats.require(http_exception=403)
# def stats_item(product_id):
#     """
#     产品统计明细
#     :param product_id:
#     :return:
#     """
#     product_info = get_product_row_by_id(product_id)
#     # 检查资源是否存在
#     if not product_info:
#         abort(404)
#     # 检查资源是否删除
#     if product_info.status_delete == STATUS_DEL_OK:
#         abort(410)
#
#     # 统计数据
#     product_stats_item_info = get_product_row_by_id(product_id)
#     # 文档信息
#     document_info = DOCUMENT_INFO.copy()
#     document_info['TITLE'] = _('product stats item')
#     # 渲染模板
#     return render_template(
#         'product/stats_item.html',
#         product_stats_item_info=product_stats_item_info,
#         **document_info
#     )
