#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: gen.py
@time: 2018-03-14 17:19
"""


from __future__ import print_function
from __future__ import unicode_literals

import os
import sys

from config import current_config


BASE_DIR = current_config.BASE_DIR
SQLALCHEMY_DATABASE_URI = current_config.SQLALCHEMY_DATABASE_URI


def gen_models(app_name):
    """
    创建 models
    $ python gen.py gen_models
    :param app_name:
    :return:
    """
    file_path = os.path.join(BASE_DIR, '%s/models/bearing_project.py' % app_name)
    cmd = 'sqlacodegen %s --noinflect --outfile %s' % (SQLALCHEMY_DATABASE_URI, file_path)

    output = os.popen(cmd)
    result = output.read()
    print(result)

    # 更新 model 文件
    with open(file_path, b'r') as f:
        lines = f.readlines()
    # 替换 model 关键内容
    lines[2] = b'from %s import db\n' % app_name
    lines[5] = b'Base = db.Model\n'

    # 新增 model 转 dict 方法
    with open(file_path, b'w') as f:
        lines.insert(9, b'def to_dict(self):\n')
        lines.insert(10, b'    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}\n')
        lines.insert(11, b'\n')
        lines.insert(12, b'Base.to_dict = to_dict\n')
        lines.insert(13, b'\n\n')
        f.write(b''.join(lines))


def run():
    """
    入口
    """
    # print sys.argv
    try:
        if len(sys.argv) > 2:
            fun_name = globals()[sys.argv[1]]
            fun_name(sys.argv[2])
        else:
            print('缺失参数\n')
            usage()
    except NameError as e:
        print(e)
        print('未定义的方法[%s]' % sys.argv[1])


def usage():
    print('''
创建/更新 models
$ python gen.py gen_models app_frontend
$ python gen.py gen_models app_backend
''')


if __name__ == '__main__':
    run()
    # print BASE_DIR
    # print SQLALCHEMY_DATABASE_URI
