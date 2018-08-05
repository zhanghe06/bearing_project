#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: login.py
@time: 2018-03-06 00:18
"""

from app_backend.models.bearing_project import User
from flask_login import UserMixin


class LoginUser(User, UserMixin):
    """
    用户登录类
    """
