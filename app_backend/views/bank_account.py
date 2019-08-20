#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: bank_account.py
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
from app_backend.api.bank import get_bank_choices
from app_backend.api.bank_account import (
    get_bank_account_pagination,
    get_bank_account_row_by_id,
    add_bank_account,
    edit_bank_account,
    # bank_account_current_stats,
    # bank_account_former_stats,
)
from app_backend.api.bank_account import (
    get_bank_account_rows,
    # get_distinct_brand,
)
from app_backend.api.inventory import count_inventory
from app_backend.api.rack import count_rack
from app_backend.forms.bank_account import (
    BankAccountSearchForm,
    BankAccountAddForm,
    BankAccountEditForm,
)
from app_backend.models.bearing_project import BankAccount
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
bp_bank_account = Blueprint('bank_account', __name__, url_prefix='/bank_account')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


@bp_bank_account.route('/lists.html', methods=['GET', 'POST'])
@login_required
@permission_account_section_search.require(http_exception=403)
def lists():
    """
    账目列表
    :return:
    """
    template_name = 'bank_account/lists.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('bank account lists')

    # 搜索条件
    form = BankAccountSearchForm(request.form)
    form.bank_id.choices = get_bank_choices()
    # form.id.choices = get_bank_account_choices()
    # app.logger.info('')

    search_condition = [
        BankAccount.status_delete == STATUS_DEL_NO,
    ]
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Search Failure'), 'danger')
            # 单独处理csrf_token
            if hasattr(form, 'csrf_token') and getattr(form, 'csrf_token').errors:
                map(lambda x: flash(x, 'danger'), form.csrf_token.errors)
        else:
            if form.bank_id.data != DEFAULT_SEARCH_CHOICES_INT_OPTION:
                search_condition.append(BankAccount.bank_id == form.bank_id.data)
            if form.type_current.data:
                search_condition.append(BankAccount.type_current == form.type_current.data)
            if form.type_account.data:
                search_condition.append(BankAccount.type_account == form.type_account.data)
            if form.start_record_date.data:
                search_condition.append(BankAccount.record_date >= form.start_record_date.data)
            if form.end_record_date.data:
                search_condition.append(BankAccount.record_date <= form.end_record_date.data)
        # 处理导出
        if form.op.data == 1:
            # 检查导出权限
            if not permission_account_section_export.can():
                abort(403)
            column_names = BankAccount.__table__.columns.keys()
            query_sets = get_bank_account_rows(*search_condition)

            return excel.make_response_from_query_sets(
                query_sets=query_sets,
                column_names=column_names,
                file_type='csv',
                file_name='%s.csv' % _('bank account lists')
            )
        # 批量删除
        if form.op.data == 2:
            bank_account_ids = request.form.getlist('bank_account_id')
            # 检查删除权限
            if not (permission_role_administrator.can() or permission_role_stock_keeper.can()):
                ext_msg = _('Permission Denied')
                flash(_('Del Failure, %(ext_msg)s', ext_msg=ext_msg), 'danger')
            else:
                permitted = True
                for bank_account_id in bank_account_ids:
                    # 检查是否正在使用
                    # 库存、货架
                    if count_inventory(**{'bank_account_id': bank_account_id, 'status_delete': STATUS_DEL_NO}):
                        ext_msg = _('Currently In Use')
                        flash(_('Del Failure, %(ext_msg)s', ext_msg=ext_msg), 'danger')
                        permitted = False
                        break
                    if count_rack(**{'bank_account_id': bank_account_id, 'status_delete': STATUS_DEL_NO}):
                        ext_msg = _('Currently In Use')
                        flash(_('Del Failure, %(ext_msg)s', ext_msg=ext_msg), 'danger')
                        permitted = False
                        break
                if permitted:
                    result_total = True
                    for bank_account_id in bank_account_ids:
                        current_time = datetime.utcnow()
                        bank_account_data = {
                            'status_delete': STATUS_DEL_OK,
                            'delete_time': current_time,
                            'update_time': current_time,
                        }
                        result = edit_bank_account(bank_account_id, bank_account_data)
                        result_total = result_total and result
                    if result_total:
                        flash(_('Del Success'), 'success')
                    else:
                        flash(_('Del Failure'), 'danger')

    # 翻页数据
    pagination = get_bank_account_pagination(form.page.data, PER_PAGE_BACKEND, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )


@bp_bank_account.route('/<int:bank_account_id>/info.html')
@login_required
@permission_account_section_get.require(http_exception=403)
def info(bank_account_id):
    """
    账目详情
    :param bank_account_id:
    :return:
    """
    # 详情数据
    bank_account_info = get_bank_account_row_by_id(bank_account_id)
    # 检查资源是否存在
    if not bank_account_info:
        abort(404)
    # 检查资源是否删除
    if bank_account_info.status_delete == STATUS_DEL_OK:
        abort(410)
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('bank account info')
    # 渲染模板
    return render_template('bank_account/info.html', bank_account_info=bank_account_info, **document_info)


@bp_bank_account.route('/add.html', methods=['GET', 'POST'])
@login_required
@permission_account_section_add.require(http_exception=403)
def add():
    """
    创建账目
    :return:
    """
    template_name = 'bank_account/add.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('bank account add')

    # 加载创建表单
    form = BankAccountAddForm(request.form)

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
        bank_account_data = {
            'name': form.name.data,
            'address': form.address.data,
            'linkman': form.linkman.data,
            'tel': form.tel.data,
            'fax': form.fax.data,
            'create_time': current_time,
            'update_time': current_time,
        }
        result = add_bank_account(bank_account_data)
        # 创建操作成功
        if result:
            flash(_('Add Success'), 'success')
            return redirect(request.args.get('next') or url_for('bank_account.lists'))
        # 创建操作失败
        else:
            flash(_('Add Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                **document_info
            )


@bp_bank_account.route('/<int:bank_account_id>/edit.html', methods=['GET', 'POST'])
@login_required
@permission_account_section_edit.require(http_exception=403)
def edit(bank_account_id):
    """
    账目编辑
    """
    bank_account_info = get_bank_account_row_by_id(bank_account_id)
    # 检查资源是否存在
    if not bank_account_info:
        abort(404)
    # 检查资源是否删除
    if bank_account_info.status_delete == STATUS_DEL_OK:
        abort(410)

    template_name = 'bank_account/edit.html'

    # 加载编辑表单
    form = BankAccountEditForm(request.form)

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('bank account edit')

    # 进入编辑页面
    if request.method == 'GET':
        # 表单赋值
        form.name.data = bank_account_info.name
        form.address.data = bank_account_info.address
        form.linkman.data = bank_account_info.linkman
        form.tel.data = bank_account_info.tel
        form.fax.data = bank_account_info.fax
        # form.create_time.data = bank_account_info.create_time
        # form.update_time.data = bank_account_info.update_time
        # 渲染页面
        return render_template(
            template_name,
            bank_account_id=bank_account_id,
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
                bank_account_id=bank_account_id,
                form=form,
                **document_info
            )
        # 表单校验成功
        current_time = datetime.utcnow()
        bank_account_data = {
            'name': form.name.data,
            'address': form.address.data,
            'linkman': form.linkman.data,
            'tel': form.tel.data,
            'fax': form.fax.data,
            'update_time': current_time,
        }
        result = edit_bank_account(bank_account_id, bank_account_data)
        # 编辑操作成功
        if result:
            flash(_('Edit Success'), 'success')
            return redirect(request.args.get('next') or url_for('bank_account.lists'))
        # 编辑操作失败
        else:
            flash(_('Edit Failure'), 'danger')
            return render_template(
                template_name,
                bank_account_id=bank_account_id,
                form=form,
                **document_info
            )


@bp_bank_account.route('/ajax/del', methods=['GET', 'POST'])
@login_required
def ajax_delete():
    """
    仓库删除
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
    bank_account_id = request.args.get('bank_account_id', 0, type=int)
    if not bank_account_id:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    bank_account_info = get_bank_account_row_by_id(bank_account_id)
    # 检查资源是否存在
    if not bank_account_info:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)
    # 检查资源是否删除
    if bank_account_info.status_delete == STATUS_DEL_OK:
        ext_msg = _('Already deleted')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)
    # 检查是否正在使用
    # 库存、货架
    if count_inventory(**{'bank_account_id': bank_account_id, 'status_delete': STATUS_DEL_NO}):
        ext_msg = _('Currently In Use')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)
    if count_rack(**{'bank_account_id': bank_account_id, 'status_delete': STATUS_DEL_NO}):
        ext_msg = _('Currently In Use')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    current_time = datetime.utcnow()
    bank_account_data = {
        'status_delete': STATUS_DEL_OK,
        'delete_time': current_time,
        'update_time': current_time,
    }
    result = edit_bank_account(bank_account_id, bank_account_data)
    if result:
        ajax_success_msg['msg'] = _('Del Success')
        return jsonify(ajax_success_msg)
    else:
        ajax_failure_msg['msg'] = _('Del Failure')
        return jsonify(ajax_failure_msg)
