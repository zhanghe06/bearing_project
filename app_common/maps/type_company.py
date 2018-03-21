#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: type_company.py
@time: 2018-03-19 00:02
"""

from __future__ import unicode_literals

# 认证类型（0:未知,1:中间商2:终端）
TYPE_COMPANY_DEFAULT = 0
TYPE_COMPANY_MIDDLEMAN = 1
TYPE_COMPANY_END_USER = 2

TYPE_COMPANY_DICT = {
    0: '未知',
    1: '中间商',
    2: '终端用户',
}
