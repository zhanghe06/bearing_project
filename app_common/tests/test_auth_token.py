#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: test_auth_token.py
@time: 2019-08-15 11:33
"""

import time
import unittest

from itsdangerous import SignatureExpired, BadSignature

from app_common.libs.auth_token import AuthToken


class AuthTokenTest(unittest.TestCase):
    """
    认证测试
    """

    def setUp(self):
        self.secret_key = '123456'
        self.user_id = 123

    def test_auth_token_success(self):
        auth_token_obj = AuthToken(self.secret_key)
        token = auth_token_obj.create(self.user_id)
        # print(token)
        self.assertIn(
            'eyJ1c2VyX2lkIjoxMjN9',  # 对应 {"user_id":123} 的base64编码
            token
        )
        user = auth_token_obj.verify(token)
        # print(user)
        self.assertEqual(self.user_id, user.get('user_id'))

    def test_auth_token_signature_expired(self):
        auth_token_obj = AuthToken(self.secret_key, 1)
        token = auth_token_obj.create(self.user_id)
        # print(token)
        self.assertIn(
            'eyJ1c2VyX2lkIjoxMjN9',  # 对应 {"user_id":123} 的base64编码
            token
        )
        time.sleep(2)
        self.assertRaises(SignatureExpired, auth_token_obj.verify, token)

    def test_auth_token_bad_signature(self):
        auth_token_obj = AuthToken(self.secret_key, 1)
        token = auth_token_obj.create(self.user_id)
        # print(token)
        self.assertIn(
            'eyJ1c2VyX2lkIjoxMjN9',  # 对应 {"user_id":123} 的base64编码
            token
        )
        time.sleep(2)
        self.assertRaises(BadSignature, auth_token_obj.verify, 'error_token')

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
