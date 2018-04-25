#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: test_es.py
@time: 2018-04-10 21:20
"""


from __future__ import unicode_literals

import unittest
from app_backend.clients.client_es import es_client
from app_common.libs.es import ES


class IndexTest(unittest.TestCase):
    """
    索引测试
    """

    def setUp(self):
        self.es = ES(es_client)
        self.index = 'test_index_01'
        self.doc_type = 'test_doc_type_01'

    def test_index(self):
        """
        测试索引
        :return:
        """

        exists_status = self.es.exists_index(self.index)
        if exists_status:
            res_delete_index = self.es.delete_index(self.index)
            self.assertEqual(
                res_delete_index,
                {u'acknowledged': True}
            )

        res_create_index = self.es.create_index(self.index)
        self.assertEqual(
            res_create_index,
            {u'index': u'test_index_01', u'acknowledged': True, u'shards_acknowledged': True}
        )

        mapping = {
            'properties': {
                'content': {
                    'type': 'text',
                    'analyzer': 'ik_max_word',
                    'search_analyzer': 'ik_max_word'
                }
            }
        }
        res_create_mapping = self.es.create_mapping(self.index, self.doc_type, mapping)
        self.assertEqual(
            res_create_mapping,
            {u'acknowledged': True}
        )

        res_add_index = self.es.add_index(self.index, self.doc_type, {'content': '美国留给伊拉克的是个烂摊子吗'}, 1)
        self.assertEqual(
            res_add_index,
            {u'_type': u'test_doc_type_01', u'_seq_no': 0, u'_shards': {u'successful': 1, u'failed': 0, u'total': 2},
             u'_index': u'test_index_01', u'_version': 1, u'_primary_term': 1, u'result': u'created', u'_id': u'1'}
        )

        res_add_index = self.es.add_index(self.index, self.doc_type, {'content': '公安部：各地校车将享最高路权'}, 2)
        self.assertEqual(
            res_add_index,
            {u'_type': u'test_doc_type_01', u'_seq_no': 0, u'_shards': {u'successful': 1, u'failed': 0, u'total': 2},
             u'_index': u'test_index_01', u'_version': 1, u'_primary_term': 1, u'result': u'created', u'_id': u'2'}
        )

        res_add_index = self.es.add_index(self.index, self.doc_type, {'content': '中韩渔警冲突调查：韩警平均每天扣1艘中国渔船'}, 3)
        self.assertEqual(
            res_add_index,
            {u'_type': u'test_doc_type_01', u'_seq_no': 0, u'_shards': {u'successful': 1, u'failed': 0, u'total': 2},
             u'_index': u'test_index_01', u'_version': 1, u'_primary_term': 1, u'result': u'created', u'_id': u'3'}
        )

        res_add_index = self.es.add_index(self.index, self.doc_type, {'content': '中国驻洛杉矶领事馆遭亚裔男子枪击 嫌犯已自首'}, 4)
        self.assertEqual(
            res_add_index,
            {u'_type': u'test_doc_type_01', u'_seq_no': 1, u'_shards': {u'successful': 1, u'failed': 0, u'total': 2},
             u'_index': u'test_index_01', u'_version': 1, u'_primary_term': 1, u'result': u'created', u'_id': u'4'}
        )

        res_refresh_index = self.es.refresh_index(self.index)
        self.assertEqual(
            res_refresh_index,
            {u'_shards': {u'successful': 5, u'failed': 0, u'total': 10}}
        )

        res_search_fulltext = self.es.search_fulltext(self.index, self.doc_type, 'content', '中国')
        self.assertEqual(
            res_search_fulltext,
            {
                "total": 2,
                "data": [
                    {
                        "value": "中国驻洛杉矶领事馆遭亚裔男子枪击 嫌犯已自首",
                        "label": "<span class=\"text-primary\">中国</span>驻洛杉矶领事馆遭亚裔男子枪击 嫌犯已自首"
                    },
                    {
                        "value": "中韩渔警冲突调查：韩警平均每天扣1艘中国渔船",
                        "label": "中韩渔警冲突调查：韩警平均每天扣1艘<span class=\"text-primary\">中国</span>渔船"
                    }
                ]
            }
        )

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()

