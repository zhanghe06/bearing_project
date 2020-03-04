#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: futures.py
@time: 2018-08-13 22:14
"""

from __future__ import unicode_literals

from copy import copy
from datetime import datetime

from flask import (
    request,
    flash,
    render_template,
    abort,
    jsonify,
    Blueprint,
)
from flask_babel import gettext as _
from flask_login import login_required

from app_backend import app
from app_backend import excel
from app_backend.api.futures import (
    get_futures_pagination,
    get_futures_row_by_id,
    edit_futures,
    # futures_current_stats,
    # futures_former_stats,
    get_futures_rows,
    get_distinct_futures_brand,
)
from app_backend.forms.futures import (
    FuturesSearchForm,
)
from app_backend.models.model_bearing import Futures
from app_backend.permissions.futures import (
    permission_futures_section_search,
    permission_futures_section_export,
    permission_futures_section_get,
    permission_futures_section_del,
)
from app_common.maps.default import DEFAULT_SEARCH_CHOICES_STR, \
    DEFAULT_SEARCH_CHOICES_STR_OPTION
from app_common.maps.status_delete import (
    STATUS_DEL_OK,
    STATUS_DEL_NO)

# 定义蓝图
bp_futures = Blueprint('futures', __name__, url_prefix='/futures')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


def get_futures_brand_choices():
    futures_brand_list = copy(DEFAULT_SEARCH_CHOICES_STR)
    distinct_brand = get_distinct_futures_brand(status_delete=STATUS_DEL_NO)
    futures_brand_list.extend([(brand, brand) for brand in distinct_brand])
    return futures_brand_list


@bp_futures.route('/lists.html', methods=['GET', 'POST'])
@login_required
@permission_futures_section_search.require(http_exception=403)
def lists():
    """
    期货列表
    :return:
    """
    template_name = 'futures/lists.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('futures lists')

    # 搜索条件
    form = FuturesSearchForm(request.form)
    form.production_brand.choices = get_futures_brand_choices()
    # app.logger.info('')

    search_condition = [
        Futures.status_delete == STATUS_DEL_NO,
    ]
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Search Failure'), 'danger')
            # 单独处理csrf_token
            if hasattr(form, 'csrf_token') and getattr(form, 'csrf_token').errors:
                map(lambda x: flash(x, 'danger'), form.csrf_token.errors)
        else:
            if form.production_brand.data != DEFAULT_SEARCH_CHOICES_STR_OPTION:
                search_condition.append(Futures.production_brand == form.production_brand.data)
            if form.production_model.data:
                search_condition.append(Futures.production_model.like('%%%s%%' % form.production_model.data))
            if form.req_date.data:
                search_condition.append(Futures.req_date <= form.req_date.data)
            if form.acc_date.data:
                search_condition.append(Futures.acc_date <= form.acc_date.data)
        # 处理导出
        if form.op.data == 1:
            # 检查导出权限
            if not permission_futures_section_export.can():
                abort(403)
            column_names = Futures.__table__.columns.keys()
            query_sets = get_futures_rows(*search_condition)

            return excel.make_response_from_query_sets(
                query_sets=query_sets,
                column_names=column_names,
                file_type='csv',
                file_name='%s.csv' % _('futures lists')
            )
        # 批量删除
        if form.op.data == 2:
            # 检查删除权限
            if not permission_futures_section_del.can():
                abort(403)

            futures_ids = request.form.getlist('futures_id')
            result_total = True
            for futures_id in futures_ids:
                current_time = datetime.utcnow()
                futures_data = {
                    'status_delete': STATUS_DEL_OK,
                    'delete_time': current_time,
                    'update_time': current_time,
                }
                result = edit_futures(futures_id, futures_data)
                result_total = result_total and result
            if result_total:
                flash(_('Del Success'), 'success')
            else:
                flash(_('Del Failure'), 'danger')
    # 翻页数据
    pagination = get_futures_pagination(form.page.data, PER_PAGE_BACKEND, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )


@bp_futures.route('/<int:futures_id>/info.html')
@login_required
@permission_futures_section_get.require(http_exception=403)
def info(futures_id):
    """
    期货详情
    :param futures_id:
    :return:
    """
    # 详情数据
    futures_info = get_futures_row_by_id(futures_id)
    # 检查资源是否存在
    if not futures_info:
        abort(404)
    # 检查资源是否删除
    if futures_info.status_delete == STATUS_DEL_OK:
        abort(410)
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('futures info')
    # 渲染模板
    return render_template('futures/info.html', futures_info=futures_info, **document_info)


@bp_futures.route('/ajax/del', methods=['GET', 'POST'])
@login_required
def ajax_delete():
    """
    期货删除
    :return:
    """
    ajax_success_msg = AJAX_SUCCESS_MSG.copy()
    ajax_failure_msg = AJAX_FAILURE_MSG.copy()

    # 检查删除权限
    if not permission_futures_section_del.can():
        ext_msg = _('Permission Denied')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查请求方法
    if not (request.method == 'GET' and request.is_xhr):
        ext_msg = _('Method Not Allowed')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查请求参数
    futures_id = request.args.get('futures_id', 0, type=int)
    if not futures_id:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    futures_info = get_futures_row_by_id(futures_id)
    # 检查资源是否存在
    if not futures_info:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)
    # 检查资源是否删除
    if futures_info.status_delete == STATUS_DEL_OK:
        ext_msg = _('Already deleted')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    current_time = datetime.utcnow()
    futures_data = {
        'status_delete': STATUS_DEL_OK,
        'delete_time': current_time,
        'update_time': current_time,
    }
    result = edit_futures(futures_id, futures_data)
    if result:
        ajax_success_msg['msg'] = _('Del Success')
        return jsonify(ajax_success_msg)
    else:
        ajax_failure_msg['msg'] = _('Del Failure')
        return jsonify(ajax_failure_msg)

# @bp_futures.route('/ajax/stats', methods=['GET', 'POST'])
# @login_required
# def ajax_stats():
#     """
#     获取期货统计
#     :return:
#     """
#     time_based = request.args.get('time_based', 'hour')
#     result_futures_current = futures_current_stats(time_based)
#     result_futures_former = futures_former_stats(time_based)
#
#     line_chart_data = {
#         'labels': [label for label, _ in result_futures_current],
#         'datasets': [
#             {
#                 'label': '在职',
#                 'backgroundColor': 'rgba(220,220,220,0.5)',
#                 'borderColor': 'rgba(220,220,220,1)',
#                 'pointBackgroundColor': 'rgba(220,220,220,1)',
#                 'pointBorderColor': '#fff',
#                 'pointBorderWidth': 2,
#                 'data': [data for _, data in result_futures_current]
#             },
#             {
#                 'label': '离职',
#                 'backgroundColor': 'rgba(151,187,205,0.5)',
#                 'borderColor': 'rgba(151,187,205,1)',
#                 'pointBackgroundColor': 'rgba(151,187,205,1)',
#                 'pointBorderColor': '#fff',
#                 'pointBorderWidth': 2,
#                 'data': [data for _, data in result_futures_former]
#             }
#         ]
#     }
#     return json.dumps(line_chart_data, default=json_default)
#
#
# @bp_futures.route('/stats.html')
# @login_required
# @permission_futures_section_stats.require(http_exception=403)
# def stats():
#     """
#     期货统计
#     :return:
#     """
#     # 统计数据
#     time_based = request.args.get('time_based', 'hour')
#     if time_based not in ['hour', 'date', 'month']:
#         abort(404)
#     # 文档信息
#     document_info = DOCUMENT_INFO.copy()
#     document_info['TITLE'] = _('futures stats')
#     # 渲染模板
#     return render_template(
#         'futures/stats.html',
#         time_based=time_based,
#         **document_info
#     )
#
#
# @bp_futures.route('/<int:futures_id>/stats.html')
# @login_required
# @permission_futures_section_stats.require(http_exception=403)
# def stats_item(futures_id):
#     """
#     期货统计明细
#     :param futures_id:
#     :return:
#     """
#     futures_info = get_futures_row_by_id(futures_id)
#     # 检查资源是否存在
#     if not futures_info:
#         abort(404)
#     # 检查资源是否删除
#     if futures_info.status_delete == STATUS_DEL_OK:
#         abort(410)
#
#     # 统计数据
#     futures_stats_item_info = get_futures_row_by_id(futures_id)
#     # 文档信息
#     document_info = DOCUMENT_INFO.copy()
#     document_info['TITLE'] = _('futures stats item')
#     # 渲染模板
#     return render_template(
#         'futures/stats_item.html',
#         futures_stats_item_info=futures_stats_item_info,
#         **document_info
#     )
