#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: tpl_view.py
@time: 2018-07-18 14:09
"""

from __future__ import unicode_literals


CODE_TEMPLATE_VIEW = '''
#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: %(section)s.py
@time: %(time)s
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

from app_backend import (
    app,
    excel,
)
from app_backend.api.%(section)s import (
    get_%(section)s_pagination,
    get_%(section)s_row_by_id,
    add_%(section)s,
    edit_%(section)s,
    get_%(section)s_rows,
)
from app_backend.forms.%(section)s import (
    %(model)sSearchForm,
    %(model)sAddForm,
    %(model)sEditForm,
)
from app_backend.models.bearing_project import %(model)s
from app_backend.permissions import (
    permission_%(section)s_section_add,
    permission_%(section)s_section_search,
    permission_%(section)s_section_export,
    permission_%(section)s_section_stats,
    %(model)sItemGetPermission,
    %(model)sItemEditPermission,
    %(model)sItemDelPermission,
)
from app_common.maps.default import default_choices_int, default_choice_option_int
from app_common.maps.status_delete import (
    STATUS_DEL_OK,
    STATUS_DEL_NO)
from app_common.maps.type_role import (
    TYPE_ROLE_SALES,
)
from app_common.tools import json_default

# 定义蓝图
bp_%(section)s = Blueprint('%(section)s', __name__, url_prefix='/%(section)s')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


@bp_%(section)s.route('/lists.html', methods=['GET', 'POST'])
@bp_%(section)s.route('/lists/<int:page>.html', methods=['GET', 'POST'])
@login_required
@permission_%(section)s_section_search.require(http_exception=403)
def lists(page=1):
    """
    列表
    :param page:
    :return:
    """
    template_name = '%(section)s/lists.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('%(section)s lists')

    # 搜索条件
    form = %(model)sSearchForm(request.form)
    # TODO 补充完整搜索条件下拉字段选项

    search_condition = [
        %(model)s.status_delete == STATUS_DEL_NO,
    ]
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Search Failure'), 'danger')
            # 单独处理csrf_token
            if hasattr(form, 'csrf_token') and getattr(form, 'csrf_token').errors:
                map(lambda x: flash(x, 'danger'), form.csrf_token.errors)
        else:
            # TODO 
            if form.start_create_time.data:
                search_condition.append(%(model)s.create_time >= form.start_create_time.data)
            if form.end_create_time.data:
                search_condition.append(%(model)s.create_time <= form.end_create_time.data)
        # 处理导出
        if form.op.data == 1:
            # 检查导出权限
            if not permission_%(section)s_section_export.can():
                abort(403)
            column_names = %(model)s.__table__.columns.keys()
            query_sets = get_%(section)s_rows(*search_condition)

            return excel.make_response_from_query_sets(
                query_sets=query_sets,
                column_names=column_names,
                file_type='csv',
                file_name='%%s.csv' %% _('%(section)s lists')
            )
    # 翻页数据
    pagination = get_%(section)s_pagination(page, PER_PAGE_BACKEND, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )


@bp_%(section)s.route('/<int:%(section)s_id>/info.html')
@login_required
def info(%(section)s_id):
    """
    详情
    :param %(section)s_id:
    :return:
    """
    # 检查读取权限
    %(section)s_item_get_permission = %(model)sItemGetPermission(%(section)s_id)
    if not %(section)s_item_get_permission.can():
        abort(403)
    # 详情数据
    %(section)s_info = get_%(section)s_row_by_id(%(section)s_id)
    # 检查资源是否存在
    if not %(section)s_info:
        abort(404)
    # 检查资源是否删除
    if %(section)s_info.status_delete == STATUS_DEL_OK:
        abort(410)
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('%(section)s info')
    # 渲染模板
    return render_template('%(section)s/info.html', %(section)s_info=%(section)s_info, **document_info)


@bp_%(section)s.route('/add.html', methods=['GET', 'POST'])
@login_required
@permission_%(section)s_section_add.require(http_exception=403)
def add():
    """
    创建
    :return:
    """
    template_name = '%(section)s/add.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('%(section)s add')

    # 加载创建表单
    form = %(model)sAddForm(request.form)

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
        %(section)s_data = {
            # TODO 完善数据
            'create_time': current_time,
            'update_time': current_time,
        }
        result = add_%(section)s(%(section)s_data)
        # 创建操作成功
        if result:
            flash(_('Add Success'), 'success')
            return redirect(request.args.get('next') or url_for('%(section)s.lists'))
        # 创建操作失败
        else:
            flash(_('Add Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                **document_info
            )


@bp_%(section)s.route('/<int:%(section)s_id>/edit.html', methods=['GET', 'POST'])
@login_required
def edit(%(section)s_id):
    """
    编辑
    """
    # 检查编辑权限
    %(section)s_item_edit_permission = %(model)sItemEditPermission(%(section)s_id)
    if not %(section)s_item_edit_permission.can():
        abort(403)

    %(section)s_info = get_%(section)s_row_by_id(%(section)s_id)
    # 检查资源是否存在
    if not %(section)s_info:
        abort(404)
    # 检查资源是否删除
    if %(section)s_info.status_delete == STATUS_DEL_OK:
        abort(410)

    template_name = '%(section)s/edit.html'

    # 加载编辑表单
    form = %(model)sEditForm(request.form)

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('%(section)s edit')

    # 进入编辑页面
    if request.method == 'GET':
        # 表单赋值
        form.id.data = %(section)s_info.id
        # TODO 完善数据
        form.create_time.data = %(section)s_info.create_time
        form.update_time.data = %(section)s_info.update_time
        # 渲染页面
        return render_template(
            template_name,
            %(section)s_id=%(section)s_id,
            form=form,
            **document_info
        )

    # 处理编辑请求
    if request.method == 'POST':
        # 表单校验失败
        if %(section)s_id != form.id.data or not form.validate_on_submit():
            flash(_('Edit Failure'), 'danger')
            return render_template(
                template_name,
                %(section)s_id=%(section)s_id,
                form=form,
                **document_info
            )
        # 表单校验成功
        current_time = datetime.utcnow()
        %(section)s_data = {
            # TODO 完善数据
            'update_time': current_time,
        }
        result = edit_%(section)s(%(section)s_id, %(section)s_data)
        # 编辑操作成功
        if result:
            flash(_('Edit Success'), 'success')
            return redirect(request.args.get('next') or url_for('%(section)s.lists'))
        # 编辑操作失败
        else:
            flash(_('Edit Failure'), 'danger')
            return render_template(
                template_name,
                %(section)s_id=%(section)s_id,
                form=form,
                **document_info
            )


@bp_%(section)s.route('/ajax/del', methods=['GET', 'POST'])
@login_required
def ajax_delete():
    """
    客户删除
    :return:
    """
    ajax_success_msg = AJAX_SUCCESS_MSG.copy()
    ajax_failure_msg = AJAX_FAILURE_MSG.copy()

    # 检查请求方法
    if not (request.method == 'GET' and request.is_xhr):
        ajax_failure_msg['msg'] = _('Del Failure')  # Method Not Allowed
        return jsonify(ajax_failure_msg)

    # 检查请求参数
    %(section)s_id = request.args.get('%(section)s_id', 0, type=int)
    if not %(section)s_id:
        ajax_failure_msg['msg'] = _('Del Failure')  # ID does not exist
        return jsonify(ajax_failure_msg)

    # 检查删除权限
    %(section)s_item_del_permission = %(model)sItemDelPermission(%(section)s_id)
    if not %(section)s_item_del_permission.can():
        ajax_failure_msg['msg'] = _('Del Failure')  # Permission Denied
        return jsonify(ajax_failure_msg)

    %(section)s_info = get_%(section)s_row_by_id(%(section)s_id)
    # 检查资源是否存在
    if not %(section)s_info:
        ajax_failure_msg['msg'] = _('Del Failure')  # ID does not exist
        return jsonify(ajax_failure_msg)
    # 检查资源是否删除
    if %(section)s_info.status_delete == STATUS_DEL_OK:
        ajax_success_msg['msg'] = _('Del Success')  # Already deleted
        return jsonify(ajax_success_msg)

    current_time = datetime.utcnow()
    %(section)s_data = {
        'status_delete': STATUS_DEL_OK,
        'delete_time': current_time,
        'update_time': current_time,
    }
    result = edit_%(section)s(%(section)s_id, %(section)s_data)
    if result:
        ajax_success_msg['msg'] = _('Del Success')
        return jsonify(ajax_success_msg)
    else:
        ajax_failure_msg['msg'] = _('Del Failure')
        return jsonify(ajax_failure_msg)
'''
