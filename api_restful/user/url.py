#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: url.py
@time: 2020-02-28 21:27
"""


from api_restful.apis import api_bearing
from api_restful.user.resource import (
    UserResource,
    UsersResource,
)

# 详情、修改、删除
api_bearing.add_resource(
    UserResource,
    '/user/<int:pk>',
    endpoint='user',
    strict_slashes=False
)

# 创建、列表
api_bearing.add_resource(
    UsersResource,
    '/user',
    endpoint='users',
    strict_slashes=False
)
