#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: example.py
@time: 2020-03-02 00:54
"""


from socket import *

remote_host = '192.168.4.1'
remote_port = 5160

conn = socket(AF_INET, SOCK_STREAM)
# conn = socket(AF_INET, SOCK_DGRAM)
conn.connect((remote_host, remote_port))
conn.send('client msg: 123456')
conn.close()
