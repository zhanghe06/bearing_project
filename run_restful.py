#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: run_backend.py
@time: 2018-03-05 23:49
"""


from api_restful import app


if __name__ == '__main__':
    app.run(
        host=app.config['HOST'],
        debug=app.config['DEBUG'],
        port=8000,  # 端口号必须为整型
    )
