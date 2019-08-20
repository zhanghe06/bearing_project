#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: user.py
@time: 2018-04-04 17:33
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
from flask_babel import gettext as _
from flask_login import login_required

from app_backend import app
from app_backend import excel
from app_backend.api.buyer_order import count_buyer_order
from app_backend.api.delivery import count_delivery
from app_backend.api.enquiry import count_enquiry
from app_backend.api.purchase import count_purchase
from app_backend.api.quotation import count_quotation
from app_backend.api.sales_order import count_sales_order
from app_backend.api.user import (
    get_user_rows,
    get_user_pagination,
    get_user_row_by_id,
    add_user,
    edit_user,
    user_current_stats,
    user_former_stats)
from app_backend.api.user_auth import (
    add_user_auth,
    edit_user_auth, get_user_auth_row)
from app_backend.forms.user import (
    UserSearchForm,
    UserAddForm,
    UserEditForm,
)
from app_backend.models.bearing_project import User
from app_backend.permissions.user import (
    permission_user_section_add,
    permission_user_section_search,
    permission_user_section_stats,
    permission_user_section_export,
    permission_user_section_get,
    permission_user_section_edit,
    permission_user_section_del,
)
from app_common.maps.default import DEFAULT_SEARCH_CHOICES_INT_OPTION
from app_common.maps.operations import OPERATION_EXPORT, OPERATION_DELETE
from app_common.maps.status_delete import (
    STATUS_DEL_OK,
    STATUS_DEL_NO)
from app_common.maps.status_verified import STATUS_VERIFIED_OK
from app_common.maps.type_auth import TYPE_AUTH_ACCOUNT
from app_common.tools import json_default

# 定义蓝图
bp_user = Blueprint('user', __name__, url_prefix='/user')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


@bp_user.route('/lists.html', methods=['GET', 'POST'])
@login_required
@permission_user_section_search.require(http_exception=403)
def lists():
    """
    用户列表
    :return:
    """
    template_name = 'user/lists.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('user lists')

    # 搜索条件
    form = UserSearchForm(request.form)

    search_condition = [
        User.status_delete == STATUS_DEL_NO,
    ]
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Search Failure'), 'danger')
            # 单独处理csrf_token
            if hasattr(form, 'csrf_token') and getattr(form, 'csrf_token').errors:
                map(lambda x: flash(x, 'danger'), form.csrf_token.errors)
        else:
            if form.name.data:
                search_condition.append(User.name == form.name.data)
            if form.role_id.data != DEFAULT_SEARCH_CHOICES_INT_OPTION:
                search_condition.append(User.role_id == form.role_id.data)
            if form.start_create_time.data:
                search_condition.append(User.create_time >= form.start_create_time.data)
            if form.end_create_time.data:
                search_condition.append(User.create_time <= form.end_create_time.data)
        # 处理导出
        if form.op.data == OPERATION_EXPORT:
            # 检查导出权限
            if not permission_user_section_export.can():
                abort(403)
            column_names = User.__table__.columns.keys()
            query_sets = get_user_rows(*search_condition)

            return excel.make_response_from_query_sets(
                query_sets=query_sets,
                column_names=column_names,
                file_type='csv',
                file_name='%s.csv' % _('user lists')
            )
        # 批量删除
        if form.op.data == OPERATION_DELETE:
            # 检查删除权限
            if not permission_user_section_del.can():
                abort(403)
            user_ids = request.form.getlist('user_id')
            # 检查删除权限
            permitted = True
            for user_id in user_ids:
                # 检查是否正在使用
                # 1、报价
                if count_quotation(**{'uid': user_id, 'status_delete': STATUS_DEL_NO}):
                    ext_msg = _('Currently In Use')
                    flash(_('Del Failure, %(ext_msg)s', ext_msg=ext_msg), 'danger')
                    permitted = False
                    break
                # 2、销售订单
                if count_sales_order(**{'uid': user_id, 'status_delete': STATUS_DEL_NO}):
                    ext_msg = _('Currently In Use')
                    flash(_('Del Failure, %(ext_msg)s', ext_msg=ext_msg), 'danger')
                    permitted = False
                    break
                # 3、销售出货
                if count_delivery(**{'uid': user_id, 'status_delete': STATUS_DEL_NO}):
                    ext_msg = _('Currently In Use')
                    flash(_('Del Failure, %(ext_msg)s', ext_msg=ext_msg), 'danger')
                    permitted = False
                    break
                # 4、询价
                if count_enquiry(**{'uid': user_id, 'status_delete': STATUS_DEL_NO}):
                    ext_msg = _('Currently In Use')
                    flash(_('Del Failure, %(ext_msg)s', ext_msg=ext_msg), 'danger')
                    permitted = False
                    break
                # 5、采购订单
                if count_buyer_order(**{'uid': user_id, 'status_delete': STATUS_DEL_NO}):
                    ext_msg = _('Currently In Use')
                    flash(_('Del Failure, %(ext_msg)s', ext_msg=ext_msg), 'danger')
                    permitted = False
                    break
                # 6、采购进货
                if count_purchase(**{'uid': user_id, 'status_delete': STATUS_DEL_NO}):
                    ext_msg = _('Currently In Use')
                    flash(_('Del Failure, %(ext_msg)s', ext_msg=ext_msg), 'danger')
                    permitted = False
                    break
            if permitted:
                result_total = True
                for user_id in user_ids:
                    current_time = datetime.utcnow()
                    user_data = {
                        'status_delete': STATUS_DEL_OK,
                        'delete_time': current_time,
                        'update_time': current_time,
                    }
                    result = edit_user(user_id, user_data)
                    result_total = result_total and result
                if result_total:
                    flash(_('Del Success'), 'success')
                else:
                    flash(_('Del Failure'), 'danger')
    # 翻页数据
    pagination = get_user_pagination(form.page.data, PER_PAGE_BACKEND, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )


# @bp_user.route('/search.html', methods=['GET', 'POST'])
# @login_required
# @permission_user_section_search.require(http_exception=403)
# def search():
#     """
#     用户搜索
#     :return:
#     """
#     template_name = 'customer/search_modal.html'
#     # 文档信息
#     document_info = DOCUMENT_INFO.copy()
#     document_info['TITLE'] = _('Customer Search')
#
#     # 搜索条件
#     form = UserSearchForm(request.form)
#     form.owner_uid.choices = get_sales_user_list()
#     # app.logger.info('')
#
#     search_condition = [
#         Customer.status_delete == STATUS_DEL_NO,
#     ]
#     if request.method == 'POST':
#         # 表单校验失败
#         if not form.validate_on_submit():
#             flash(_('Search Failure'), 'danger')
#             # 单独处理csrf_token
#             if hasattr(form, 'csrf_token') and getattr(form, 'csrf_token').errors:
#                 map(lambda x: flash(x, 'danger'), form.csrf_token.errors)
#         else:
#             if form.company_type.data != default_choice_option_int:
#                 search_condition.append(Customer.company_type == form.company_type.data)
#             if form.company_name.data:
#                 search_condition.append(Customer.company_name.like('%%%s%%' % form.company_name.data))
#     # 翻页数据
#     pagination = get_customer_pagination(form.page.data, PER_PAGE_BACKEND_MODAL, *search_condition)
#
#     # 渲染模板
#     return render_template(
#         template_name,
#         form=form,
#         pagination=pagination,
#         **document_info
#     )


@bp_user.route('/<int:user_id>/info.html')
@login_required
@permission_user_section_get.require(http_exception=403)
def info(user_id):
    """
    用户详情
    :param user_id:
    :return:
    """
    # 详情数据
    user_info = get_user_row_by_id(user_id)
    # 检查资源是否存在
    if not user_info:
        abort(404)
    # 检查资源是否删除
    if user_info.status_delete == STATUS_DEL_OK:
        abort(410)
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('user info')
    # 渲染模板
    return render_template('user/info.html', user_info=user_info, **document_info)


@bp_user.route('/add.html', methods=['GET', 'POST'])
@login_required
@permission_user_section_add.require(http_exception=403)
def add():
    """
    创建用户
    :return:
    """
    template_name = 'user/add.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('user add')

    # 加载创建表单
    form = UserAddForm(request.form)

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

        # 创建用户基本信息
        current_time = datetime.utcnow()
        user_data = {
            'name': form.name.data,
            'salutation': form.salutation.data,
            'mobile': form.mobile.data,
            'tel': form.tel.data,
            'fax': form.fax.data,
            'email': form.email.data,
            'role_id': form.role_id.data,
            'create_time': current_time,
            'update_time': current_time,
        }
        user_id = add_user(user_data)
        if not user_id:
            flash(_('Add Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                **document_info
            )
        # 创建用户认证信息
        user_auth_data = {
            'user_id': user_id,
            'type_auth': TYPE_AUTH_ACCOUNT,
            'auth_key': form.name.data,
            'auth_secret': '123456',  # 默认密码
            'status_verified': STATUS_VERIFIED_OK,
            'create_time': current_time,
            'update_time': current_time,
        }
        result = add_user_auth(user_auth_data)
        if result:
            flash(_('Add Success'), 'success')
            return redirect(request.args.get('next') or url_for('user.lists'))
        # 创建操作失败
        else:
            flash(_('Add Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                **document_info
            )


@bp_user.route('/<int:user_id>/edit.html', methods=['GET', 'POST'])
@login_required
@permission_user_section_edit.require(http_exception=403)
def edit(user_id):
    """
    用户编辑
    """
    user_info = get_user_row_by_id(user_id)
    # 检查资源是否存在
    if not user_info:
        abort(404)
    # 检查资源是否删除
    if user_info.status_delete == STATUS_DEL_OK:
        abort(410)

    template_name = 'user/edit.html'

    # 加载编辑表单
    form = UserEditForm(request.form)
    form.id.data = user_id  # id 仅作为编辑重复校验

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('user edit')

    # 进入编辑页面
    if request.method == 'GET':
        # 表单赋值
        form.id.data = user_info.id
        form.name.data = user_info.name
        form.salutation.data = user_info.salutation
        form.mobile.data = user_info.mobile
        form.tel.data = user_info.tel
        form.fax.data = user_info.fax
        form.email.data = user_info.email
        form.role_id.data = user_info.role_id
        form.create_time.data = user_info.create_time
        form.update_time.data = user_info.update_time
        # 渲染页面
        return render_template(
            template_name,
            user_id=user_id,
            form=form,
            **document_info
        )

    # 处理编辑请求
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Edit Failure'), 'danger')
            # flash(form.errors, 'danger')
            return render_template(
                template_name,
                user_id=user_id,
                form=form,
                **document_info
            )
        # 表单校验成功

        # 编辑用户基本信息
        current_time = datetime.utcnow()
        user_data = {
            'name': form.name.data,
            'salutation': form.salutation.data,
            'mobile': form.mobile.data,
            'tel': form.tel.data,
            'fax': form.fax.data,
            'email': form.email.data,
            'role_id': form.role_id.data,
            'update_time': current_time,
        }
        result = edit_user(user_id, user_data)
        if not result:
            # 编辑操作失败
            flash(_('Edit Failure'), 'danger')
            return render_template(
                template_name,
                user_id=user_id,
                form=form,
                **document_info
            )

        user_auth_row = get_user_auth_row(user_id=user_id)
        if not user_auth_row:
            # 编辑操作失败
            flash(_('Edit Failure'), 'danger')
            return render_template(
                template_name,
                user_id=user_id,
                form=form,
                **document_info
            )
        # 编辑用户认证信息
        user_auth_data = {
            'user_id': user_id,
            'type_auth': TYPE_AUTH_ACCOUNT,
            'auth_key': form.name.data,
            'update_time': current_time,
        }
        result = edit_user_auth(user_auth_row.id, user_auth_data)

        if not result:
            # 编辑操作失败
            flash(_('Edit Failure'), 'danger')
            return render_template(
                template_name,
                user_id=user_id,
                form=form,
                **document_info
            )
        # 编辑操作成功
        flash(_('Edit Success'), 'success')
        return redirect(request.args.get('next') or url_for('user.lists'))


@bp_user.route('/ajax/del', methods=['GET', 'POST'])
@login_required
def ajax_delete():
    """
    用户删除
    :return:
    """
    ajax_success_msg = AJAX_SUCCESS_MSG.copy()
    ajax_failure_msg = AJAX_FAILURE_MSG.copy()

    # 检查删除权限
    if not permission_user_section_del.can():
        ext_msg = _('Permission Denied')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查请求方法
    if not (request.method == 'GET' and request.is_xhr):
        ext_msg = _('Method Not Allowed')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    # 检查请求参数
    user_id = request.args.get('user_id', 0, type=int)
    if not user_id:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    user_info = get_user_row_by_id(user_id)
    # 检查资源是否存在
    if not user_info:
        ext_msg = _('ID does not exist')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)
    # 检查资源是否删除
    if user_info.status_delete == STATUS_DEL_OK:
        ext_msg = _('Already deleted')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)
    # 检查是否正在使用
    # 报价、订单
    if count_quotation(**{'uid': user_id, 'status_delete': STATUS_DEL_NO}):
        ext_msg = _('Currently In Use')
        ajax_failure_msg['msg'] = _('Del Failure, %(ext_msg)s', ext_msg=ext_msg)
        return jsonify(ajax_failure_msg)

    current_time = datetime.utcnow()
    user_data = {
        'status_delete': STATUS_DEL_OK,
        'delete_time': current_time,
        'update_time': current_time,
    }
    result = edit_user(user_id, user_data)
    if result:
        ajax_success_msg['msg'] = _('Del Success')
        return jsonify(ajax_success_msg)
    else:
        ajax_failure_msg['msg'] = _('Del Failure')
        return jsonify(ajax_failure_msg)


@bp_user.route('/ajax/stats', methods=['GET', 'POST'])
@login_required
def ajax_stats():
    """
    获取用户统计
    :return:
    """
    time_based = request.args.get('time_based', 'hour')
    result_user_current = user_current_stats(time_based)
    result_user_former = user_former_stats(time_based)

    line_chart_data = {
        'labels': [label for label, _ in result_user_current],
        'datasets': [
            {
                'label': '在职',
                'backgroundColor': 'rgba(220,220,220,0.5)',
                'borderColor': 'rgba(220,220,220,1)',
                'pointBackgroundColor': 'rgba(220,220,220,1)',
                'pointBorderColor': '#fff',
                'pointBorderWidth': 2,
                'data': [data for _, data in result_user_current]
            },
            {
                'label': '离职',
                'backgroundColor': 'rgba(151,187,205,0.5)',
                'borderColor': 'rgba(151,187,205,1)',
                'pointBackgroundColor': 'rgba(151,187,205,1)',
                'pointBorderColor': '#fff',
                'pointBorderWidth': 2,
                'data': [data for _, data in result_user_former]
            }
        ]
    }
    return json.dumps(line_chart_data, default=json_default)


@bp_user.route('/stats.html')
@login_required
@permission_user_section_stats.require(http_exception=403)
def stats():
    """
    用户统计
    :return:
    """
    # 统计数据
    time_based = request.args.get('time_based', 'hour')
    if time_based not in ['hour', 'date', 'month']:
        abort(404)
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('user stats')
    # 渲染模板
    return render_template(
        'user/stats.html',
        time_based=time_based,
        **document_info
    )


@bp_user.route('/<int:user_id>/stats.html')
@login_required
@permission_user_section_stats.require(http_exception=403)
def stats_item(user_id):
    """
    用户统计明细
    :param user_id:
    :return:
    """
    user_info = get_user_row_by_id(user_id)
    # 检查资源是否存在
    if not user_info:
        abort(404)
    # 检查资源是否删除
    if user_info.status_delete == STATUS_DEL_OK:
        abort(410)

    # 统计数据
    user_stats_item_info = get_user_row_by_id(user_id)
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('user stats item')
    # 渲染模板
    return render_template(
        'user/stats_item.html',
        user_stats_item_info=user_stats_item_info,
        **document_info
    )
