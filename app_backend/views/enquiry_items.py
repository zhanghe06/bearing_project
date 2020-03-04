#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: enquiry_item.py
@time: 2018-09-13 10:08
"""

from __future__ import unicode_literals

from flask import (
    request,
    flash,
    render_template,
    abort,
    Blueprint,
)
from flask_babel import gettext as _
from flask_login import login_required
from sqlalchemy import or_

from app_backend import (
    app,
    excel,
)
from app_backend.api.enquiry_items import get_enquiry_items_rows, get_enquiry_items_pagination
from app_backend.forms.enquiry_items import EnquiryItemsSearchForm
from app_backend.models.model_bearing import EnquiryItems
from app_backend.permissions.enquiry import (
    permission_enquiry_section_search,
    permission_enquiry_section_export,
)
from app_common.maps.operations import OPERATION_EXPORT
from app_common.maps.status_delete import (
    STATUS_DEL_NO)

# 定义蓝图
bp_enquiry_items = Blueprint('enquiry_items', __name__, url_prefix='/enquiry/items')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


@bp_enquiry_items.route('/lists.html', methods=['GET', 'POST'])
@login_required
@permission_enquiry_section_search.require(http_exception=403)
def lists():
    """
    询价列表
    :return:
    """
    template_name = 'enquiry/items/lists.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('enquiry item lists')

    # 搜索条件
    form = EnquiryItemsSearchForm(request.form)
    # form.uid.choices = get_enquiry_user_list_choices()
    # app.logger.info('')

    search_condition = [
        EnquiryItems.status_delete == STATUS_DEL_NO,
    ]
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Search Failure'), 'danger')
            # 单独处理csrf_token
            if hasattr(form, 'csrf_token') and getattr(form, 'csrf_token').errors:
                map(lambda x: flash(x, 'danger'), form.csrf_token.errors)
        else:
            if form.supplier_cid.data and form.supplier_company_name.data:
                search_condition.append(EnquiryItems.supplier_cid == form.supplier_cid.data)
            if form.production_model.data:
                # 注意查询效率
                search_condition.append(
                    or_(
                        EnquiryItems.production_model.like('%%%s%%' % form.production_model.data),
                        EnquiryItems.enquiry_production_model.like('%%%s%%' % form.production_model.data)
                    )
                )
            if form.start_create_time.data:
                search_condition.append(EnquiryItems.create_time >= form.start_create_time.data)
            if form.end_create_time.data:
                search_condition.append(EnquiryItems.create_time <= form.end_create_time.data)
        # 处理导出
        if form.op.data == OPERATION_EXPORT:
            # 检查导出权限
            if not permission_enquiry_section_export.can():
                abort(403)
            column_names = EnquiryItems.__table__.columns.keys()
            query_sets = get_enquiry_items_rows(*search_condition)

            return excel.make_response_from_query_sets(
                query_sets=query_sets,
                column_names=column_names,
                file_type='csv',
                file_name='%s.csv' % _('enquiry item lists')
            )
    # 翻页数据
    pagination = get_enquiry_items_pagination(form.page.data, PER_PAGE_BACKEND, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )
