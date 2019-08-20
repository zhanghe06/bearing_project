#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: captcha.py
@time: 2018-03-17 22:20
"""

from flask import (
    Blueprint,
    request,
    make_response,
    session,
    abort,
    jsonify,
)
# from StringIO import StringIO     # PY2
# from io import StringIO           # PY3
from six import StringIO

from app_backend import app
from app_common.libs.captcha import Captcha

# 定义蓝图
bp_captcha = Blueprint('captcha', __name__, url_prefix='/captcha')

# 加载配置
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})
CAPTCHA_CONFIG = app.config.get('CAPTCHA_CONFIG', {})


@bp_captcha.route('/get_code/<code_type>/')
def get_code(code_type):
    """
    http://localhost:8000/captcha/get_code/reg/?t=1234
    """
    if code_type not in app.config['CAPTCHA_ENTITY']:
        abort(404)
    code_img, code_str = Captcha(**CAPTCHA_CONFIG).get()
    # 保存 code_str
    code_key = '%s:%s' % ('code_str', code_type)
    session[code_key] = code_str
    # 返回验证码图片
    buf = StringIO()
    code_img.save(buf, 'JPEG', quality=100)
    buf_str = buf.getvalue()
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/jpeg'
    code_img.close()
    buf.close()
    return response


@bp_captcha.route('/check_code/<code_type>/')
def check_code(code_type):
    """
    校验验证码
    http://localhost:8000/captcha/check_code/reg/?code_str=7E6G
    """
    if code_type not in app.config['CAPTCHA_ENTITY']:
        abort(404)

    ajax_success_msg = AJAX_SUCCESS_MSG.copy()
    ajax_failure_msg = AJAX_FAILURE_MSG.copy()

    code_str = request.args.get('code_str', '', type=str)
    code_key = '%s:%s' % ('code_str', code_type)
    check_result = code_str.upper() == session.pop(code_key, '').upper()

    if check_result:
        return jsonify(ajax_success_msg)
    return jsonify(ajax_failure_msg)
