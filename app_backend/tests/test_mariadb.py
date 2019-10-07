#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: test_mariadb.py
@time: 2019-10-05 20:47
"""

import time
from app_backend.api.customer import get_customer_rows, count_customer
from sqlalchemy.exc import OperationalError


conn_err_list = [
    '(_mysql_exceptions.OperationalError) (1927, ',  # Connection was killed
    '(_mysql_exceptions.OperationalError) (2006, ',  # MySQL server has gone away
    '(_mysql_exceptions.OperationalError) (2013, ',  # Lost connection to MySQL server during query
]


def run():
    try:
        cs = get_customer_rows()
        for c in cs:
            print(c.id, count_customer())  # 关键，同一连接多次数据操作，
            time.sleep(2)
    except OperationalError as e:
        for conn_e in conn_err_list:
            if conn_e in e.message:
                print('数据库连接错误')
                return
        print('其他错误')


if __name__ == '__main__':
    run()
