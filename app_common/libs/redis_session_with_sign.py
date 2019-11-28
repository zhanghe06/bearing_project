#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: redis_session_with_sign.py
@time: 2018-04-04 22:44
"""


# import pickle
import json
from datetime import timedelta
from uuid import uuid4
from redis import Redis
from werkzeug.datastructures import CallbackDict
from flask.sessions import SessionInterface, SessionMixin
from itsdangerous import TimestampSigner, SignatureExpired, BadTimeSignature


class RedisSession(CallbackDict, SessionMixin):

    def __init__(self, initial=None, sid=None, new=False):
        def on_update(self):
            self.modified = True
        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.new = new
        self.modified = False


class RedisSessionInterface(SessionInterface):
    # serializer = pickle
    serializer = json
    session_class = RedisSession

    def __init__(self, redis=None, prefix='session:', **kwargs):
        self.redis = redis or Redis(**kwargs)
        self.prefix = prefix

    @staticmethod
    def _sign(app, session_id):
        """
        签名 session_id
        :param app:
        :param session_id: 通常是uuid
        :return:
        """
        s = TimestampSigner(app.secret_key)
        return s.sign(session_id)

    @staticmethod
    def _un_sign(app, sign_session_id):
        """
        校验签名 session_id
        :param app:
        :param sign_session_id:
        :return:
        """
        s = TimestampSigner(app.secret_key)
        try:
            session_id = s.unsign(sign_session_id, max_age=app.permanent_session_lifetime.total_seconds())
            return session_id
        except SignatureExpired as e:
            # 处理签名超时
            raise Exception(e.message)
        except BadTimeSignature as e:
            # 处理签名错误
            raise Exception(e.message)

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
        sid_c = request.cookies.get(app.session_cookie_name)

        if not sid_c:
            sid_s = self.generate_sid()
            return self.session_class(sid=sid_s, new=True)
        else:
            try:
                sid_s = self._un_sign(app, sid_c)
            except:
                # TODO log
                sid_s = self.generate_sid()

        val = self.redis.get(self.prefix + sid_s)
        if val is not None:
            data = self.serializer.loads(val)
            return self.session_class(data, sid=sid_s)
        return self.session_class(sid=sid_s, new=True)

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        sid_s = session.sid
        if not session:
            self.redis.delete(self.prefix + sid_s)
            if session.modified:
                response.delete_cookie(app.session_cookie_name,
                                       domain=domain)
            return
        redis_exp = self.get_redis_expiration_time(app, session)
        cookie_exp = self.get_expiration_time(app, session)
        val = self.serializer.dumps(dict(session))
        self.redis.setex(self.prefix + sid_s, int(redis_exp.total_seconds()), val)
        sid_c = self._sign(app, sid_s)
        response.set_cookie(app.session_cookie_name, sid_c,
                            expires=cookie_exp, httponly=True,
                            domain=domain)
