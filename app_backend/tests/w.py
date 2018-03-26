#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: w.py
@time: 2018-03-23 15:23
"""


import json

from app_backend import app
from app_backend.api.user import get_user_row_by_id
from app_common.maps.type_auth import TYPE_AUTH_DICT
from app_common.maps.type_company import TYPE_COMPANY_DICT
from app_common.maps.type_role import TYPE_ROLE_DICT
from app_backend.clients.client_redis import redis_client



session_keys = redis_client.keys('%s*' % app.config['REDIS_SESSION_PREFIX_BACKEND'])
if not session_keys:
    print(False)
print [json.loads(s_k).get('user_id') for s_k in redis_client.mget(session_keys)]

# user_ids = map(lambda x: int(x) if x else 0,
#                [json.loads(s_k).get('user_id') for s_k in redis_client.mget(session_keys)])
# return redis_client.delete(dict(zip(user_ids, session_keys)).get(user_id))
