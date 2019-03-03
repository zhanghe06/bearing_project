#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: catalogue.py
@time: 2018-04-16 21:54
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

from app_backend import app
from app_backend import excel
from app_backend.api.catalogue import (
    get_catalogue_pagination,
    get_catalogue_row_by_id,
    add_catalogue,
    edit_catalogue,
    # production_current_stats,
    # production_former_stats,
)
from app_backend.api.production import (
    get_production_rows,
    get_distinct_production_brand,
)
from app_backend.forms.production import (
    ProductionSearchForm,
    ProductionAddForm,
    ProductionEditForm,
)
from app_backend.models.bearing_project import Catalogue
from app_backend.permissions import (
    permission_catalogue_section_add,
    permission_catalogue_section_search,
    permission_catalogue_section_export,
    permission_catalogue_section_stats,
    permission_role_administrator,
)
from app_common.maps.default import default_search_choices_str, default_search_choice_option_str
from app_common.maps.status_delete import (
    STATUS_DEL_OK,
)
from app_common.maps.type_role import TYPE_ROLE_MANAGER
from app_common.tools import json_default

# 定义蓝图
bp_catalogue = Blueprint('catalogue', __name__, url_prefix='/catalogue')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


def get_production_brand_choices():
    production_brand_list = copy(default_search_choices_str)
    distinct_brand = get_distinct_production_brand()
    production_brand_list.extend([(brand, brand) for brand in distinct_brand])
    return production_brand_list


@bp_catalogue.route('/lists.html', methods=['GET', 'POST'])
@bp_catalogue.route('/lists/<int:page>.html', methods=['GET', 'POST'])
@login_required
@permission_production_section_search.require(http_exception=403)
def lists(page=1):
    """
    产品列表
    :param page:
    :return:
    """
    template_name = 'catalogue/lists.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('catalogue lists')

    # 搜索条件
    form = ProductionSearchForm(request.form)
    form.production_brand.choices = get_production_brand_choices()
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
            if form.production_brand.data != default_search_choice_option_str:
                search_condition.append(Production.production_brand == form.production_brand.data)
            if form.production_model.data:
                search_condition.append(Production.production_model == form.production_model.data)
        # 处理导出
        if form.op.data == 1:
            # 检查导出权限
            if not permission_production_section_export.can():
                abort(403)
            column_names = Production.__table__.columns.keys()
            query_sets = get_production_rows(*search_condition)

            return excel.make_response_from_query_sets(
                query_sets=query_sets,
                column_names=column_names,
                file_type='csv',
                file_name='%s.csv' % _('catalogue lists')
            )
    # 翻页数据
    pagination = get_catalogue_pagination(page, PER_PAGE_BACKEND, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )
