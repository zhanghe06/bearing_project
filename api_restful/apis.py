#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: apis.py
@time: 2020-02-28 21:24
"""


from flask_restful import Api

# from app_common.exceptions import errors
from api_restful.blueprints import bp_bearing

# api_bearing = Api(bp_bearing, errors=errors)
api_bearing = Api(bp_bearing)
