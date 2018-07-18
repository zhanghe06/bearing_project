#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: orders_buyer.py
@time: 2018-07-16 18:01
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
from flask_login import login_required, current_user

from app_backend import (
    app,
    excel,
)

# 定义蓝图
bp_buyer_orders = Blueprint('buyer_orders', __name__, url_prefix='/buyer_orders')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


@bp_buyer_orders.route('/lists.html', methods=['GET', 'POST'])
@bp_buyer_orders.route('/lists/<int:page>.html', methods=['GET', 'POST'])
@login_required
def lists(page=1):
    return jsonify({})


@bp_buyer_orders.route('/add.html', methods=['GET', 'POST'])
@login_required
def add():
    return jsonify({})


@bp_buyer_orders.route('/stats.html', methods=['GET', 'POST'])
@login_required
def stats():
    return jsonify({})

