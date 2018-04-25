#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: test_search_fulltext.py
@time: 2018-04-23 17:30
"""


from __future__ import unicode_literals

import json
from app_backend.clients.client_es import es_client
from app_common.libs.es import ES


es = ES(es_client)


def search_fulltext():
    index = 'catalogue'
    doc_type = 'bearing'
    # field = 'product_label'
    # keywords = '7008 ACD GA/P4A'
    field = 'product_model'
    keywords = '7008ACDGA/P4A'
    query_from = 0
    size = 10

    return es.search_fulltext(index, doc_type, field, keywords, query_from, size)


if __name__ == '__main__':
    res_search_fulltext = search_fulltext()
    print(json.dumps(res_search_fulltext, indent=4, ensure_ascii=False))
