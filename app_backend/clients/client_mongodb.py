#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: client_mongodb.py
@time: 2019-03-30 10:06
"""

from __future__ import unicode_literals

from pymongo import MongoClient, errors

from config import current_config

MONGODB = current_config.MONGO

try:
    mongodb_client = MongoClient(MONGODB.MONGO_URL)
except errors.ServerSelectionTimeoutError as e:
    print('Mongodb 连接超时: %s' % e)
    raise e
except Exception as e:
    print('Mongodb 连接异常: %s' % e)
    raise e
