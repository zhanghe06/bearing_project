#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: file.py
@time: 2018-04-12 13:03
"""


from os.path import splitext


def get_file_extend_name(file_path):
    """
    获取文件扩展名
    :param file_path:
    :return:
    >>> get_file_extend_name('abc')
    ''
    >>> get_file_extend_name('abc.txt')
    '.txt'
    >>> get_file_extend_name('/root/abc.txt')
    '.txt'
    """
    return splitext(file_path)[1]


def get_file_size(file_obj):
    """
    获取文件大小
    :param file_obj:
    :return:
    """
    file_obj.seek(0, 2)  # Seek to the end of the file
    size = file_obj.tell()  # Get the position of EOF
    file_obj.seek(0)  # Reset the file position to the beginning
    return size


def bytes2human(n):
    """
    可视化字节数
    >>> bytes2human(10000)
    '9.77 KB'
    >>> bytes2human(100001221)
    '95.37 MB'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.2f %sB' % (value, s)
    return '%.2f B' % n
