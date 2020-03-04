#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: system.py
@time: 2018-04-11 17:34
"""

from __future__ import unicode_literals

from flask import (
    request,
    render_template,
    jsonify,
    Blueprint,
)
from flask_babel import gettext as _
from flask_login import login_required

from app_backend import app
from app_backend.api.catalogue import delete_catalogue_table, count_catalogue, add_catalogue
from app_backend.api.futures import delete_futures_table, add_futures, count_futures
from app_backend.api.production import delete_production_table, count_production, add_production
from app_backend.api.quotation import delete_quotation_table, count_quotation, add_quotation
from app_backend.forms.system import CatalogueUploadForm
from app_backend.forms.system import ProductionUploadForm
from app_backend.forms.system import QuotationUploadForm
from app_backend.models.model_bearing import Catalogue
from app_backend.models.model_bearing import Production
from app_backend.models.model_bearing import Quotation
from app_backend.permissions import (
    permission_role_administrator,
)
from app_common.maps.type_tax import TYPE_TAX_NOT
# 定义蓝图
from app_common.tools.file import get_file_size, bytes2human

bp_system = Blueprint('system', __name__, url_prefix='/system')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


@bp_system.route("/catalogue_import", methods=['GET', 'POST'])
@login_required
@permission_role_administrator.require(http_exception=403)
def catalogue_import():
    """
    型录导入
    :return:
    """
    template_name = 'system/catalogue_import.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('catalogue import')

    # 加载表单
    form = CatalogueUploadForm(request.form)

    if request.method == 'POST':
        ajax_success_msg = AJAX_SUCCESS_MSG.copy()
        ajax_failure_msg = AJAX_FAILURE_MSG.copy()
        try:
            # files = []
            file_item = request.files.get('file')
            csv_data = request.get_array(field_name='file')
            # 校验数据是否有效
            if len(csv_data) < 3:
                raise Exception('数据错误')
            csv_data.pop(0)
            csv_head = csv_data.pop(0)

            csv_count = len(csv_data)

            column_names = Catalogue.__table__.columns.keys()

            if not set(csv_head).issubset(set(column_names)):
                raise Exception('数据错误')
            # 清空历史
            delete_count = delete_catalogue_table()
            # 执行导入
            for item in csv_data:
                add_catalogue(dict(zip(csv_head, item)))

            file_info = {
                'name': file_item.filename,
                'content_type': file_item.content_type,
                'size': bytes2human(get_file_size(file_item)),
            }

            import_info = {
                'delete_count': delete_count,
                'csv_count': csv_count,
                'db_count': count_catalogue(),
            }

            # files.append(file_info)

            ajax_success_msg['file_info'] = file_info
            ajax_success_msg['import_info'] = import_info
            return jsonify(ajax_success_msg)
        except Exception as e:
            ajax_failure_msg['msg'] = e.message
            return jsonify(ajax_failure_msg)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        **document_info
    )


@bp_system.route("/production_import", methods=['GET', 'POST'])
@login_required
# @permission_role_administrator.require(http_exception=403)
def production_import():
    """
    产品导入
    :return:
    """
    template_name = 'system/production_import.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('production import')

    # 加载表单
    form = ProductionUploadForm(request.form)

    if request.method == 'POST':
        ajax_success_msg = AJAX_SUCCESS_MSG.copy()
        ajax_failure_msg = AJAX_FAILURE_MSG.copy()
        try:
            # files = []
            file_item = request.files.get('file')
            csv_data = request.get_array(field_name='file')
            # 校验数据是否有效
            if len(csv_data) < 3:
                raise Exception('数据错误')
            csv_data.pop(0)
            csv_head = csv_data.pop(0)

            csv_count = len(csv_data)

            column_names = Production.__table__.columns.keys()

            if not set(csv_head).issubset(set(column_names)):
                raise Exception('数据错误')
            # 清空历史
            delete_count = delete_production_table()
            # 执行导入
            for item in csv_data:
                add_production(dict(zip(csv_head, item)))

            file_info = {
                'name': file_item.filename,
                'content_type': file_item.content_type,
                'size': bytes2human(get_file_size(file_item)),
            }

            import_info = {
                'delete_count': delete_count,
                'csv_count': csv_count,
                'db_count': count_production(),
            }

            # files.append(file_info)

            ajax_success_msg['file_info'] = file_info
            ajax_success_msg['import_info'] = import_info
            return jsonify(ajax_success_msg)
        except Exception as e:
            ajax_failure_msg['msg'] = e.message
            return jsonify(ajax_failure_msg)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        **document_info
    )


@bp_system.route("/quotation_import", methods=['GET', 'POST'])
@login_required
@permission_role_administrator.require(http_exception=403)
def quotation_import():
    """
    报价导入
    :return:
    """
    template_name = 'system/quotation_import.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('quotation import')

    # 加载表单
    form = QuotationUploadForm(request.form)

    if request.method == 'POST':
        ajax_success_msg = AJAX_SUCCESS_MSG.copy()
        ajax_failure_msg = AJAX_FAILURE_MSG.copy()
        try:
            # files = []
            file_item = request.files.get('file')
            csv_data = request.get_array(field_name='file')
            # 校验数据是否有效
            if len(csv_data) < 3:
                raise Exception('数据错误')
            csv_data.pop(0)
            csv_head = csv_data.pop(0)

            csv_count = len(csv_data)

            column_names = Quotation.__table__.columns.keys()

            if not set(csv_head).issubset(set(column_names)):
                raise Exception('数据错误')
            # 清空历史
            delete_count = delete_quotation_table()
            # 执行导入
            for item in csv_data:
                add_quotation(dict(zip(csv_head, item)))

            file_info = {
                'name': file_item.filename,
                'content_type': file_item.content_type,
                'size': bytes2human(get_file_size(file_item)),
            }

            import_info = {
                'delete_count': delete_count,
                'csv_count': csv_count,
                'db_count': count_quotation(),
            }

            # files.append(file_info)

            ajax_success_msg['file_info'] = file_info
            ajax_success_msg['import_info'] = import_info
            return jsonify(ajax_success_msg)
        except Exception as e:
            ajax_failure_msg['msg'] = e.message
            return jsonify(ajax_failure_msg)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        **document_info
    )


@bp_system.route("/futures_import", methods=['GET', 'POST'])
@login_required
# @permission_role_administrator.require(http_exception=403)
def futures_import():
    """
    在途导入
    :return:
    """
    template_name = 'system/futures_import.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('futures import')

    # 加载表单
    form = CatalogueUploadForm(request.form)

    if request.method == 'POST':
        ajax_success_msg = AJAX_SUCCESS_MSG.copy()
        ajax_failure_msg = AJAX_FAILURE_MSG.copy()
        try:
            # files = []
            file_item = request.files.get('file')
            csv_data = request.get_array(field_name='file')
            # 校验数据是否有效
            if len(csv_data) < 3:
                raise Exception('数据错误')
            # csv_data.pop(0)
            csv_head = csv_data.pop(0)
            print(csv_head)

            skf_head = [
                'Sales Name', 'Customer ID', 'Short Name', 'Cust Order ID', 'Line.', 'Split L',
                'Customers own ord ID', 'Product Desgn', 'Product Desgn1', 'Text', 'Req qty',
                'Package Code',
                'Country/Manufactured', 'RTW Date', 'Last date shipped', 'Acc Del Date', 'Req del date',
                'Transport Code', 'Warehouse Ident', 'Currency code', 'Order line status',
                'Good Receiving Date',
                'Loading Set number', 'Unit Price', 'Net Sales', 'Run Date', 'DD Code', 'Diff Acc Days',
                'Diff RTW Days'
            ]
            
            skf_head = [
                '客户号', '客户简称', '客户订单号', '系统订单号', '系统行号', '系统分行号', '型号', '客户物料号', '订单备注', '要求交货数量', '本币单价',
                '订单总额（本币）', '单价', '订单发货确认', '跟踪理由', '包装代码', '产地', '订单包装日', '发货日期', '当前确认的交货期', '要求交货期',
                '运输方式(TMC)', '配送中心', '仓库', '订单状态', '实到库时间', '箱单号', '开发票日期', '配送时间', '发票控制代码', '订单控制代码',
                '仓库指令代码', '供应商订单号', '供应商订单行', '供应商订单分行', '供应商发票号', '供应商', '公司代码', '确认的上一个交货期', '订单货期改变次数',
                '货期差异', '信贷状态', '新计划交货日期', '币种', '销售员', '销售经理', '经销商集团', '信用证是否收到', '信用证收取截止日',
            ]

            skf_map = {
                'Customer ID': 'supplier_company_name',
                # '': 'production_brand',
                'Product Desgn': 'production_model',
                'Currency code': 'currency',
                'Req del date': 'req_date',
                'Acc Del Date': 'acc_date',
                'Req qty': 'quantity',
                'Unit Price': 'unit_price',
                'Net Sales': 'sub_total',
                'Customers own ord ID': 'note',
            }

            skf_map = {
                '客户号': 'supplier_company_name',
                # '': 'production_brand',
                '型号': 'production_model',
                '币种': 'currency',
                '要求交货期': 'req_date',
                '当前确认的交货期': 'acc_date',
                '要求交货数量': 'quantity',
                '单价': 'unit_price',
                '订单总额（本币）': 'sub_total',
                '客户订单号': 'note',
            }

            csv_count = len(csv_data)

            # column_names = Catalogue.__table__.columns.keys()

            if not set(csv_head).issubset(set(skf_head)):
                raise Exception('数据错误')
            # 清空历史
            delete_count = delete_futures_table()
            # 执行导入
            for csv_item in csv_data:
                d = {}
                data_csv_item = dict(zip(csv_head, csv_item))
                for k, v in data_csv_item.items():
                    if k not in skf_map:
                        continue
                    d[skf_map[k]] = v

                d['production_brand'] = 'SKF'
                d['type_tax'] = TYPE_TAX_NOT
                add_futures(d)

            file_info = {
                'name': file_item.filename,
                'content_type': file_item.content_type,
                'size': bytes2human(get_file_size(file_item)),
            }

            import_info = {
                'delete_count': delete_count,
                'csv_count': csv_count,
                'db_count': count_futures(),
            }

            # files.append(file_info)

            ajax_success_msg['file_info'] = file_info
            ajax_success_msg['import_info'] = import_info
            return jsonify(ajax_success_msg)
        except Exception as e:
            ajax_failure_msg['msg'] = e.message
            return jsonify(ajax_failure_msg)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        **document_info
    )
