#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: quotation_item.py
@time: 2018-03-16 10:00
"""


from __future__ import unicode_literals

import json
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
from flask_babel import gettext as _
from flask_login import login_required, current_user

from app_backend.api.catalogue import get_catalogue_choices
from app_backend.api.customer import get_customer_choices, get_customer_row_by_id
from app_backend.api.user import get_user_choices
from app_backend.forms.production import ProductionSelectForm
from app_backend.forms.quotation import QuotationItemEditForm
from app_backend import (
    app,
    excel,
)
from app_backend.api.quotation import (
    get_quotation_pagination,
    get_quotation_row_by_id,
    add_quotation,
    edit_quotation,
    get_quotation_rows,
    get_distinct_quotation_uid,
    get_distinct_quotation_cid,
    quotation_total_stats,
    quotation_order_stats,
    get_quotation_user_list_choices, get_quotation_customer_list_choices)

from app_backend.api.quotation_item import get_quotation_item_rows, add_quotation_item, edit_quotation_item, \
    delete_quotation_item, get_quotation_item_pagination
from wtforms.fields import FieldList, FormField
from app_backend.forms.quotation import (
    QuotationSearchForm,
    QuotationAddForm,
    QuotationEditForm,
)
from app_backend.forms.quotation_item import QuotationItemSearchForm
from app_backend.models.bearing_project import Quotation, QuotationItems
from app_backend.permissions import (
    permission_quotation_section_add,
    permission_quotation_section_search,
    permission_quotation_section_export,
    permission_quotation_section_stats,
    QuotationItemGetPermission,
    QuotationItemEditPermission,
    QuotationItemDelPermission,
)
from app_common.maps.default import default_choices_int, default_choice_option_int
from app_common.maps.status_delete import (
    STATUS_DEL_OK,
    STATUS_DEL_NO)
from app_common.maps.status_order import STATUS_ORDER_CHOICES
from app_common.maps.type_role import (
    TYPE_ROLE_SALES,
)
from app_common.tools import json_default

# 定义蓝图
bp_quotation_item = Blueprint('quotation_item', __name__, url_prefix='/quotation/item')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


@bp_quotation_item.route('/lists.html', methods=['GET', 'POST'])
@bp_quotation_item.route('/lists/<int:page>.html', methods=['GET', 'POST'])
@login_required
@permission_quotation_section_search.require(http_exception=403)
def lists(page=1):
    """
    报价列表
    :param page:
    :return:
    """
    template_name = 'quotation_item/lists.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('quotation item lists')

    # 搜索条件
    form = QuotationItemSearchForm(request.form)
    # form.uid.choices = get_quotation_user_list_choices()
    # app.logger.info('')

    search_condition = [
        QuotationItems.status_delete == STATUS_DEL_NO,
    ]
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Search Failure'), 'danger')
            # 单独处理csrf_token
            if hasattr(form, 'csrf_token') and getattr(form, 'csrf_token').errors:
                map(lambda x: flash(x, 'danger'), form.csrf_token.errors)
        else:
            if form.cid.data and form.company_name.data:
                search_condition.append(QuotationItems.cid == form.cid.data)
            if form.production_model.data:
                search_condition.append(QuotationItems.production_model.like('%%%s%%' % form.production_model.data))
            if form.start_create_time.data:
                search_condition.append(QuotationItems.create_time >= form.start_create_time.data)
            if form.end_create_time.data:
                search_condition.append(QuotationItems.create_time <= form.end_create_time.data)
        # 处理导出
        if form.op.data == 1:
            # 检查导出权限
            if not permission_quotation_section_export.can():
                abort(403)
            column_names = QuotationItems.__table__.columns.keys()
            query_sets = get_quotation_item_rows(*search_condition)

            return excel.make_response_from_query_sets(
                query_sets=query_sets,
                column_names=column_names,
                file_type='csv',
                file_name='%s.csv' % _('quotation item lists')
            )
    # 翻页数据
    pagination = get_quotation_item_pagination(page, PER_PAGE_BACKEND, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )
