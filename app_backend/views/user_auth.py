#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: user_auth.py
@time: 2018-03-16 10:02
"""

from __future__ import unicode_literals

import json
from datetime import datetime

from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    flash,
)
from flask_babel import gettext as _
from flask_login import (
    current_user,
    login_user,
    fresh_login_required)
from flask_principal import (
    Identity,
    identity_changed,
)

from app_backend import app
from app_backend.api.login_user import get_login_user_row_by_id
from app_backend.api.user_auth import get_user_auth_row, edit_user_auth
from app_backend.forms.user_auth import UserAuthForm, UserAuthChangePasswordForm, UserAuthEmailForm
from app_backend.tasks.send_mail_login import pub
from app_common.libs.auth_token import AuthToken
from app_common.maps.status_verified import STATUS_VERIFIED_OK
from app_common.maps.type_auth import TYPE_AUTH_ACCOUNT, TYPE_AUTH_EMAIL
from app_common.tools.date_time import get_tc

bp_auth = Blueprint('auth', __name__, url_prefix='/auth')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})
PREFERRED_URL_SCHEME = app.config.get('PREFERRED_URL_SCHEME', 'http')


@bp_auth.route('/index.html', methods=['GET', 'POST'])
def index():
    """
    账号登录认证
    """
    if current_user and current_user.is_authenticated:
        return redirect(url_for('index'))

    template_name = 'user_auth/index.html'

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('Sign in with account')

    # 加载表单
    form = UserAuthForm(request.form)

    # 进入页面
    if request.method == 'GET':
        # 渲染页面
        return render_template(
            template_name,
            form=form,
            t=get_tc(),
            **document_info
        )
    # 处理认证
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Auth Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                t=get_tc(),
                **document_info
            )
        # 表单校验成功
        condition = {
            'type_auth': TYPE_AUTH_ACCOUNT,
            'auth_key': form.auth_key.data,
            # 'auth_secret': form.auth_secret.data
        }
        user_auth_info = get_user_auth_row(**condition)
        if not user_auth_info:
            form.auth_key.errors.append(_('Username Error'))
            flash(_('Auth Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                t=get_tc(),
                **document_info
            )
        if user_auth_info.status_verified != STATUS_VERIFIED_OK:
            form.auth_key.errors.append(_('Need Verify'))
            flash(_('Auth Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                t=get_tc(),
                **document_info
            )
        if user_auth_info.auth_secret != form.auth_secret.data:
            form.auth_secret.errors.append(_('Password Error'))
            flash(_('Auth Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                t=get_tc(),
                **document_info
            )

        # 认证成功
        # 用户登录
        login_user(get_login_user_row_by_id(user_auth_info.user_id), remember=form.remember.data)

        # 加载权限信号通知(Tell Flask-Principal the identity changed)
        identity_changed.send(app, identity=Identity(user_auth_info.user_id))

        flash(_('Auth Success'), 'success')
        return redirect(request.args.get('next') or url_for('index'))


@bp_auth.route('/email.html', methods=['GET', 'POST'])
def email():
    """
    邮箱登录（邮箱链接登录）
    """
    if current_user and current_user.is_authenticated:
        return redirect(url_for('index'))

    template_name = 'user_auth/email.html'

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('Sign in with email')

    # 加载表单
    form = UserAuthEmailForm(request.form)

    # 进入页面
    if request.method == 'GET':
        # 渲染页面
        return render_template(
            template_name,
            form=form,
            t=get_tc(),
            **document_info
        )
    # 处理认证
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Auth Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                t=get_tc(),
                **document_info
            )
        # 表单校验成功
        condition = {
            'type_auth': TYPE_AUTH_EMAIL,
            'auth_key': form.auth_key.data,
            # 'auth_secret': form.auth_secret.data
        }
        user_auth_info = get_user_auth_row(**condition)
        if not user_auth_info:
            form.auth_key.errors.append(_('Email not exist'))
            flash(_('Auth Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                t=get_tc(),
                **document_info
            )
        user_id = user_auth_info.user_id
        auth_token_obj = AuthToken(app.secret_key)
        token = auth_token_obj.create(user_id)

        # send email task
        message = json.dumps(
            {
                'name': '尊敬的用户',
                'email': form.auth_key.data,
                'link': url_for('sign', auth_token=token, _external=True, _scheme=PREFERRED_URL_SCHEME)
            }
        )

        result = pub(form.auth_key.data, message)
        if not result:
            flash(_('Repeat application, Enter mailbox, click the authentication link to sign in'), 'success')
        else:
            flash(_('Auth Success, Enter mailbox, click the authentication link to sign in'), 'success')
        return render_template(
            template_name,
            form=form,
            t=get_tc(),
            **document_info
        )


@app.route('/change_password.html', methods=['GET', 'POST'])
@fresh_login_required
def change_password():
    """
    修改密码
    """
    template_name = 'user_auth/change_password.html'

    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('change password')

    # 加载表单
    form = UserAuthChangePasswordForm(request.form)

    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Change Password Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                **document_info
            )

        # 获取 user_auth_id
        condition = {
            'user_id': current_user.id,
            'type_auth': TYPE_AUTH_ACCOUNT,
        }
        user_auth_info = get_user_auth_row(**condition)
        if not user_auth_info:
            flash(_('Cann\'t Change Password'), 'danger')
            return render_template(
                template_name,
                form=form,
                **document_info
            )
        elif user_auth_info.auth_secret != form.password_current.data:
            flash(_('Current Password Error'), 'danger')
            return render_template(
                template_name,
                form=form,
                **document_info
            )

        # 表单校验成功
        user_auth_id = user_auth_info.id
        current_time = datetime.utcnow()
        user_auth_data = {
            'auth_secret': form.password_new.data,
            'status_verified': STATUS_VERIFIED_OK,
            'update_time': current_time,
        }

        result = edit_user_auth(user_auth_id, user_auth_data)
        # 编辑操作成功
        if result:
            flash(_('Edit Success'), 'success')
            return redirect(request.args.get('next') or url_for('change_password'))
        # 编辑操作失败
        else:
            flash(_('Edit Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                **document_info
            )

    return render_template(
        template_name,
        form=form,
        **document_info
    )
