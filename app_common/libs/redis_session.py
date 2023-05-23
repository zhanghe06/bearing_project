#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: redis_session.py
@time: 2018-03-14 17:04
"""


# import pickle
import json
from datetime import timedelta
from uuid import uuid4
from redis import Redis
from werkzeug.datastructures import CallbackDict
from flask.sessions import SessionInterface, SessionMixin


class RedisSession(CallbackDict, SessionMixin):

    def __init__(self, initial=None, sid=None, new=False):
        # def on_update(self):
        #     self.modified = True
        CallbackDict.__init__(self, initial, self.on_update())
        self.sid = sid
        self.new = new
        self.modified = False

    def on_update(self):
        self.modified = True


class RedisSessionInterface(SessionInterface):
    # serializer = pickle
    serializer = json
    session_class = RedisSession

    def __init__(self, redis=None, prefix='session:', **kwargs):
        self.redis = redis or Redis(**kwargs)
        self.prefix = prefix

    @staticmethod
    def generate_sid():
        return str(uuid4())

    @staticmethod
    def get_redis_expiration_time(app, session):
        if session.permanent:
            return app.permanent_session_lifetime
        # return timedelta(days=1)
        return timedelta(minutes=20)

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            sid = self.generate_sid()
            return self.session_class(sid=sid, new=True)
        val = self.redis.get(self.prefix + sid)
        if val is not None:
            data = self.serializer.loads(val)
            return self.session_class(data, sid=sid)
        return self.session_class(sid=sid, new=True)

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        if not session:
            self.redis.delete(self.prefix + session.sid)
            if session.modified:
                response.delete_cookie(app.session_cookie_name,
                                       domain=domain)
            return
        redis_exp = self.get_redis_expiration_time(app, session)
        cookie_exp = self.get_expiration_time(app, session)
        val = self.serializer.dumps(dict(session))
        self.redis.setex(self.prefix + session.sid, int(redis_exp.total_seconds()), val)
        response.set_cookie(app.session_cookie_name, session.sid,
                            expires=cookie_exp, httponly=True,
                            domain=domain)
