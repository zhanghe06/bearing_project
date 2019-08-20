#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: cash.py
@time: 2019-08-17 17:19
"""

from __future__ import unicode_literals

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
from app_backend.api.cash import (
    get_cash_pagination,
    get_cash_row_by_id,
    add_cash,
    edit_cash,
    get_cash_choices,
    # cash_current_stats,
    # cash_former_stats,
)
from app_backend.api.cash import (
    get_cash_rows,
    # get_distinct_brand,
)
from app_backend.api.inventory import count_inventory
from app_backend.api.rack import count_rack
from app_backend.forms.cash import (
    CashSearchForm,
    CashAddForm,
    CashEditForm,
)
from app_backend.models.bearing_project import Cash
from app_backend.permissions import permission_role_administrator, permission_role_stock_keeper
from app_backend.permissions.account import (
    permission_account_section_add,
    permission_account_section_search,
    permission_account_section_export,
    permission_account_section_get,
    permission_account_section_edit,
    permission_account_section_del,
)
from app_common.maps.default import DEFAULT_SEARCH_CHOICES_INT_OPTION
from app_common.maps.status_delete import (
    STATUS_DEL_OK,
    STATUS_DEL_NO)

# 定义蓝图
bp_cash = Blueprint('cash', __name__, url_prefix='/cash')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


@bp_cash.route('/lists.html', methods=['GET', 'POST'])
@login_required
@permission_account_section_search.require(http_exception=403)
def lists():
    """
    现金列表
    :return:
    """
    template_name = 'cash/lists.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('cash lists')

    # 搜索条件
    form = CashSearchForm(request.form)
    form.id.choices = get_cash_choices()
    # app.logger.info('')

    search_condition = [
        Cash.status_delete == STATUS_DEL_NO,
    ]
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Search Failure'), 'danger')
            # 单独处理csrf_token
            if hasattr(form, 'csrf_token') and getattr(form, 'csrf_token').errors:
                map(lambda x: flash(x, 'danger'), form.csrf_token.errors)
        else:
            if form.id.data != DEFAULT_SEARCH_CHOICES_INT_OPTION:
                search_condition.append(Cash.id == form.id.data)
        # 处理导出
        if form.op.data == 1:
            # 检查导出权限
            if not permission_account_section_export.can():
                abort(403)
            column_names = Cash.__table__.columns.keys()
            query_sets = get_cash_rows(*search_condition)

            return excel.make_response_from_query_sets(
                query_sets=query_sets,
                column_names=column_names,
                file_type='csv',
                file_name='%s.csv' % _('cash lists')
            )
        # 批量删除
        if form.op.data == 2:
            cash_ids = request.form.getlist('cash_id')
            # 检查删除权限
            if not (permission_role_administrator.can() or permission_role_stock_keeper.can()):
                ext_msg = _('Permission Denied')
                flash(_('Del Failure, %(ext_msg)s', ext_msg=ext_msg), 'danger')
            else:
                permitted = True
                for cash_id in cash_ids:
                    # 检查是否正在使用
                    # 库存、货架
                    if count_inventory(**{'cash_id': cash_id, 'status_delete': STATUS_DEL_NO}):
                        ext_msg = _('Currently In Use')
                        flash(_('Del Failure, %(ext_msg)s', ext_msg=ext_msg), 'danger')
                        permitted = False
                        break
                    if count_rack(**{'cash_id': cash_id, 'status_delete': STATUS_DEL_NO}):
                        ext_msg = _('Currently In Use')
                        flash(_('Del Failure, %(ext_msg)s', ext_msg=ext_msg), 'danger')
                        permitted = False
                        break
                if permitted:
                    result_total = True
                    for cash_id in cash_ids:
                        current_time = datetime.utcnow()
                        cash_data = {
                            'status_delete': STATUS_DEL_OK,
                            'delete_time': current_time,
                            'update_time': current_time,
                        }
                        result = edit_cash(cash_id, cash_data)
                        result_total = result_total and result
                    if result_total:
                        flash(_('Del Success'), 'success')
                    else:
                        flash(_('Del Failure'), 'danger')

    # 翻页数据
    pagination = get_cash_pagination(form.page.data, PER_PAGE_BACKEND, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )


@bp_cash.route('/<int:cash_id>/info.html')
@login_required
@permission_account_section_get.require(http_exception=403)
def info(cash_id):
    """
    现金详情
    :param cash_id:
    :return:
    """
    # 详情数据
    cash_info = get_cash_row_by_id(cash_id)
    # 检查资源是否存在
    if not cash_info:
        abort(404)
    # 检查资源是否删除
    if cash_info.status_delete == STATUS_DEL_OK:
        abort(410)
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('cash info')
    # 渲染模板
    return render_template('cash/info.html', cash_info=cash_info, **document_info)


@bp_cash.route('/add.html', methods=['GET', 'POST'])
@login_required
@permission_account_section_add.require(http_exception=403)
def add():
    """
    创建现金
    :return:
    """
    template_name = 'cash/add.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('cash add')

    # 加载创建表单
    form = CashAddForm(request.form)

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
        cash_data = {
            'cash_name': form.cash_name.data,
            'initial_balance': form.initial_balance.data,
            'closing_balance': form.closing_balance.data,
            'note': form.note.data,
            'create_time': current_time,
            'update_time': current_time,
        }
        result = add_cash(cash_data)
        # 创建操作成功
        if result:
            flash(_('Add Success'), 'success')
            return redirect(request.args.get('next') or url_for('cash.lists'))
        # 创建操作失败
        else:
            flash(_('Add Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                **document_info
            )


@bp_cash.route('/<int:cash_id>/edit.html', methods=['GET', 'POST'])
@login_required
@permission_account_section_edit.require(http_exception=403)
def edit(cash_id):
    """
    现金编辑
    """
    cash_info = get_cash_row_by_id(cash_id)
    # 检查资源是否存在
    if not cash_info:
        abort(404)
    # 检查资源是否删除
    if cash_info.status_delete == STATUS_DEL_OK:
        abort(410)

    template_name = 'cash/edit.html'

    # 加载编辑表单
    form = CashEditForm(request.form)

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('cash edit')

    # 进入编辑页面
    if request.method == 'GET':
        # 表单赋值
        form.cash_name.data = cash_info.cash_name
        form.initial_balance.data = cash_info.initial_balance
        form.closing_balance.data = cash_info.closing_balance
        form.note.data = cash_info.note
        # form.create_time.data = cash_info.create_time
        # form.update_time.data = cash_info.update_time
        # 渲染页面
        return render_template(
            template_name,
            cash_id=cash_id,
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
                cash_id=cash_id,
                form=form,
                **document_info
            )
        # 表单校验成功
        current_time = datetime.utcnow()
        cash_data = {
            'cash_name': form.cash_name.data,
            'initial_balance': form.initial_balance.data,
            'closing_balance': form.closing_balance.data,
            'note': form.note.data,
            'update_time': current_time,
        }
        result = edit_cash(cash_id, cash_data)
        # 编辑操作成功
        if result:
            flash(_('Edit Success'), 'success')
            return redirect(request.args.get('next') or url_for('cash.lists'))
        # 编辑操作失败
        else:
            flash(_('Edit Failure'), 'danger')
            return render_template(
                template_name,
                cash_id=cash_id,
                form=form,
                **document_info
            )


@bp_cash.route('/ajax/del', methods=['GET', 'POST'])
@login_required
def ajax_delete():
    """
    现金删除
    :return:
    """
    ajax_success_msg = AJAX_SUCCESS_MSG.copy()
    ajax_failure_msg = AJAX_FAILURE_MSG.copy()

    # 检查删除权限
    if not permission_account_section_del.can():
        ext_msg = _('Permission Denied')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查请求方法
    if not (request.method == 'GET' and request.is_xhr):
        ext_msg = _('Method Not Allowed')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查请求参数
    cash_id = request.args.get('cash_id', 0, type=int)
    if not cash_id:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    cash_info = get_cash_row_by_id(cash_id)
    # 检查资源是否存在
    if not cash_info:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)
    # 检查资源是否删除
    if cash_info.status_delete == STATUS_DEL_OK:
        ext_msg = _('Already deleted')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)
    # 检查是否正在使用
    # 现金流水 TODO
    # if count_inventory(**{'cash_id': cash_id, 'status_delete': STATUS_DEL_NO}):
    #     ext_msg = _('Currently In Use')
    #     ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
    #     return jsonify(ajax_failure_msg)

    current_time = datetime.utcnow()
    cash_data = {
        'status_delete': STATUS_DEL_OK,
        'delete_time': current_time,
        'update_time': current_time,
    }
    result = edit_cash(cash_id, cash_data)
    if result:
        ajax_success_msg['msg'] = _('Del Success')
        return jsonify(ajax_success_msg)
    else:
        ajax_failure_msg['msg'] = _('Del Failure')
        return jsonify(ajax_failure_msg)
