#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: bearing.py
@time: 2020-02-28 21:40
"""


from flask_sqlalchemy import SQLAlchemy

from api_restful import app

db_bearing = SQLAlchemy(app)
