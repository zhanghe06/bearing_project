#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: purchase.py
@time: 2018-07-16 17:25
"""

from __future__ import unicode_literals

import json
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
from flask_babel import lazy_gettext as _
from flask_login import login_required, current_user

from app_backend.api.purchase import (
    get_purchase_row_by_id,
    edit_purchase,
)
from app_backend.permissions import permission_role_purchaser
from app_common.maps.status_confirm import (
    STATUS_CONFIRM_OK,
    STATUS_CONFIRM_NO,
)
from app_common.maps.status_audit import (
    STATUS_AUDIT_OK,
    STATUS_AUDIT_NO,
)
from app_backend import (
    app,
    excel,
)

# 定义蓝图
from app_common.maps.status_delete import STATUS_DEL_OK

bp_purchase = Blueprint('purchase', __name__, url_prefix='/purchase')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


@bp_purchase.route('/lists.html', methods=['GET', 'POST'])
@bp_purchase.route('/lists/<int:page>.html', methods=['GET', 'POST'])
@login_required
def lists(page=1):
    return jsonify({})


@bp_purchase.route('/add.html', methods=['GET', 'POST'])
@login_required
def add():
    return jsonify({})


@bp_purchase.route('/ajax/del', methods=['GET', 'POST'])
@login_required
def ajax_delete():
    """
    采购入库删除
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
    purchase_id = request.args.get('purchase_id', 0, type=int)
    if not purchase_id:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查删除权限
    purchase_item_del_permission = permission_role_purchaser
    if not purchase_item_del_permission.can():
        ext_msg = _('Permission Denied')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    purchase_info = get_purchase_row_by_id(purchase_id)

    # 检查资源是否存在
    if not purchase_info:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查资源是否删除
    if purchase_info.status_delete == STATUS_DEL_OK:
        ext_msg = _('Already deleted')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查确认状态
    if purchase_info.status_confirm == STATUS_CONFIRM_OK:
        ext_msg = _('Already confirm success')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查审核状态
    if purchase_info.status_audit == STATUS_AUDIT_OK:
        ext_msg = _('Already audit success')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 修改状态
    current_time = datetime.utcnow()
    purchase_data = {
        'status_delete': STATUS_DEL_OK,
        'delete_time': current_time,
        'update_time': current_time,
    }
    result = edit_purchase(purchase_id, purchase_data)
    if result:
        ajax_success_msg['msg'] = _('Del Success')
        return jsonify(ajax_success_msg)
    else:
        ajax_failure_msg['msg'] = _('Del Failure')
        return jsonify(ajax_failure_msg)


@bp_purchase.route('/ajax/confirm/success', methods=['GET', 'POST'])
@login_required
def ajax_confirm_success():
    """
    采购入库确认成功
    1、新增库存
    2、重算成本
    3、修改状态
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
    purchase_id = request.args.get('purchase_id', 0, type=int)
    if not purchase_id:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查删除权限
    purchase_item_del_permission = permission_role_purchaser
    if not purchase_item_del_permission.can():
        ext_msg = _('Permission Denied')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    purchase_info = get_purchase_row_by_id(purchase_id)

    # 检查资源是否存在
    if not purchase_info:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查资源是否删除
    if purchase_info.status_delete == STATUS_DEL_OK:
        ext_msg = _('Already deleted')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查确认状态
    if purchase_info.status_confirm == STATUS_CONFIRM_OK:
        ext_msg = _('Already confirm success')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查审核状态
    if purchase_info.status_audit == STATUS_AUDIT_OK:
        ext_msg = _('Already audit success')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 修改状态
    current_time = datetime.utcnow()
    purchase_data = {
        'status_delete': STATUS_DEL_OK,
        'delete_time': current_time,
        'update_time': current_time,
    }
    result = edit_purchase(purchase_id, purchase_data)
    if result:
        ajax_success_msg['msg'] = _('Del Success')
        return jsonify(ajax_success_msg)
    else:
        ajax_failure_msg['msg'] = _('Del Failure')
        return jsonify(ajax_failure_msg)


@bp_purchase.route('/ajax/confirm/failure', methods=['GET', 'POST'])
@login_required
def ajax_confirm_failure():
    """
    采购入库确认失败
    1、修改状态
    :return:
    """
    ajax_success_msg = AJAX_SUCCESS_MSG.copy()
    ajax_failure_msg = AJAX_FAILURE_MSG.copy()
    pass


@bp_purchase.route('/ajax/confirm/cancel', methods=['GET', 'POST'])
@login_required
def ajax_confirm_cancel():
    """
    取消采购入库确认状态
    1、扣减库存
        1.1、库存不够, 返回失败
        1.2、完成扣减, 继续执行
    2、重算成本
    3、修改状态
    :return:
    """
    ajax_success_msg = AJAX_SUCCESS_MSG.copy()
    ajax_failure_msg = AJAX_FAILURE_MSG.copy()
    pass


@bp_purchase.route('/ajax/audit/success', methods=['GET', 'POST'])
@login_required
def ajax_audit_success():
    """
    采购入库审核通过
    1、检查确认状态（是否确认）
        1.1、已确认/已取消, 返回失败
        1.2、未确认, 修改状态
    :return:
    """
    ajax_success_msg = AJAX_SUCCESS_MSG.copy()
    ajax_failure_msg = AJAX_FAILURE_MSG.copy()
    pass


@bp_purchase.route('/ajax/audit/failure', methods=['GET', 'POST'])
@login_required
def ajax_audit_failure():
    """
    采购入库审核失败
    1、检查确认状态（是否确认）
        1.1、已确认/已取消, 返回失败
        1.2、未确认, 修改状态
    :return:
    """
    ajax_success_msg = AJAX_SUCCESS_MSG.copy()
    ajax_failure_msg = AJAX_FAILURE_MSG.copy()
    pass


@bp_purchase.route('/ajax/audit/cancel', methods=['GET', 'POST'])
@login_required
def ajax_audit_cancel():
    """
    取消采购入库审核状态
    1、检查确认状态（是否确认）
        1.1、已确认/已取消 返回失败
        1.2、未确认, 修改状态
    :return:
    """
    ajax_success_msg = AJAX_SUCCESS_MSG.copy()
    ajax_failure_msg = AJAX_FAILURE_MSG.copy()
    pass
