#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: test_compatibility.py
@time: 2018-04-04 15:04
"""


from __future__ import print_function
from __future__ import unicode_literals

import unittest

from future.moves.urllib.parse import urljoin


class CompatibilityTest(unittest.TestCase):
    """
    兼容测试
    """

    def setUp(self):
        pass

    def test_urljoin(self):
        """
        测试索引
        :return:
        """
        self.assertEqual(
            urljoin('http://www.baidu.com/a', 'b'),
            'http://www.baidu.com/b'
        )
        self.assertEqual(
            urljoin('http://www.baidu.com/a/', 'b'),
            'http://www.baidu.com/a/b'
        )
        self.assertEqual(
            urljoin('http://www.baidu.com/a/', '/b'),
            'http://www.baidu.com/b'
        )

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
