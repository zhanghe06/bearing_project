#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: import_es_quotation.py
@time: 2018-08-01 10:02
"""


from __future__ import unicode_literals
from __future__ import print_function

from app_backend import app
from app_backend.api.production import get_production_limit_rows_by_last_id
from app_backend.clients.client_es import es_client
from app_common.libs.es import ES

# 推送上下文
ctx = app.app_context()
ctx.push()

es = ES(es_client)


def import_production():
    pk_id = 0
    limit = 200
    import_count = 0

    index = 'production'
    doc_type = 'bearing'
    mapping = {
        'properties': {
            'id': {
                'type': 'integer',
            },
            'category_id': {
                'type': 'integer',
            },
            'production_brand': {
                'type': 'text',
                'analyzer': 'ik_max_word',
            },
            'production_model': {
                'type': 'text',
                'analyzer': 'ik_max_word',
            },
            'production_sku': {
                'type': 'text',
            },
        }
    }

    if es.exists_index(index):
        es.delete_index(index)
    es.create_index(index)
    es.create_mapping(index, doc_type, mapping)
    while 1:
        rows = get_production_limit_rows_by_last_id(pk_id, limit)
        if not rows:
            break
        for row in rows:
            import_count += 1
            pk_id = row.id

            body = {
                'id': row.id,
                'category_id': row.category_id,
                'production_brand': row.production_brand,
                'production_model': row.production_model,
                'production_sku': row.production_sku,
            }
            es.add_index(index, doc_type, body, row.id)
        print('import count: %s' % import_count)


if __name__ == '__main__':
    import_production()
