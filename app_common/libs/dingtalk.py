#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: dingtalk.py
@time: 2020-11-04 09:27
"""


import base64
import hashlib
import hmac
import time
import urllib

import requests


class DingTalkClient(object):
    """
    钉钉
    """
    AGENT_ID = ''
    APP_KEY = ''
    APP_SECRET = ''
    ACCESS_TOKEN = ''
    WEB_HOOK = ''
    SECRET = ''
    timestamp = ''
    sign = ''

    def __init__(self, app_key, app_secret, agent_id=''):
        """
        初始化应用
        """
        self.APP_KEY = app_key
        self.APP_SECRET = app_secret
        self.AGENT_ID = agent_id

    def get_token(self):
        url = 'https://oapi.dingtalk.com/gettoken?appkey={app_key}&appsecret={app_secret}'
        url_api = url.format(app_key=self.APP_KEY, app_secret=self.APP_SECRET)
        response = requests.get(url_api)
        res = response.json()
        print(res)
        if not (response.status_code == 200 and not res.get('errcode')):
            print(res.get('errmsg', 'get token error'))
            return
        self.ACCESS_TOKEN = res.get('access_token', '')
        print(self.ACCESS_TOKEN)


class DingTalkRobotClient(object):
    """
    钉钉机器人
    """
    web_hook = ''
    secret = ''
    timestamp = ''
    sign = ''

    def __init__(self, web_hook='', secret=''):
        """
        初始化应用
        """
        self.web_hook = web_hook
        # secret 复制禁用的输入框，避免遗漏
        self.secret = secret

    def _timestamp(self):
        self.timestamp = int(round(time.time() * 1000))

    def _sign(self):
        secret_enc = bytes(self.secret).encode('utf-8')
        string_to_sign = '{}\n{}'.format(self.timestamp, self.secret)
        string_to_sign_enc = bytes(string_to_sign).encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        self.sign = urllib.quote_plus(base64.b64encode(hmac_code))
        print(self.timestamp)
        print(self.sign)

    def msg_structure_text(self, content):
        msg_structure = {
            'msgtype': 'text',
            'text': {
                'content': content
            },
        }
        return msg_structure

    def msg_structure_markdown(self, title, content):
        msg_structure = {
            'msgtype': 'markdown',
            'markdown': {
                'title': title,
                'text': content
            },
        }
        return msg_structure

    def send_msg(self, at_list, title, content, msg_type='text'):
        """
        发送自定义机器人消息
        https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq
        :param at_list:
        :param title:
        :param content:
        :param msg_type:
        :return:
        """
        url = self.web_hook + '&timestamp={timestamp}&sign={sign}'
        self._timestamp()
        self._sign()
        url_api = url.format(timestamp=self.timestamp, sign=self.sign)
        print(url_api)
        data = {
            'at': {
                'atMobiles': at_list
            },
            'isAtAll': False
        }

        if msg_type == 'text':
            data.update(self.msg_structure_text(content=content))
        if msg_type == 'markdown':
            data.update(self.msg_structure_markdown(title=title, content=content))

        response = requests.post(url_api, json=data)
        res = response.json()
        if not (response.status_code == 200 and not res.get('errcode')):
            print(res.get('errmsg', 'send message error'))
            return
        print(res)


if __name__ == '__main__':
    # 钉钉机器人
    dt = DingTalkRobotClient(
        web_hook='https://oapi.dingtalk.com/robot/send?access_token=33c22d6eabed466bb2d493fa6db9fc284bdd468c38cd35f25df6ae54999e1f06',
        secret='SEC415075711917ff907a801a4dd82a0aa444944c2381089529242dd59e8a035827'
    )
    # dt.send_msg(
    #     ['13818732593'],
    #     '文本测试',
    #     '文本测试',
    #     'text',
    # )
    dt.send_msg(
        ['13818732593'],
        'markdown测试',  # 不能为空
        '引用\n> A man who stands for nothing will fall for anything.\n无序列表\n- item1\n- item2',
        'markdown',
    )
