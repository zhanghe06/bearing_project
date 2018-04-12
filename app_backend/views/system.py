#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: system.py
@time: 2018-04-11 17:34
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

from app_backend.forms.system import CatalogueUploadForm
from app_backend.models.bearing_project import Rack
from app_backend.permissions import (
    permission_role_administrator,
)


# 定义蓝图
from app_common.tools.file import get_file_size, bytes2human

bp_system = Blueprint('system', __name__, url_prefix='/system')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


@bp_system.route("/catalogue", methods=['GET', 'POST'])
@login_required
@permission_role_administrator.require(http_exception=403)
def catalogue():
    template_name = 'system/catalogue.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('catalogue upload')

    # 加载表单
    form = CatalogueUploadForm(request.form)

    if request.method == 'POST':
        ajax_success_msg = AJAX_SUCCESS_MSG.copy()
        ajax_failure_msg = AJAX_FAILURE_MSG.copy()
        try:
            # files = []
            file_item = request.files.get('file')
            # todo 校验格式
            # todo 执行导入
            # csv_data = request.get_array(field_name='file')

            file_info = {
                'name': file_item.filename,
                'content_type': file_item.content_type,
                'size': bytes2human(get_file_size(file_item)),
            }

            # files.append(file_info)

            ajax_success_msg['file'] = file_info
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
