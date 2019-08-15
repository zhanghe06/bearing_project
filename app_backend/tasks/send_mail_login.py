#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: send_mail_login.py
@time: 2019-07-29 23:46
"""

from __future__ import print_function
from __future__ import unicode_literals

import json

from flask import render_template

from app_backend import app, mail
from app_backend.clients.client_redis import redis_client
from app_common.decorators.exception import ignore_exception
from app_common.libs.email import MailClient
from app_common.libs.redis_pub_sub import RedisPubSub

ctx = app.app_context()
ctx.push()

prefix_key = 'email_login'

redis_pub_sub_obj = RedisPubSub('email_login', redis_client=redis_client)


def pub(email, message):
    key = ':'.join([prefix_key, email])
    ex = app.config.get('PERMANENT_SESSION_LIFETIME')
    # SET 'email_login:zhang_he06@163.com' '{"name": "空ping子", "email": "zhang_he06@163.com", "link": "http://www.baidu.com"}' EX 60 NX
    result = redis_client.set(key, message, ex=ex, nx=True)
    if not result:
        return False
    redis_pub_sub_obj.pub('email', message)
    return True


def sub():
    for message in redis_pub_sub_obj.sub('email'):
        # print(message)
        send_email_login(message)


@ignore_exception
def send_email_login(message):
    data = json.loads(message)
    name = data.get('name')
    email = data.get('email')
    link = data.get('link')
    if not (name and email and link):
        return
    template_name = 'email/email_login.html'
    mail_client = MailClient(mail)
    mail_client.send_html_email(
        # _('Sign in with email'),
        "邮箱登录",
        [email],
        render_template(
            template_name,
            name=name,
            link=link,
        )
    )


if __name__ == '__main__':
    sub()
