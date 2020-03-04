#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: auth_middleware.py
@time: 2020-03-01 19:37
"""


from werkzeug.wrappers import Request, Response, ResponseStream


class AuthMiddleware(object):
    """Auth Middleware"""

    def __init__(self, app):
        self.app = app
        self.username = 'Tony'
        self.password = 'IamIronMan'

    def __call__(self, environ, start_response):
        request = Request(environ)
        username = request.authorization['username']
        password = request.authorization['password']

        # these are hardcoded for demonstration
        # verify the username and password from some database or env config variable
        if username == self.username and password == self.password:
            environ['user'] = {'name': 'Tony'}
            return self.app(environ, start_response)

        res = Response(u'Authorization failed', mimetype='text/plain', status=401)
        return res(environ, start_response)

