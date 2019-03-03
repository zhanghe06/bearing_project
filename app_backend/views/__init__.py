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
import user_agents

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
from app_backend.api.user import get_user_rows
from app_backend.api.customer import get_customer_rows
from app_backend.api.quotation import get_quotation_rows
from app_backend.api.role import get_role_row_by_id

from app_backend import app, oauth_github, oauth_qq, oauth_weibo
from flask_babel import gettext as _, ngettext

from app_backend import app, login_manager, babel
from app_backend.permissions import (
    SectionActionNeed,
    SectionActionItemNeed,
    permission_role_administrator,
)
from app_common.maps.type_role import (
    TYPE_ROLE_SALES,
    TYPE_ROLE_PURCHASER,
    TYPE_ROLE_MANAGER,
    TYPE_ROLE_SYSTEM,
    TYPE_ROLE_STOREKEEPER,
)

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})

# moment 插件语言映射关系
moment_locale_map = {
    'en': 'en',
    'zh': 'zh-cn'
}


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
    lang = request.accept_languages.best_match(['en', 'zh'], default='zh')
    g.lang = lang
    g.moment_locale = moment_locale_map.get(lang)
    g.user_agent = user_agents.parse(str(request.user_agent))

    # g.user = current_user
    # if current_user.is_authenticated:
    #     session['status_login'] = True
    # else:
    #     session['status_login'] = False

    # 加载基本配置
    g.QUOTATION_PREFIX = app.config.get('QUOTATION_PREFIX', '')  # 报价
    g.ENQUIRIES_PREFIX = app.config.get('ENQUIRIES_PREFIX', '')  # 询价

    g.SALES_ORDER_PREFIX = app.config.get('SALES_ORDER_PREFIX', '')  # 销售订单
    g.BUYER_ORDER_PREFIX = app.config.get('BUYER_ORDER_PREFIX', '')  # 采购订单

    g.DELIVERY_PREFIX = app.config.get('DELIVERY_PREFIX', '')  # 出货
    g.PURCHASE_PREFIX = app.config.get('PURCHASE_PREFIX', '')  # 进货

    g.STATIC_RES_VER = '1.5.26'  # 静态资源版本


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    """
    视图层模块的权限控制
    :param sender:
    :param identity:
    :return:
    """
    # Set the identity user object
    identity.user = current_user

    if not (hasattr(current_user, 'id') and hasattr(current_user, 'role_id')):
        return

    # Add the UserNeed to the identity
    identity.provides.add(UserNeed(current_user.id))

    # 公共权限（用户查询、产品查询、库存查询）
    # 用户查询
    identity.provides.add(SectionActionNeed('user', 'search'))
    # 产品查询
    identity.provides.add(SectionActionNeed('production', 'search'))
    # 库存查询
    identity.provides.add(SectionActionNeed('inventory', 'search'))
    # 仓库查询
    identity.provides.add(SectionActionNeed('warehouse', 'search'))

    # 角色 - 系统
    if current_user.role_id == TYPE_ROLE_SYSTEM:
        # 赋予整体角色权限
        identity.provides.add(RoleNeed('系统'))

        # 版块基本操作权限（系统）
        # 用户-----------------------------------------------------------------------
        # 用户创建
        identity.provides.add(SectionActionNeed('user', 'add'))
        # 用户统计
        identity.provides.add(SectionActionNeed('user', 'stats'))
        # 产品-----------------------------------------------------------------------
        # 产品创建
        identity.provides.add(SectionActionNeed('product', 'add'))
        # 产品统计
        identity.provides.add(SectionActionNeed('product', 'stats'))

        # 版块明细操作权限（系统）
        # 系统角色拥有全部版块权限，不区分明细权限

    # 角色 - 销售
    if current_user.role_id == TYPE_ROLE_SALES:
        # 赋予整体角色权限
        identity.provides.add(RoleNeed('销售'))
        # 版块基本操作权限（销售）
        # （创建、查询、统计）
        # 客户-----------------------------------------------------------------------
        # 客户创建
        identity.provides.add(SectionActionNeed('customer', 'add'))
        # 客户查询
        identity.provides.add(SectionActionNeed('customer', 'search'))
        # 客户统计
        identity.provides.add(SectionActionNeed('customer', 'stats'))
        # 报价-----------------------------------------------------------------------
        # 报价创建
        identity.provides.add(SectionActionNeed('quotation', 'add'))
        # 报价查询
        identity.provides.add(SectionActionNeed('quotation', 'search'))
        # 报价统计
        identity.provides.add(SectionActionNeed('quotation', 'stats'))

        # 版块明细操作权限（销售）
        # （读取、编辑、删除、打印）
        # 客户-----------------------------------------------------------------------
        customer_rows_condition = {
            'owner_uid': current_user.id
        }
        customer_rows = get_customer_rows(**customer_rows_condition)
        for customer_row in customer_rows:
            # 客户读取权限
            identity.provides.add(SectionActionItemNeed('customer', 'get', unicode(customer_row.id)))
            # 客户编辑权限
            identity.provides.add(SectionActionItemNeed('customer', 'edit', unicode(customer_row.id)))
            # 客户删除权限
            identity.provides.add(SectionActionItemNeed('customer', 'del', unicode(customer_row.id)))
            # 客户打印权限
            identity.provides.add(SectionActionItemNeed('customer', 'print', unicode(customer_row.id)))
        # 报价-----------------------------------------------------------------------
        quotation_rows_condition = {
            'uid': current_user.id
        }
        quotation_rows = get_quotation_rows(**quotation_rows_condition)
        for quotation_row in quotation_rows:
            # 报价读取权限
            identity.provides.add(SectionActionItemNeed('quotation', 'get', unicode(quotation_row.id)))
            # 报价编辑权限
            identity.provides.add(SectionActionItemNeed('quotation', 'edit', unicode(quotation_row.id)))
            # 报价删除权限
            identity.provides.add(SectionActionItemNeed('quotation', 'del', unicode(quotation_row.id)))
            # 报价打印权限
            identity.provides.add(SectionActionItemNeed('quotation', 'print', unicode(quotation_row.id)))

    # 角色 - 采购
    if current_user.role_id == TYPE_ROLE_PURCHASER:
        # 赋予整体角色权限
        identity.provides.add(RoleNeed('采购'))
        # 版块基本操作权限（销售）
        # （创建、查询、统计）
        # 渠道-----------------------------------------------------------------------
        # 渠道创建
        identity.provides.add(SectionActionNeed('supplier', 'add'))
        # 渠道查询
        identity.provides.add(SectionActionNeed('supplier', 'search'))
        # 渠道统计
        identity.provides.add(SectionActionNeed('supplier', 'stats'))
        # 询价-----------------------------------------------------------------------
        # 询价创建
        identity.provides.add(SectionActionNeed('enquiry', 'add'))
        # 询价查询
        identity.provides.add(SectionActionNeed('enquiry', 'search'))
        # 询价统计
        identity.provides.add(SectionActionNeed('enquiry', 'stats'))

        # 版块明细操作权限（销售）
        # （读取、编辑、删除、打印）
        # 客户-----------------------------------------------------------------------
        customer_rows_condition = {
            'owner_uid': current_user.id
        }
        customer_rows = get_customer_rows(**customer_rows_condition)
        for customer_row in customer_rows:
            # 客户读取权限
            identity.provides.add(SectionActionItemNeed('customer', 'get', unicode(customer_row.id)))
            # 客户编辑权限
            identity.provides.add(SectionActionItemNeed('customer', 'edit', unicode(customer_row.id)))
            # 客户删除权限
            identity.provides.add(SectionActionItemNeed('customer', 'del', unicode(customer_row.id)))
            # 客户打印权限
            identity.provides.add(SectionActionItemNeed('customer', 'print', unicode(customer_row.id)))
        # 报价-----------------------------------------------------------------------
        quotation_rows_condition = {
            'uid': current_user.id
        }
        quotation_rows = get_quotation_rows(**quotation_rows_condition)
        for quotation_row in quotation_rows:
            # 报价读取权限
            identity.provides.add(SectionActionItemNeed('quotation', 'get', unicode(quotation_row.id)))
            # 报价编辑权限
            identity.provides.add(SectionActionItemNeed('quotation', 'edit', unicode(quotation_row.id)))
            # 报价删除权限
            identity.provides.add(SectionActionItemNeed('quotation', 'del', unicode(quotation_row.id)))
            # 报价打印权限
            identity.provides.add(SectionActionItemNeed('quotation', 'print', unicode(quotation_row.id)))

    # 角色 - 经理
    if current_user.role_id == TYPE_ROLE_MANAGER:
        # 赋予整体角色权限
        identity.provides.add(RoleNeed('经理'))
        # 版块基本操作权限（经理）
        # （创建、查询、统计、导出）
        # 客户-----------------------------------------------------------------------
        # 客户创建
        identity.provides.add(SectionActionNeed('customer', 'add'))
        # 客户查询
        identity.provides.add(SectionActionNeed('customer', 'search'))
        # 客户统计
        identity.provides.add(SectionActionNeed('customer', 'stats'))
        # 客户导出
        identity.provides.add(SectionActionNeed('customer', 'export'))
        # 报价-----------------------------------------------------------------------
        # 报价创建
        identity.provides.add(SectionActionNeed('quotation', 'add'))
        # 报价查询
        identity.provides.add(SectionActionNeed('quotation', 'search'))
        # 报价统计
        identity.provides.add(SectionActionNeed('quotation', 'stats'))
        # 报价导出
        identity.provides.add(SectionActionNeed('quotation', 'export'))

        # 版块明细操作权限（经理）
        # （读取、编辑、删除、打印、审核）
        # 客户-----------------------------------------------------------------------
        customer_rows_condition = {
            'owner_uid': current_user.id
        }
        customer_rows = get_customer_rows(**customer_rows_condition)
        for customer_row in customer_rows:
            # 客户读取权限
            identity.provides.add(SectionActionItemNeed('customer', 'get', unicode(customer_row.id)))
            # 客户编辑权限
            identity.provides.add(SectionActionItemNeed('customer', 'edit', unicode(customer_row.id)))
            # 客户删除权限
            identity.provides.add(SectionActionItemNeed('customer', 'del', unicode(customer_row.id)))
            # 客户打印权限
            identity.provides.add(SectionActionItemNeed('customer', 'print', unicode(customer_row.id)))
        # 报价-----------------------------------------------------------------------
        quotation_rows_condition = {
            'uid': current_user.id
        }
        quotation_rows = get_quotation_rows(**quotation_rows_condition)
        for quotation_row in quotation_rows:
            # 报价读取权限
            identity.provides.add(SectionActionItemNeed('quotation', 'get', unicode(quotation_row.id)))
            # 报价编辑权限
            identity.provides.add(SectionActionItemNeed('quotation', 'edit', unicode(quotation_row.id)))
            # 报价删除权限
            identity.provides.add(SectionActionItemNeed('quotation', 'del', unicode(quotation_row.id)))
            # 报价打印权限
            identity.provides.add(SectionActionItemNeed('quotation', 'print', unicode(quotation_row.id)))
            # 报价审核权限
            identity.provides.add(SectionActionItemNeed('quotation', 'audit', unicode(quotation_row.id)))

        # 版块明细操作权限 - 所属销售（经理）
        sales_rows_condition = {
            'parent_id': current_user.id
        }
        sales_rows = get_user_rows(**sales_rows_condition)
        for sales_item in sales_rows:
            # 客户-----------------------------------------------------------------------
            customer_rows_condition = {
                'owner_uid': sales_item.id
            }
            customer_rows = get_customer_rows(**customer_rows_condition)
            for customer_row in customer_rows:
                # 客户读取权限
                identity.provides.add(SectionActionItemNeed('customer', 'get', unicode(customer_row.id)))
                # 客户编辑权限
                identity.provides.add(SectionActionItemNeed('customer', 'edit', unicode(customer_row.id)))
                # 客户删除权限
                identity.provides.add(SectionActionItemNeed('customer', 'del', unicode(customer_row.id)))
                # 客户打印权限
                identity.provides.add(SectionActionItemNeed('customer', 'print', unicode(customer_row.id)))
            # 报价-----------------------------------------------------------------------
            quotation_rows_condition = {
                'uid': sales_item.id
            }
            quotation_rows = get_quotation_rows(**quotation_rows_condition)
            for quotation_row in quotation_rows:
                # 报价读取权限
                identity.provides.add(SectionActionItemNeed('quotation', 'get', unicode(quotation_row.id)))
                # 报价编辑权限
                identity.provides.add(SectionActionItemNeed('quotation', 'edit', unicode(quotation_row.id)))
                # 报价删除权限
                identity.provides.add(SectionActionItemNeed('quotation', 'del', unicode(quotation_row.id)))
                # 报价打印权限
                identity.provides.add(SectionActionItemNeed('quotation', 'print', unicode(quotation_row.id)))
                # 报价审核权限
                identity.provides.add(SectionActionItemNeed('quotation', 'audit', unicode(quotation_row.id)))

    # 角色 - 库管
    if current_user.role_id == TYPE_ROLE_STOREKEEPER:
        # 赋予整体角色权限
        identity.provides.add(RoleNeed('库管'))
        # 库存-----------------------------------------------------------------------
        # 库存创建
        identity.provides.add(SectionActionNeed('inventory', 'add'))
        # 库存统计
        identity.provides.add(SectionActionNeed('inventory', 'stats'))
        # 仓库-----------------------------------------------------------------------
        # 仓库创建
        identity.provides.add(SectionActionNeed('warehouse', 'add'))
        # 仓库统计
        identity.provides.add(SectionActionNeed('warehouse', 'stats'))
        # 货架-----------------------------------------------------------------------
        # 货架创建
        identity.provides.add(SectionActionNeed('rack', 'add'))
        # 货架统计
        identity.provides.add(SectionActionNeed('rack', 'stats'))


@user_loaded_from_cookie.connect_via(app)
def on_user_loaded_from_cookie(sender, user):
    """
    记住密码后，通过cookie加载用户，需要重新赋予权限，否则权限会丢失
    :param sender:
    :param user:
    :return:
    """
    identity_changed.send(app, identity=Identity(user.id))


@babel.localeselector
def get_locale():
    # if a user is logged in, use the locale from the user settings
    if hasattr(current_user, 'locale') and current_user.locale:
        g.lang = current_user.locale
        g.moment_locale = moment_locale_map.get(current_user.locale)
        return current_user.locale
    # otherwise try to guess the language from the user accept
    # header the browser transmits.  We support de/fr/en in this
    # example.  The best match wins.
    return getattr(g, 'lang', 'en')


@babel.timezoneselector
def get_timezone():
    if hasattr(current_user, 'timezone') and current_user.timezone:
        return current_user.timezone


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
    document_info['TITLE'] = _('management homepage')
    return render_template('index.html', **document_info)


@app.route('/home.html')
@login_required
def home():
    """
    个人中心
    """
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('personal information')
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

    flash(_('Exit Success'), 'success')
    return redirect(url_for('auth.index'))


@app.route('/test_permission_role_administrator/')
@permission_role_administrator.require(http_exception=403)
def test_permission_role_administrator():
    """
    管理员权限测试
    :return:
    """
    return Response('Only if you are admin')


# @app.route('/stream/')
# def stream():
#     """
#     流式响应
#     http://0.0.0.0:8010/stream/
#     :return:
#     """
#     import time
#
#     def gen():
#         for c in 'Hello world!':
#             yield c
#             time.sleep(0.5)
#     return Response(gen())
#
#
# @app.route('/stream_with_context/')
# def stream_with_context():
#     """
#     http://0.0.0.0:8010/stream_with_context/?name=Administrator
#     :return:
#     """
#     import time
#     from flask import stream_with_context, request, Response
#
#     def generate():
#         for i in 'Hello %s!' % (request.args.get('name', '')):
#             time.sleep(0.2)
#             yield i
#     return Response(stream_with_context(generate()))


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
    flash(error.description or _('Not Found'), 'warning')
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


@app.route('/client_info.html')
def client_info():
    """
    客户端信息
    """
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('client information')
    request.headers.get('X-Forwarded-For', request.remote_addr)
    env_info = {
        'x_forwarded_for': request.headers.get('X-Forwarded-For'),
        'x_real_ip': request.headers.get('X-Real-IP'),
        'remote_addr': request.remote_addr,
        'cookies': request.cookies,
    }
    return render_template('client_info.html', env_info=env_info, **document_info)


@app.route('/server_info.html')
def server_info():
    """
    服务端信息
    """
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('server information')
    return render_template('server_info.html', **document_info)
