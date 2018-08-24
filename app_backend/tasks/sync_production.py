#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: sync_production.py
@time: 2018-08-22 17:39
"""


from __future__ import unicode_literals
from __future__ import print_function

from app_backend import app
from app_backend.api.production import (
    add_production,
    edit_production,
)

# 推送上下文
ctx = app.app_context()
ctx.push()


def sync_production():
    """
    产品同步
    1、产品信息
    2、品牌信息
    :return:
    """
    pass


if __name__ == '__main__':
    sync_production()
