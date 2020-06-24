#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: test_email.py
@time: 2018-12-25 23:59
"""

from flask import render_template

from app_backend import app, mail
from app_common.libs.mail import MailClient


ctx = app.app_context()
ctx.push()


def test_send_email_text():
    mail_client = MailClient(mail)
    mail_client.send_text_email("this is a test subject", ["zhang_he06@163.com"], "this is a test content")


def test_send_email_html():
    mail_client = MailClient(mail)
    mail_client.send_html_email(
        "bug information",
        ["zhang_he06@163.com"],
        render_template('email.html', message='bug content')
    )


if __name__ == '__main__':
    test_send_email_text()
    test_send_email_html()
