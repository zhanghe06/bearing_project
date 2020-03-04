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
    Blueprint,
)
from flask_babel import gettext as _
from flask_login import login_required

from app_backend import (
    app,
)
from app_backend.api.inventory import get_inventory_pagination
from app_backend.api.futures import get_futures_pagination
from app_backend.api.delivery_items import get_delivery_items_pagination
from app_backend.api.enquiry_items import get_enquiry_items_pagination
from app_backend.api.purchase_items import get_purchase_items_pagination
from app_backend.api.quotation_items import get_quotation_items_pagination
from app_backend.forms.price import PriceSearchForm
from app_backend.models.model_bearing import (
    Inventory,
    Futures,
    QuotationItems,
    EnquiryItems,
    DeliveryItems,
    PurchaseItems,
)
from app_common.maps.status_delete import (
    STATUS_DEL_NO)

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
# @permission_customer_section_search.require(http_exception=403)
def search():
    """
    价格搜索
    1、当前型号-价格货期
    2、当前型号-价格历史
        2.1、报价记录（日期、客户、型号、数量、单价、货期）
        2.2、销售记录（日期、客户、型号、数量、单价）
        2.3、采购记录（日期、供应商、型号、数量、货期）
        2.4、库存成本（型号、最小成本、最大成本、平均成本）
    3、推荐型号
        3.1、当前品牌类似型号
        3.2、其它品牌类似型号
    :return:
    """
    template_name = 'price/lists.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('price lists')

    # 搜索条件
    form = PriceSearchForm(request.form)
    # form.uid.choices = get_quotation_user_list_choices()
    # app.logger.info('')

    search_condition_inventory = [
        Inventory.status_delete == STATUS_DEL_NO,
    ]
    search_condition_futures = [
        Futures.status_delete == STATUS_DEL_NO,
    ]
    search_condition_quotation = [
        QuotationItems.status_delete == STATUS_DEL_NO,
    ]
    search_condition_enquiry = [
        EnquiryItems.status_delete == STATUS_DEL_NO,
    ]
    search_condition_delivery = [
        DeliveryItems.status_delete == STATUS_DEL_NO,
    ]
    search_condition_purchase = [
        PurchaseItems.status_delete == STATUS_DEL_NO,
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
                search_condition_quotation.append(QuotationItems.customer_cid == form.cid.data)
                search_condition_enquiry.append(EnquiryItems.supplier_cid == form.cid.data)
                search_condition_delivery.append(DeliveryItems.customer_cid == form.cid.data)
                search_condition_purchase.append(PurchaseItems.supplier_cid == form.cid.data)
            if form.production_model.data:
                search_condition_inventory.append(
                    Inventory.production_model.like('%%%s%%' % form.production_model.data))
                search_condition_futures.append(
                    Futures.production_model.like('%%%s%%' % form.production_model.data))
                search_condition_quotation.append(
                    QuotationItems.production_model.like('%%%s%%' % form.production_model.data))
                search_condition_enquiry.append(
                    EnquiryItems.production_model.like('%%%s%%' % form.production_model.data))
                search_condition_delivery.append(
                    DeliveryItems.production_model.like('%%%s%%' % form.production_model.data))
                search_condition_purchase.append(
                    PurchaseItems.production_model.like('%%%s%%' % form.production_model.data))
            if form.start_create_time.data:
                search_condition_quotation.append(QuotationItems.create_time >= form.start_create_time.data)
                search_condition_enquiry.append(EnquiryItems.create_time >= form.start_create_time.data)
                search_condition_delivery.append(DeliveryItems.create_time >= form.start_create_time.data)
                search_condition_purchase.append(PurchaseItems.create_time >= form.start_create_time.data)
            if form.end_create_time.data:
                search_condition_quotation.append(QuotationItems.create_time <= form.end_create_time.data)
                search_condition_enquiry.append(EnquiryItems.create_time <= form.end_create_time.data)
                search_condition_delivery.append(DeliveryItems.create_time <= form.end_create_time.data)
                search_condition_purchase.append(PurchaseItems.create_time <= form.end_create_time.data)
                # 处理导出
                # if form.op.data == 1:
                #     # 检查导出权限
                #     if not permission_quotation_section_export.can():
                #         abort(403)
                #     column_names = QuotationItems.__table__.columns.keys()
                #     query_sets = get_quotation_items_rows(*search_condition_quotation)
                #
                #     return excel.make_response_from_query_sets(
                #         query_sets=query_sets,
                #         column_names=column_names,
                #         file_type='csv',
                #         file_name='%s.csv' % _('price lists')
                #     )
    # 翻页数据
    pagination_inventory = get_inventory_pagination(form.page.data, PER_PAGE_BACKEND, *search_condition_inventory)
    pagination_futures = get_futures_pagination(form.page.data, PER_PAGE_BACKEND, *search_condition_futures)
    pagination_quotation = get_quotation_items_pagination(form.page.data, PER_PAGE_BACKEND, *search_condition_quotation)
    pagination_enquiry = get_enquiry_items_pagination(form.page.data, PER_PAGE_BACKEND, *search_condition_enquiry)
    pagination_delivery = get_delivery_items_pagination(form.page.data, PER_PAGE_BACKEND, *search_condition_delivery)
    pagination_purchase = get_purchase_items_pagination(form.page.data, PER_PAGE_BACKEND, *search_condition_purchase)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination_inventory=pagination_inventory,
        pagination_futures=pagination_futures,
        pagination_quotation=pagination_quotation,
        pagination_enquiry=pagination_enquiry,
        pagination_delivery=pagination_delivery,
        pagination_purchase=pagination_purchase,
        **document_info
    )
