#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: run_frontend.py
@time: 2018-03-05 23:49
"""


from app_frontend import app


if __name__ == '__main__':
    app.debug = app.config['DEBUG']  # 调试模式, DEBUG = True
    app.run(host='0.0.0.0', port=8050)  # 端口号必须为整型

