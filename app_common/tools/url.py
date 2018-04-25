#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: url.py
@time: 2018-04-20 18:42
"""


from flask import request, url_for, redirect

from future.moves.urllib.parse import urlparse, urljoin


def is_safe_url(target):
    """
    是否安全链接
    参考:
        http://flask.pocoo.org/snippets/62/
        http://flask.pocoo.org/snippets/63/
    :param target:
    :return:
    """
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def get_redirect_target():
    """
    获取跳转目标
    :return:
    """
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target


def redirect_back(endpoint='index', **values):
    """
    跳转（优先next, 其次endpoint）
    :param endpoint:
    :param values:
    :return:
    """
    target = request.args.get('next')
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)
