#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: bearing.py
@time: 2020-02-29 23:23
"""


from flask_sqlalchemy import SQLAlchemy

from app_backend import app

db_bearing = SQLAlchemy(app)
