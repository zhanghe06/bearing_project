#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: socket_io.py
@time: 2018-04-13 23:32
"""

from __future__ import unicode_literals
from flask import Blueprint
from flask import render_template
from flask_socketio import send, emit
from copy import copy
from datetime import datetime
from flask_babel import gettext as _
from flask_login import (
    user_logged_in,
    user_logged_out,
    user_loaded_from_cookie,
)

from app_backend import app, socketio

# 定义蓝图
bp_socket_io = Blueprint('socket_io', __name__, url_prefix='/socket_io')

SOCKET_IO_NAMESPACE = '/msg'

SOCKET_IO_INFO = {
    'title': '',
    'info': '',
    'time': '',
}


@socketio.on('event_audit', namespace=SOCKET_IO_NAMESPACE)
def audit_message(message):
    emit('s_res', {'data': message['data']})


@socketio.on('broadcast_event_login', namespace=SOCKET_IO_NAMESPACE)
def login_message(message):
    emit('s_res', {'data': message['data']}, broadcast=True)


@socketio.on('broadcast_event_logout', namespace=SOCKET_IO_NAMESPACE)
def logout_message(message):
    emit('s_res', {'data': message['data']}, broadcast=True)


@socketio.on('connect', namespace=SOCKET_IO_NAMESPACE)
def connect():
    # emit('s_res', {'data': 'Connected'})
    pass


@socketio.on('disconnect', namespace=SOCKET_IO_NAMESPACE)
def disconnect():
    # print('Client disconnected')
    pass


@socketio.on('user_logged_in')
@user_logged_in.connect_via(app)
def on_user_logged_in(sender, user):
    """
    用户登录 广播通知
    :param sender:
    :param user:
    :return:
    """
    if not hasattr(user, 'name'):
        return
    socket_io_info = SOCKET_IO_INFO.copy()
    socket_io_info['title'] = _('User logged in')
    socket_io_info['info'] = _('User [%(user_name)s] has logged in', user_name=user.name)
    # socket_io_info['time'] = datetime.utcnow().strftime('%H:%M')
    socket_io_info['time'] = datetime.utcnow()
    emit(
        's_res',
        render_template('_msg.html', **socket_io_info),
        # socket_io_info,
        namespace=SOCKET_IO_NAMESPACE,
        broadcast=True
    )


@user_loaded_from_cookie.connect_via(app)
@socketio.on('user_loaded_from_cookie')
def on_user_loaded_from_cookie(sender, user):
    """
    用户登录 广播通知
    :param sender:
    :param user:
    :return:
    """
    if not hasattr(user, 'name'):
        return
    socket_io_info = SOCKET_IO_INFO.copy()
    socket_io_info['title'] = _('User logged in')
    socket_io_info['info'] = _('User [%(user_name)s] has logged in', user_name=user.name)
    socket_io_info['time'] = datetime.utcnow()
    emit(
        's_res',
        render_template('_msg.html', **socket_io_info),
        # socket_io_info,
        namespace=SOCKET_IO_NAMESPACE,
        broadcast=True
    )


@user_logged_out.connect_via(app)
@socketio.on('user_logged_out')
def on_user_logged_out(sender, user):
    """
    用户退出 广播通知
    :param sender:
    :param user:
    :return:
    """
    if not hasattr(user, 'name'):
        return
    socket_io_info = SOCKET_IO_INFO.copy()
    socket_io_info['title'] = _('User logged out')
    socket_io_info['info'] = _('User [%(user_name)s] has logged out', user_name=user.name)
    socket_io_info['time'] = datetime.utcnow()
    emit(
        's_res',
        render_template('_msg.html', **socket_io_info),
        # socket_io_info,
        namespace=SOCKET_IO_NAMESPACE,
        broadcast=True
    )
