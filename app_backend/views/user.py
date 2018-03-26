#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: user.py
@time: 2018-03-16 09:58
"""

from __future__ import unicode_literals

from copy import copy
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
)
from flask_login import login_required
from app_backend import excel
from app_backend import app
from app_backend.api.user import (
    get_user_pagination,
    get_user_row_by_id,
    add_user,
    edit_user,
    get_user_rows)
from app_backend.forms.user import (
    UserSearchForm,
    UserAddForm,
    UserEditForm,
)
from app_backend.models.bearing_project import User
from app_backend.permissions import (
    permission_section_user,
    permission_role_administrator,
)
from app_common.maps.status_delete import (
    STATUS_DEL_OK,
)

from app_common.maps.default import default_choices, default_choice_option

from flask_babel import gettext as _, ngettext


from app_common.maps.type_role import TYPE_ROLE_MANAGER

# 定义蓝图
bp_user = Blueprint('user', __name__, url_prefix='/user')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


def get_manager_user_list():
    manager_user_list = copy(default_choices)
    user_list = get_user_rows(**{'role_id': TYPE_ROLE_MANAGER})
    manager_user_list.extend([(user.id, user.name) for user in user_list])
    return manager_user_list


@bp_user.route('/lists.html', methods=['GET', 'POST'])
@bp_user.route('/lists/<int:page>.html', methods=['GET', 'POST'])
@login_required
@permission_section_user.require(http_exception=403)
def lists(page=1):
    """
    用户列表
    :param page:
    :return:
    """
    template_name = 'user/lists.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('user lists')

    # 搜索条件
    form = UserSearchForm(request.form)
    form.parent_id.choices = get_manager_user_list()

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
            if form.name.data:
                search_condition.append(User.name == form.name.data)
            if form.role_id.data != default_choice_option:
                search_condition.append(User.role_id == form.role_id.data)
            if form.parent_id.data != default_choice_option:
                search_condition.append(User.parent_id == form.parent_id.data)
            if form.start_create_time.data:
                search_condition.append(User.create_time >= form.start_create_time.data)
            if form.end_create_time.data:
                search_condition.append(User.create_time <= form.end_create_time.data)
        # 处理导出
        if form.op.data == 1:
            column_names = User.__table__.columns.keys()
            query_sets = get_user_rows(*search_condition)

            return excel.make_response_from_query_sets(
                query_sets=query_sets,
                column_names=column_names,
                file_type='csv',
                file_name='%s.csv' % _('user lists')
            )

    # 翻页数据
    pagination = get_user_pagination(page, PER_PAGE_BACKEND, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )


@bp_user.route('/<int:user_id>/info.html')
@login_required
@permission_section_user.require(http_exception=403)
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
@permission_section_user.require(http_exception=403)
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
        current_time = datetime.utcnow()
        user_data = {
            'company_name': form.company_name.data,
            'company_address': form.company_address.data,
            'company_site': form.company_site.data,
            'company_tel': form.company_tel.data,
            'company_fax': form.company_fax.data,
            'company_type': form.company_type.data,
            'owner_uid': form.owner_uid.data,
            'status_delete': form.status_delete.data,
            'delete_time': form.delete_time.data,
            'create_time': current_time,
            'update_time': current_time,
        }
        result = add_user(user_data)
        # 创建操作成功
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
@permission_role_administrator.require(http_exception=403)
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

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('user edit')

    # 进入编辑页面
    if request.method == 'GET':
        # 表单赋值
        form.company_name.data = user_info.company_name
        form.company_address.data = user_info.company_address
        form.company_site.data = user_info.company_site
        form.company_tel.data = user_info.company_tel
        form.company_fax.data = user_info.company_fax
        form.company_type.data = user_info.company_type
        form.owner_uid.data = user_info.owner_uid
        form.status_delete.data = user_info.status_delete
        form.delete_time.data = user_info.delete_time
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
            return render_template(
                template_name,
                user_id=user_id,
                form=form,
                **document_info
            )
        # 表单校验成功
        current_time = datetime.utcnow()
        user_data = {
            'company_name': form.company_name.data,
            'company_address': form.company_address.data,
            'company_site': form.company_site.data,
            'company_tel': form.company_tel.data,
            'company_fax': form.company_fax.data,
            'company_type': form.company_type.data,
            'owner_uid': form.owner_uid.data,
            'status_delete': form.status_delete.data,
            'delete_time': form.delete_time.data,
            'create_time': current_time,
            'update_time': current_time,
        }
        result = edit_user(user_id, user_data)
        # 编辑操作成功
        if result:
            flash(_('Edit Success'), 'success')
            return redirect(request.args.get('next') or url_for('user.lists'))
        # 编辑操作失败
        else:
            flash(_('Edit Failure'), 'danger')
            return render_template(
                template_name,
                user_id=user_id,
                form=form,
                **document_info
            )


@bp_user.route('/<int:user_id>/del.html')
@login_required
@permission_role_administrator.require(http_exception=403)
def delete(user_id):
    """
    用户删除
    """

    current_time = datetime.utcnow()
    user_data = {
        'status_delete': STATUS_DEL_OK,
        'delete_time': current_time,
        'update_time': current_time,
    }
    result = edit_user(user_id, user_data)
    if result:
        flash('Del Success', 'success')
    else:
        flash('Del Failure', 'danger')
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

    # 检查模块权限
    if not permission_section_user.can():
        ajax_failure_msg['msg'] = _('Del Failure')  # Permission Denied
        return jsonify(ajax_failure_msg)

    if request.method == 'GET' and request.is_xhr:
        user_id = request.args.get('user_id', 0, type=int)
        if not user_id:
            ajax_failure_msg['msg'] = _('Del Failure')  # ID does not exist
            return jsonify(ajax_failure_msg)

        # 检查编辑权限
        if not permission_role_administrator.can():
            ajax_failure_msg['msg'] = _('Del Failure')  # Permission Denied
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
    ajax_failure_msg['msg'] = _('Del Failure')  # Method Not Allowed
    return jsonify(ajax_failure_msg)


@bp_user.route('/stats.html')
@bp_user.route('/stats/<int:page>.html')
@login_required
@permission_section_user.require(http_exception=403)
def stats(page=1):
    """
    用户统计
    :param page:
    :return:
    """
    # 统计数据
    user_stats_info = get_user_pagination(page, PER_PAGE_BACKEND)
    # 翻页数据
    pagination = get_user_pagination(page, PER_PAGE_BACKEND)
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('user stats')
    # 渲染模板
    return render_template(
        'user/stats.html',
        user_stats_info=user_stats_info,
        pagination=pagination,
        **document_info
    )


@bp_user.route('/<int:user_id>/stats.html')
@login_required
@permission_section_user.require(http_exception=403)
def stats_item(user_id):
    """
    用户统计明细
    :param user_id:
    :return:
    """
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
