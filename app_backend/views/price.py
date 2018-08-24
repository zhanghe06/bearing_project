#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: price.py
@time: 2018-08-22 18:34
"""


from __future__ import unicode_literals

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

from app_backend import (
    app,
    excel,
)
from flask_babel import gettext as _
from flask_login import login_required
from app_common.maps.default import default_choices_int, default_choice_option_int
from app_common.maps.status_delete import (
    STATUS_DEL_OK,
    STATUS_DEL_NO)
from app_common.maps.type_company import TYPE_COMPANY_CHOICES
from app_common.maps.type_role import (
    TYPE_ROLE_SALES,
)
from app_backend.permissions import permission_customer_section_search

# 定义蓝图
bp_price = Blueprint('price', __name__, url_prefix='/price')


# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
PER_PAGE_BACKEND_MODAL = app.config.get('PER_PAGE_BACKEND_MODAL', 10)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


@bp_price.route('/search.html', methods=['GET', 'POST'])
@login_required
@permission_customer_section_search.require(http_exception=403)
def search():
    """
    价格搜索
    1、当前型号-价格情况
    2、当前型号-价格情况
        2.1、报价记录（日期、客户、型号、数量、单价、货期）
        2.2、销售记录（日期、客户、型号、数量、单价）
        2.3、采购记录（日期、供应商、型号、数量、货期）
        2.4、库存成本（型号、最小成本、最大成本、平均成本）
    3、推荐型号
        3.1、当前品牌类似型号
        3.2、其它品牌类似型号
    :return:
    """
    template_name = 'customer/search_modal.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('Customer Search')

    # 搜索条件
    form = CustomerSearchForm(request.form)
    form.owner_uid.choices = get_sales_user_list()
    # app.logger.info('')

    search_condition = [
        Customer.status_delete == STATUS_DEL_NO,
    ]
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Search Failure'), 'danger')
            # 单独处理csrf_token
            if hasattr(form, 'csrf_token') and getattr(form, 'csrf_token').errors:
                map(lambda x: flash(x, 'danger'), form.csrf_token.errors)
        else:
            if form.company_type.data != default_choice_option_int:
                search_condition.append(Customer.company_type == form.company_type.data)
            if form.company_name.data:
                search_condition.append(Customer.company_name.like('%%%s%%' % form.company_name.data))
    # 翻页数据
    pagination = get_customer_pagination(form.page.data, PER_PAGE_BACKEND_MODAL, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )
