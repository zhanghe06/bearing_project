#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: sms_ry.py
@time: 2018-11-21 14:06
"""

import json
import threading
import time

import requests
from future.moves.urllib.parse import urlencode

# dc 数据类型
DATA_CODING = 15  # dc定义成15能符合大部分编码
# rf 响应格式
RESPONSE_FORMAT = 2  # rf 返回JSON格式数据
# rd 是否需要状态报告
REPORT_DATA = 1  # rd 需要状态报告
# tf 短信内容的传输编码
TRANSFER_CODING = 3  # tf URLEncoder-utf8编码
# url 接口地址
URL = 'http://server:7891/mt'
# headers 请求头
HEADER = {
    "accept": "*/*",
    "connection": "Keep-Alive",
    "user-agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;SV1)"
}
TIME_OUT = (30, 30)

USER_NAME = '用户名'
PASS_WORD = '密码'
PHONE_ID = '测试手机号'

# 取上行信息与状态报告 的定时器
# timer = None

# 每次获取的最大量 可自定义
fs = 50
# 接收状态报告和上行信息方法
mo = "mo"


# 发送单一内容
def send_single_sms():
    content = '【测试】这是一条测试短信aaa123'
    param_map = {
        'un': USER_NAME,
        'pw': PASS_WORD,
        'da': PHONE_ID,
        'dc': DATA_CODING,
        'rf': RESPONSE_FORMAT,
        'rd': REPORT_DATA,
        'tf': TRANSFER_CODING,
        'ex': 1493,
        'sm': content
    }

    result = requests.post(url=URL, data=urlencode(param_map).encode('utf-8'), headers=HEADER, timeout=TIME_OUT)
    return json.loads(result.text)


# 单一内容短信群发与不同短信不同内容群发
def send_group_sms():
    mobiles = ['测试手机号', '测试手机号']
    contents = ['【测试1】这是一条测试短信aaa123', '【测试2】这是一条测试短信aaa123']
    content = ''.join([item + '#' + contents[count] + '|' for count, item in enumerate(mobiles)])[:-1]

    param_map = {
        'un': USER_NAME,
        'pw': PASS_WORD,
        'da': '',
        'dc': DATA_CODING,
        'rf': RESPONSE_FORMAT,
        'rd': REPORT_DATA,
        'tf': TRANSFER_CODING,
        'ex': 1493,
        'sm': content
    }

    result = requests.post(url=URL, data=param_map, headers=HEADER, timeout=TIME_OUT)
    return json.loads(result.text)


# 取上行信息与状态报告
def get_mo():
    global fs
    global mo

    # 数据封装
    param_map = {
        "fs": fs,
        "un": USER_NAME,
        "pw": PASS_WORD,
        'dc': DATA_CODING,
        'rf': RESPONSE_FORMAT,
        'rd': REPORT_DATA,
        'tf': TRANSFER_CODING
    }

    # 给fs一个基准 再取数据多少时用哪种方式 量少可以让线程休眠然后加大其他线程效率
    if fs < 50:
        get_s_data(param_map)
    else:
        get_l_data(param_map)


def get_l_data(param_map):
    result = json.loads(requests.post(url=URL, data=param_map, headers=HEADER, timeout=TIME_OUT).text)
    json_array = result.get('data', '')
    if json_array is not None:
        # 进行需要的操作
        print(json_array)
    try:
        if len(json_array) < fs:
            if len(json_array) == 0:
                time.sleep(1)
                timer = threading.Timer(1, get_l_data, [param_map])
                timer.start()
            else:
                # 数据操作
                data_operation(json_array)
                time.sleep(1)
                # 循环获取
                timer = threading.Timer(1, get_l_data, [param_map])
                timer.start()
        else:
            data_operation(json_array)
            timer = threading.Timer(1, get_l_data, [param_map])
            timer.start()
    except Exception as e:
        print('error3: %s' % e)


def get_s_data(param_map):
    result = json.loads(requests.post(url=URL, data=param_map, headers=HEADER, timeout=TIME_OUT).text)
    json_array = result.get('data', '')
    if json_array is not None:
        # 将获取到的数据进行自己需要的操作
        print(json_array)
    try:
        if len(json_array) < 1:
            time.sleep(1)
            timer = threading.Timer(1, get_s_data, [param_map])
            timer.start()

        data_operation(json_array)
        # 可根据实际情况定义线程休眠时长
        time.sleep(1)
        timer = threading.Timer(1, get_s_data, [param_map])
        timer.start()
    except Exception as e:
        print('error4: %s' % e)


def data_operation(json_array):
    for i in json_array:
        op = i['op']
        if op is "dr":
            # 将获取到的数据进行自己需要的操作
            print(i)
        else:
            smdata = i['sm']
            data = bytearray.fromhex(smdata)
            sm = decode_message(int(i['dc']), data)
            # 将获取到的数据进行自己需要的操作
            print(sm)
            print(i)


def decode_message(dc, data):
    try:
        if not data:
            return ''
        elif dc is 8:
            return data.decode('UTF-16BE')
        elif dc is 0:
            return data.decode('Ascii')
        elif dc is 15:
            return data.decode('GBK')
        else:
            return ''
    except Exception as e:
        print('error5: %s' % e)


def main():
    try:
        res = send_group_sms()  # send_group_sms() 自行调用
        if res['success'] is True:
            print('success')
            # get_mo()
        else:
            print('error1: %s' % res['r'])
    except Exception as e:
        print('error2: %s' % e)


if __name__ == '__main__':
    main()
