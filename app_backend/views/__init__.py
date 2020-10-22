#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: __init__.py
@time: 2018-03-06 00:18
"""

from __future__ import unicode_literals

import time
from collections import defaultdict
from uuid import uuid4
import logging
import user_agents
from flask import Response
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
from flask import send_from_directory
from flask_babel import gettext as _
from flask_login import (
    login_user,
    logout_user,
    current_user,
    login_required,
    user_loaded_from_cookie
)
from flask_principal import (
    identity_changed,
    Identity,
    AnonymousIdentity,
    identity_loaded,
    UserNeed)
from flask_wtf.csrf import CSRFError
from itsdangerous import SignatureExpired, BadTimeSignature

from app_backend import app, login_manager, babel
from app_backend.api.customer import get_customer_latest
from app_backend.api.login_user import get_login_user_row_by_id
from app_backend.api.quotation import get_quotation_latest
from app_backend.api.sales_order import get_sales_order_latest
from app_backend.identities import identity_role_administrator, identity_role_sales, identity_role_purchaser, \
    identity_role_manager, identity_role_stock_keeper, identity_role_accountant
from app_backend.models.model_bearing import Customer, Quotation, SalesOrder
from app_backend.permissions import (
    permission_role_administrator)
from app_common.libs.auth_token import AuthToken
from app_common.maps.status_delete import STATUS_DEL_NO
from app_common.maps.type_role import (
    TYPE_ROLE_SALES,
    TYPE_ROLE_PURCHASER,
    TYPE_ROLE_MANAGER,
    TYPE_ROLE_SYSTEM,
    TYPE_ROLE_STOREKEEPER,
    TYPE_ROLE_ACCOUNTANT)

app_logger = logging.getLogger('app')
debug_logger = logging.getLogger('debug')

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
    request_id = request.headers.get('X-Request-Id', str(uuid4()))  # 不带短横: uuid4().get_hex()
    g.request_id = request_id
    debug_logger.debug('before_request')

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

    g.STATIC_RES_VER = app.config.get('STATIC_RES_VER', '1.0')  # 静态资源版本

#
# @app.errorhandler(Exception)
# def unhandled_exception(e):
#     debug_logger.debug('after_request')
#     # return render_template('generic.html'), 500
#     return 'Exception', 500


@app.after_request
def after_request(response):
    request_id = g.get('request_id', str(uuid4()))
    g.request_id = request_id
    debug_logger.debug('after_request')

    # 头部注入
    response.headers.add('X-Request-Id', request_id)

    return response  # 必须返回response


@app.teardown_request
def teardown_request(exception=None):
    request_id = g.get('request_id', str(uuid4()))
    g.request_id = request_id
    debug_logger.debug('teardown_request')

    g.project = app.name

    # 接口日志
    g.app_log = defaultdict(lambda: '-')
    # g.app_log['project_name'] = app.name

    if exception:
        exception_info = {
            'module': exception.__class__.__module__,
            'name': exception.__class__.__name__,
            'message': exception.message,
        }
        g.app_log['exception'] = '%(module)s.%(name)s: %(message)s' % exception_info
        app_logger.error(dict(g.app_log))
    else:
        app_logger.info(dict(g.app_log))
    return exception


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

    # 角色 - 系统
    if current_user.role_id == TYPE_ROLE_SYSTEM:
        identity_role_administrator.setup(identity)

    # 角色 - 销售
    if current_user.role_id == TYPE_ROLE_SALES:
        identity_role_sales.setup(identity)

    # 角色 - 采购
    if current_user.role_id == TYPE_ROLE_PURCHASER:
        identity_role_purchaser.setup(identity)

    # 角色 - 经理
    if current_user.role_id == TYPE_ROLE_MANAGER:
        identity_role_manager.setup(identity)

    # 角色 - 库管
    if current_user.role_id == TYPE_ROLE_STOREKEEPER:
        identity_role_stock_keeper.setup(identity)

    # 角色 - 财务
    if current_user.role_id == TYPE_ROLE_ACCOUNTANT:
        identity_role_accountant.setup(identity)


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


@app.route('/s')
def sign():
    """
    认证
    """
    auth_token = request.args.get('auth_token')
    if not auth_token:
        return redirect(url_for('auth.index'))
    try:
        auth_token_obj = AuthToken(app.secret_key)
        data = auth_token_obj.verify(auth_token)
        user_id = data.get('user_id')
        # 认证成功
        # 用户登录
        login_user(get_login_user_row_by_id(user_id))

        # 加载权限信号通知(Tell Flask-Principal the identity changed)
        identity_changed.send(app, identity=Identity(user_id))

        flash(_('Auth Success'), 'success')
        return redirect(url_for('index'))
    except SignatureExpired as e:
        # 处理签名超时
        flash(_('Signature Expired'), 'danger')
        return redirect(url_for('auth.index'))
    except BadTimeSignature as e:
        # 处理签名错误
        flash(_('Signature Error'), 'danger')
        return redirect(url_for('auth.index'))
    except Exception as e:
        # 其它异常
        flash(_('Signature Error'), 'danger')
        return redirect(url_for('auth.index'))


@app.route('/')
@app.route('/index.html')
@login_required
def index():
    """
    后台首页
    """
    # ERROR > WARNING > INFO > DEBUG
    debug_logger.debug('api debug')
    debug_logger.info('api info')
    debug_logger.warning('api warning')
    debug_logger.error('api error')
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

    latest_customer = get_customer_latest(
        Customer.owner_uid == current_user.id,
        Customer.status_delete == STATUS_DEL_NO
    )

    latest_quotation = get_quotation_latest(
        Quotation.uid == current_user.id,
        Quotation.status_delete == STATUS_DEL_NO
    )

    latest_transaction = get_sales_order_latest(
        SalesOrder.uid == current_user.id,
        SalesOrder.status_delete == STATUS_DEL_NO
    )

    return render_template(
        'home.html',
        latest_customer=latest_customer,
        latest_quotation=latest_quotation,
        latest_transaction=latest_transaction,
        **document_info
    )


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


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    if request.is_xhr:
        return jsonify({'result': False, 'msg': e.description}), 400
    else:
        return redirect(request.args.get('next') or url_for('index'))


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


@app.errorhandler(423)
def locked_requests(error):
    flash(getattr(error, 'description', None) or getattr(error, 'message', None) or _('Locked'), 'warning')
    return render_template('http_exception/423.html'), 423


@app.errorhandler(429)
def too_many_requests(error):
    flash(_('Too Many Requests'), 'warning')
    return render_template('http_exception/429.html'), 429


@app.errorhandler(500)
def internal_server_error(error):
    # 提取原始异常
    error = getattr(error, 'original_exception', error)

    message = getattr(error, 'description', None) or getattr(error, 'message', None) or _('Internal Server Error')

    # Redis 连接失败
    from redis import ConnectionError
    # MariaDB 连接失败
    from sqlalchemy.exc import OperationalError

    if isinstance(error, ConnectionError):
        # 因为本项目session依赖redis，所以redis连接失败，异常处理不能用render_template，其间有操作session会报错
        message = '缓存连接失败'

    if isinstance(error, OperationalError):
        message = '数据连接失败'

    # 依赖组件连接失败，整体服务失效
    if request.is_xhr or isinstance(error, (ConnectionError, OperationalError)):
        return jsonify({'error': message}), 500

    # flash(message, 'warning')
    return render_template(
        'http_exception/500.html',
        message=message,
    ), 500


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
