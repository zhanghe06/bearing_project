#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: auto_gen_form.py
@time: 2018-07-18 14:05
"""


from __future__ import unicode_literals
from __future__ import print_function

import argparse
import datetime


from app_common.codes.tpl_form import CODE_TEMPLATE_FORM
from config import current_config

from os.path import join

BASE_DIR = current_config.BASE_DIR


def output_form(**kwargs):
    """
    输出代码
    :param kwargs:
    :return:
    """
    code = (CODE_TEMPLATE_FORM % kwargs).lstrip()
    print(code)
    app = kwargs[b'app']
    section = kwargs[b'section']
    with open(join(BASE_DIR, app, 'forms', '%s.py' % section), b'w') as f:
        f.write(code.encode('utf-8'))


def run():
    parser = argparse.ArgumentParser()
    parser.register('type', 'bool', lambda v: v.lower() in ['true', '1'])
    parser.add_argument(
        '--app',
        type=str,
        default='app_backend',
        help='应用名称',
    )
    parser.add_argument(
        '--section',
        type=str,
        required=True,
        help='模块名称',
    )
    parser.add_argument(
        '--time',
        type=str,
        default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
        help='创建时间',
    )
    parser.add_argument(
        '--model',
        type=str,
        help='模型名称',
    )
    parser.add_argument(
        '--debug',
        type='bool',
        default=True,
        help='调试模式',
    )

    args = parser.parse_args()

    kwargs = args.__dict__
    output_form(**kwargs)


if __name__ == '__main__':
    run()
    # python app_common/codes/auto_gen_form.py --section test --model Test
