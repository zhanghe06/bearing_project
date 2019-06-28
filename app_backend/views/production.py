#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: production.py
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
from six import text_type

from app_backend import app
from app_backend import excel
from app_backend.api.production import get_production_choices
from app_backend.api.production import (
    get_production_pagination,
    get_production_row_by_id,
    add_production,
    edit_production,
    # production_current_stats,
    # production_former_stats,
)
from app_backend.api.production import (
    get_production_rows,
    get_distinct_production_brand,
)
from app_backend.api.quotation_items import count_quotation_items
from app_backend.api.production_sensitive import count_production_sensitive
from app_backend.forms.production import (
    ProductionSearchForm,
    ProductionAddForm,
    ProductionEditForm,
    ProductionSelectForm)
from app_backend.models.bearing_project import Production
from app_backend.permissions import permission_role_administrator
from app_backend.permissions.production import (
    permission_production_section_add,
    permission_production_section_search,
    permission_production_section_export,
    permission_production_section_stats,
)
from app_common.maps.default import default_search_choices_str, default_search_choice_option_str
from app_common.maps.status_delete import (
    STATUS_DEL_OK,
    STATUS_DEL_NO,
)
from app_common.maps.type_role import TYPE_ROLE_MANAGER
from app_common.tools import json_default

# 定义蓝图
bp_production = Blueprint('production', __name__, url_prefix='/production')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
PER_PAGE_BACKEND_MODAL = app.config.get('PER_PAGE_BACKEND_MODAL', 10)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


def get_production_brand_choices():
    production_brand_list = copy(default_search_choices_str)
    distinct_brand = get_distinct_production_brand(status_delete=STATUS_DEL_NO)
    production_brand_list.extend([(brand, brand) for brand in distinct_brand])
    return production_brand_list


@bp_production.route('/lists.html', methods=['GET', 'POST'])
@login_required
@permission_production_section_search.require(http_exception=403)
def lists():
    """
    产品列表
    :return:
    """
    template_name = 'production/lists.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('production lists')

    # 搜索条件
    form = ProductionSearchForm(request.form)
    form.production_brand.choices = get_production_brand_choices()
    # app.logger.info('')

    search_condition = [
        Production.status_delete == STATUS_DEL_NO,
    ]
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Search Failure'), 'danger')
            # 单独处理csrf_token
            if hasattr(form, 'csrf_token') and getattr(form, 'csrf_token').errors:
                map(lambda x: flash(x, 'danger'), form.csrf_token.errors)
        else:
            if form.production_brand.data != default_search_choice_option_str:
                search_condition.append(Production.production_brand == form.production_brand.data)
            if form.production_model.data:
                search_condition.append(Production.production_model.like('%%%s%%' % form.production_model.data))
        # 处理导出
        if form.op.data == 1:
            # 检查导出权限
            # if not permission_production_section_export.can():
            #     abort(403)
            column_names = Production.__table__.columns.keys()
            query_sets = get_production_rows(*search_condition)

            return excel.make_response_from_query_sets(
                query_sets=query_sets,
                column_names=column_names,
                file_type='csv',
                file_name='%s.csv' % _('production lists')
            )
        # 批量删除
        if form.op.data == 2:
            production_ids = request.form.getlist('production_id')
            # 检查删除权限
            if not permission_role_administrator.can():
                ext_msg = _('Permission Denied')
                flash(_('Del Failure, %(ext_msg)s', ext_msg=ext_msg), 'danger')
            else:
                permitted = True
                for production_id in production_ids:
                    # 检查是否正在使用
                    # 报价、订单、敏感型号
                    if count_quotation_items(**{'production_id': production_id, 'status_delete': STATUS_DEL_NO}):
                        ext_msg = _('Currently In Use')
                        flash(_('Del Failure, %(ext_msg)s', ext_msg=ext_msg), 'danger')
                        permitted = False
                        break
                    if count_production_sensitive(**{'production_id': production_id, 'status_delete': STATUS_DEL_NO}):
                        ext_msg = _('Currently In Use')
                        flash(_('Del Failure, %(ext_msg)s', ext_msg=ext_msg), 'danger')
                        permitted = False
                        break
                if permitted:
                    result_total = True
                    for production_id in production_ids:
                        current_time = datetime.utcnow()
                        production_data = {
                            'status_delete': STATUS_DEL_OK,
                            'delete_time': current_time,
                            'update_time': current_time,
                        }
                        result = edit_production(production_id, production_data)
                        result_total = result_total and result
                    if result_total:
                        flash(_('Del Success'), 'success')
                    else:
                        flash(_('Del Failure'), 'danger')

    # 翻页数据
    pagination = get_production_pagination(form.page.data, PER_PAGE_BACKEND, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )


@bp_production.route('/search.html', methods=['GET', 'POST'])
@login_required
@permission_production_section_search.require(http_exception=403)
def search():
    """
    产品搜索
    :return:
    """
    template_name = 'production/search_modal.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('Production Search')

    # 搜索条件
    form = ProductionSearchForm(request.form)
    form.production_brand.choices = get_production_brand_choices()
    # app.logger.info('')

    search_condition = [
        Production.status_delete == STATUS_DEL_NO,
    ]
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Search Failure'), 'danger')
            # 单独处理csrf_token
            if hasattr(form, 'csrf_token') and getattr(form, 'csrf_token').errors:
                map(lambda x: flash(x, 'danger'), form.csrf_token.errors)
        else:
            if form.production_brand.data != default_search_choice_option_str:
                search_condition.append(Production.production_brand == form.production_brand.data)
            if form.production_model.data:
                search_condition.append(Production.production_model.like('%s%%' % form.production_model.data))
    # 翻页数据
    pagination = get_production_pagination(form.page.data, PER_PAGE_BACKEND_MODAL, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )


@bp_production.route('/<int:production_id>/info.html')
@login_required
def info(production_id):
    """
    产品详情
    :param production_id:
    :return:
    """
    # 详情数据
    production_info = get_production_row_by_id(production_id)
    # 检查资源是否存在
    if not production_info:
        abort(404)
    # 检查资源是否删除
    if production_info.status_delete == STATUS_DEL_OK:
        abort(410)
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('production info')
    # 渲染模板
    return render_template('production/info.html', production_info=production_info, **document_info)


@bp_production.route('/add.html', methods=['GET', 'POST'])
@login_required
@permission_production_section_add.require(http_exception=403)
def add():
    """
    创建产品
    :return:
    """
    template_name = 'production/add.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('production add')

    # 加载创建表单
    form = ProductionAddForm(request.form)

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
        production_data = {
            'production_brand': form.production_brand.data.upper(),
            'production_model': form.production_model.data.upper(),
            'production_sku': form.production_sku.data,
            'ind': form.ind.data,
            'oud': form.oud.data,
            'wid': form.wid.data,
            'note': form.note.data,
            'create_time': current_time,
            'update_time': current_time,
        }
        result = add_production(production_data)
        # 创建操作成功
        if result:
            flash(_('Add Success'), 'success')
            return redirect(request.args.get('next') or url_for('production.lists'))
        # 创建操作失败
        else:
            flash(_('Add Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                **document_info
            )


@bp_production.route('/<int:production_id>/edit.html', methods=['GET', 'POST'])
@login_required
# @permission_role_administrator.require(http_exception=403)
def edit(production_id):
    """
    产品编辑
    """
    production_info = get_production_row_by_id(production_id)
    # 检查资源是否存在
    if not production_info:
        abort(404)
    # 检查资源是否删除
    if production_info.status_delete == STATUS_DEL_OK:
        abort(410)

    template_name = 'production/edit.html'

    # 加载编辑表单
    form = ProductionEditForm(request.form)

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('production edit')

    # 进入编辑页面
    if request.method == 'GET':
        # 表单赋值
        form.id.data = production_info.id
        form.production_brand.data = production_info.production_brand
        form.production_model.data = production_info.production_model
        form.production_sku.data = production_info.production_sku
        form.ind.data = production_info.ind
        form.oud.data = production_info.oud
        form.wid.data = production_info.wid
        form.note.data = production_info.note
        form.create_time.data = production_info.create_time
        form.update_time.data = production_info.update_time
        # 渲染页面
        return render_template(
            template_name,
            production_id=production_id,
            form=form,
            **document_info
        )

    # 处理编辑请求
    if request.method == 'POST':
        # 表单校验失败
        if production_id != form.id.data or not form.validate_on_submit():
            flash(_('Edit Failure'), 'danger')
            return render_template(
                template_name,
                production_id=production_id,
                form=form,
                **document_info
            )
        # 表单校验成功
        current_time = datetime.utcnow()
        production_data = {
            'production_brand': form.production_brand.data.upper(),
            'production_model': form.production_model.data.upper(),
            'production_sku': form.production_sku.data,
            'ind': form.ind.data,
            'oud': form.oud.data,
            'wid': form.wid.data,
            'note': form.note.data,
            'update_time': current_time,
        }
        result = edit_production(production_id, production_data)
        # 编辑操作成功
        if result:
            flash(_('Edit Success'), 'success')
            return redirect(request.args.get('next') or url_for('production.lists'))
        # 编辑操作失败
        else:
            flash(_('Edit Failure'), 'danger')
            return render_template(
                template_name,
                production_id=production_id,
                form=form,
                **document_info
            )


@bp_production.route('/ajax/del', methods=['GET', 'POST'])
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
        ext_msg = _('Method Not Allowed')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查请求参数
    production_id = request.args.get('production_id', 0, type=int)
    if not production_id:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查删除权限
    if not permission_role_administrator.can():
        ext_msg = _('Permission Denied')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    production_info = get_production_row_by_id(production_id)
    # 检查资源是否存在
    if not production_info:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)
    # 检查资源是否删除
    if production_info.status_delete == STATUS_DEL_OK:
        ext_msg = _('Already deleted')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)
    # 检查是否正在使用
    # 报价、订单、敏感型号
    if count_quotation_items(**{'production_id': production_id, 'status_delete': STATUS_DEL_NO}):
        ext_msg = _('Currently In Use')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)
    if count_production_sensitive(**{'production_id': production_id, 'status_delete': STATUS_DEL_NO}):
        ext_msg = _('Currently In Use')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    current_time = datetime.utcnow()
    production_data = {
        'status_delete': STATUS_DEL_OK,
        'delete_time': current_time,
        'update_time': current_time,
    }
    result = edit_production(production_id, production_data)
    if result:
        ajax_success_msg['msg'] = _('Del Success')
        return jsonify(ajax_success_msg)
    else:
        ajax_failure_msg['msg'] = _('Del Failure')
        return jsonify(ajax_failure_msg)


@bp_production.route('/ajax/search/modal', methods=['GET', 'POST'])
@login_required
def ajax_search_modal():
    """
    动态搜索产品
    :return:
    """
    ajax_success_msg = AJAX_SUCCESS_MSG.copy()
    ajax_failure_msg = AJAX_FAILURE_MSG.copy()

    # # 检查请求方法
    # if not (request.method == 'GET' and request.is_xhr):
    #     ext_msg = _('Method Not Allowed')
    #     ajax_failure_msg['msg'] = _('Search Failure, %(ext_msg)s', ext_msg=ext_msg)
    #     return jsonify(ajax_failure_msg)
    #
    # # 检查请求参数
    keywords = request.args.get('keywords', '', type=text_type)
    # if not keywords:
    #     ext_msg = _('Args is empty')
    #     ajax_failure_msg['msg'] = _('Search Failure, %(ext_msg)s', ext_msg=ext_msg)
    #     return jsonify(ajax_failure_msg)

    # 执行搜索

    production_choices = get_production_choices(keywords)

    form_modal = ProductionSelectForm(request.form)
    form_modal.production_model.choices = production_choices

    template_name = '_modal_production_select_form.html'
    return render_template(
        template_name,
        form_modal=form_modal,
    )

    # if production_choices:
    #     ajax_success_msg['data'] = production_choices
    #     ajax_success_msg['msg'] = _('Search Success')
    #     return jsonify(ajax_success_msg)
    # else:
    #     ajax_failure_msg['msg'] = _('Search Failure')
    #     return jsonify(ajax_failure_msg)


@bp_production.route('/ajax/info', methods=['GET', 'POST'])
@login_required
def ajax_info():
    """
    获取产品详情
    :return:
    """
    ajax_success_msg = AJAX_SUCCESS_MSG.copy()
    ajax_failure_msg = AJAX_FAILURE_MSG.copy()

    # 检查请求方法
    if not (request.method == 'GET' and request.is_xhr):
        ext_msg = _('Method Not Allowed')
        ajax_failure_msg['msg'] = _('Get Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查请求参数
    production_id = request.args.get('production_id', 0, type=int)
    if not production_id:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Get Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    production_info = get_production_row_by_id(production_id)

    # 检查资源是否存在
    if not production_info:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Get Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查资源是否删除
    if production_info.status_delete == STATUS_DEL_OK:
        ext_msg = _('Already deleted')
        ajax_failure_msg['msg'] = _('Get Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    ajax_success_msg['msg'] = _('Get Success')
    ajax_success_msg['data'] = production_info.to_dict()
    return jsonify(ajax_success_msg)



# @bp_production.route('/ajax/stats', methods=['GET', 'POST'])
# @login_required
# def ajax_stats():
#     """
#     获取产品统计
#     :return:
#     """
#     time_based = request.args.get('time_based', 'hour')
#     result_production_current = production_current_stats(time_based)
#     result_production_former = production_former_stats(time_based)
#
#     line_chart_data = {
#         'labels': [label for label, _ in result_production_current],
#         'datasets': [
#             {
#                 'label': '在职',
#                 'backgroundColor': 'rgba(220,220,220,0.5)',
#                 'borderColor': 'rgba(220,220,220,1)',
#                 'pointBackgroundColor': 'rgba(220,220,220,1)',
#                 'pointBorderColor': '#fff',
#                 'pointBorderWidth': 2,
#                 'data': [data for _, data in result_production_current]
#             },
#             {
#                 'label': '离职',
#                 'backgroundColor': 'rgba(151,187,205,0.5)',
#                 'borderColor': 'rgba(151,187,205,1)',
#                 'pointBackgroundColor': 'rgba(151,187,205,1)',
#                 'pointBorderColor': '#fff',
#                 'pointBorderWidth': 2,
#                 'data': [data for _, data in result_production_former]
#             }
#         ]
#     }
#     return json.dumps(line_chart_data, default=json_default)
#
#
# @bp_production.route('/stats.html')
# @login_required
# @permission_production_section_stats.require(http_exception=403)
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
#     document_info['TITLE'] = _('production stats')
#     # 渲染模板
#     return render_template(
#         'production/stats.html',
#         time_based=time_based,
#         **document_info
#     )
#
#
# @bp_production.route('/<int:production_id>/stats.html')
# @login_required
# @permission_production_section_stats.require(http_exception=403)
# def stats_item(production_id):
#     """
#     产品统计明细
#     :param production_id:
#     :return:
#     """
#     production_info = get_production_row_by_id(production_id)
#     # 检查资源是否存在
#     if not production_info:
#         abort(404)
#     # 检查资源是否删除
#     if production_info.status_delete == STATUS_DEL_OK:
#         abort(410)
#
#     # 统计数据
#     production_stats_item_info = get_production_row_by_id(production_id)
#     # 文档信息
#     document_info = DOCUMENT_INFO.copy()
#     document_info['TITLE'] = _('production stats item')
#     # 渲染模板
#     return render_template(
#         'production/stats_item.html',
#         production_stats_item_info=production_stats_item_info,
#         **document_info
#     )
