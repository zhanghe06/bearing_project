#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: email.py
@time: 2018-12-25 18:22
"""


from flask_mail import Mail, Message


class MailClient(object):
    """
    邮件
        用 python 快速开启一个 SMTP 服务
        $ python -m smtpd -n -c DebuggingServer localhost:1025
        假如想让程序运行于标准的 25 的端口上的话，必须使用 sudo 命令，因为只有 root 才能在 1-1024 端口上开启服务
        $ sudo python -m smtpd -n -c DebuggingServer localhost:25
    """
    def __init__(self, mail, sender=None):
        self.mail = mail  # type: Mail
        self.sender = sender

    def send_text_email(self, subject, recipients, body):
        """
        发送邮件
        :param subject:
        :param recipients:
        :param body:
        :return:
        """
        msg = Message(subject, sender=self.sender, recipients=recipients)
        msg.body = body
        self.mail.send(msg)

    def send_html_email(self, subject, recipients, body):
        """
        发送邮件
        :param subject:
        :param recipients:
        :param body:
        :return:
        """
        msg = Message(subject, sender=self.sender, recipients=recipients)
        msg.html = body
        self.mail.send(msg)

