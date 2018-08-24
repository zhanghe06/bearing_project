#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: sync_customer.py
@time: 2018-08-22 17:38
"""


from __future__ import unicode_literals
from __future__ import print_function

from app_backend import app
from app_backend.api.customer import (
    add_customer,
    edit_customer,
)

# 推送上下文
ctx = app.app_context()
ctx.push()


def sync_customer():
    """
    客户同步
    1、客户信息
    2、联系方式
    :return:
    """
    pass


if __name__ == '__main__':
    sync_customer()

