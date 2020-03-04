#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: __init__.py
@time: 2018-03-05 15:02
"""

from __future__ import print_function
from __future__ import unicode_literals

import os
from importlib import import_module

MODE = os.environ.get('MODE') or 'default'
current_config = import_module('config.%s' % MODE)
try:
    current_config = import_module('config.%s' % MODE)
    print('[√] 当前环境变量: %s' % MODE)
except ImportError:
    print('[!] 配置错误，请初始化环境变量')
    print('source env_develop.sh  # 开发环境')
    print('source env_product.sh  # 生产环境')
