#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: signals.py
@time: 2018-04-14 02:02
"""


from blinker import Namespace


from app_backend import app


_signal = Namespace()


signal_quote_auth = _signal.signal('signal_quote_auth')  # 报价审核


@signal_quote_auth.connect_via(app)
def quote_auth(sender, **extra):
    """
    信号处理 - 报价审核
        发送信号：signal_quote_auth.send(app, **{'a': 1, 'b': 2})
        触发条件：报价审核
        处理逻辑：通知对应销售人员
    :param sender:
    :param extra:
    :return:
    """
    print(sender, extra)


def test_send():
    signal_quote_auth.send(app, **{'a': 1, 'b': 2})


if __name__ == '__main__':
    test_send()
