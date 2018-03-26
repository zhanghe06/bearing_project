#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: __init__.py.py
@time: 2018-03-06 00:18
"""

from __future__ import unicode_literals

import os
from datetime import datetime
import json
import traceback

from flask import current_app, Response
from sqlalchemy.exc import OperationalError
from flask import send_from_directory
from flask_principal import (
    identity_changed,
    Identity,
    AnonymousIdentity,
    identity_loaded,
    RoleNeed,
    UserNeed
)

from flask import (
    g,
    request,
    render_template,
    jsonify,
    session,
    redirect,
    url_for,
    flash
)
from flask_login import (
    login_user,
    logout_user,
    current_user,
    login_required,
    user_loaded_from_cookie
)

from app_backend.api.login_user import get_login_user_row_by_id
from app_backend.api.customer import get_customer_rows
from app_backend.api.role import get_role_row_by_id

from app_backend import app, oauth_github, oauth_qq, oauth_weibo
from flask_babel import gettext as _, ngettext

from app_backend import app, login_manager, babel
from app_backend.permissions import (
    permission_role_administrator,
    SectionNeed,
    EditCustomerItemNeed
)


DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})


@login_manager.user_loader
def load_user(user_id):
    """
    如果 user_id 无效，它应该返回 None （ 而不是抛出异常 ）。
    :param user_id:
    :return:
    """
    return get_login_user_row_by_id(int(user_id))


@app.before_request
def before_request():
    """
    当前用户信息
    """
    # g.user = current_user
    if current_user.is_authenticated:
        session['status_login'] = True
    else:
        session['status_login'] = False


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

        # 客户编辑权限
        customer_rows_condition = {
            'owner_uid': current_user.id
        }
        customer_rows = get_customer_rows(**customer_rows_condition)
        for customer_row in customer_rows:
            edit_customer_need = EditCustomerItemNeed(unicode(customer_row.id))
            identity.provides.add(edit_customer_need)

    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if hasattr(current_user, 'role_id'):
        role_row = get_role_row_by_id(current_user.role_id)
        sections = role_row.section.split(',') if role_row else []
        for section in sections:
            section_need = SectionNeed(section)
            identity.provides.add(section_need)


@user_loaded_from_cookie.connect_via(app)
def on_user_loaded_from_cookie(sender, user):
    """
    记住密码后，通过cookie加载用户，需要重新赋予权限，否则权限会丢失
    :param sender:
    :param user:
    :return:
    """
    identity_changed.send(app, identity=Identity(user.id))


# @babel.localeselector
# def get_locale():
#     return 'zh_Hans_CN'
#     # if a user is logged in, use the locale from the user settings
#     user = getattr(g, 'user', None)
#     if user is not None:
#         return user.locale
#     # otherwise try to guess the language from the user accept
#     # header the browser transmits.  We support de/fr/en in this
#     # example.  The best match wins.
#     return request.accept_languages.best_match(['de', 'fr', 'en'])
#
#
# @babel.timezoneselector
# def get_timezone():
#     user = getattr(g, 'user', None)
#     if user is not None:
#         return user.timezone


@app.route('/favicon.ico')
def favicon():
    """
    首页ico图标
    """
    return send_from_directory(
        app.static_folder,
        'img/favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )


@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    """
    爬虫协议、网站地图
    :return:
    """
    return send_from_directory(app.static_folder, request.path[1:])


@app.route('/')
@app.route('/index.html')
@login_required
def index():
    """
    后台首页
    """
    # return "Hello, World!"
    # return str(current_user.__dict__)
    document_info = DOCUMENT_INFO.copy()
    return render_template('index.html', **document_info)


@app.route('/home.html')
# @login_required
def home():
    """
    个人中心
    """
    return "home"
    # return str(current_user.__dict__)
    document_info = DOCUMENT_INFO.copy()
    return render_template('home.html', **document_info)


@app.route('/logout/')
def logout():
    """
    退出登录
    """
    logout_user()
    session.pop('qq_token', None)
    session.pop('weibo_token', None)
    session.pop('github_token', None)

    # 退出权限
    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(app, identity=AnonymousIdentity())

    flash(_('Exit Success'), 'info')
    return redirect(url_for('auth.index'))


@app.route('/test_permission_role_administrator/')
@permission_role_administrator.require(http_exception=403)
def test_permission_role_administrator():
    """
    管理员权限测试
    :return:
    """
    return Response('Only if you are admin')


@app.route('/stream/')
def stream():
    """
    流式响应
    http://0.0.0.0:8010/stream/
    :return:
    """
    import time

    def gen():
        for c in 'Hello world!':
            yield c
            time.sleep(0.5)
    return Response(gen())


@app.route('/stream_with_context/')
def stream_with_context():
    """
    http://0.0.0.0:8010/stream_with_context/?name=Administrator
    :return:
    """
    import time
    from flask import stream_with_context, request, Response

    def generate():
        for i in 'Hello %s!' % (request.args.get('name', '')):
            time.sleep(0.5)
            yield i
    return Response(stream_with_context(generate()))


@app.errorhandler(401)
def unauthorized(error):
    flash(_('Unauthorized'), 'warning')
    return render_template('http_exception/401.html'), 401


@app.errorhandler(403)
def forbidden(error):
    flash(_('Forbidden'), 'warning')
    session['redirected_from'] = request.url
    return render_template('http_exception/403.html'), 403
    # return redirect(request.args.get('next') or url_for('index'))


@app.errorhandler(404)
def not_found(error):
    flash(_('Not Found'), 'warning')
    return render_template('http_exception/404.html'), 404


@app.errorhandler(405)
def method_not_allowed(error):
    flash(_('Method Not Allowed'), 'warning')
    return render_template('http_exception/405.html'), 405


@app.errorhandler(410)
def gone(error):
    flash(_('Gone'), 'warning')
    return render_template('http_exception/410.html'), 410


@app.errorhandler(413)
def request_entity_too_large(error):
    flash(_('Request Entity Too Large'), 'warning')
    # return '文件超出大小限制', 413
    return render_template('http_exception/413.html'), 413


@app.errorhandler(429)
def too_many_requests(error):
    flash(_('Too Many Requests'), 'warning')
    return render_template('http_exception/429.html'), 429


@app.errorhandler(500)
def internal_server_error(error):
    flash(_('Internal Server Error'), 'warning')
    return render_template('http_exception/500.html'), 500
