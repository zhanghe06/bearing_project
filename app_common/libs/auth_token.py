#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: auth_token.py
@time: 2018-06-21 10:52
"""

from datetime import timedelta

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class AuthToken(object):
    """
    认证
    """

    def __init__(self, secret_key, secret_ttl=None):
        self.secret_key = secret_key
        if isinstance(secret_ttl, timedelta):
            self.secret_ttl = secret_ttl.total_seconds()
        else:
            self.secret_ttl = secret_ttl

    def create(self, user_id):
        s = Serializer(self.secret_key, expires_in=self.secret_ttl)
        return s.dumps({'user_id': user_id})

    def verify(self, token):
        s = Serializer(self.secret_key)
        data = s.loads(token)
        return data
