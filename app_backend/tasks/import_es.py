#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: import_es.py
@time: 2018-04-16 22:23
"""

from __future__ import unicode_literals

from app_backend import app
from app_backend.api.catalogue import get_catalogue_limit_rows_by_last_id
from app_backend.clients.client_es import es_client
from app_common.libs.es import ES

# 推送上下文
ctx = app.app_context()
ctx.push()

es = ES(es_client)


def import_catalogue():
    pk_id = 0
    limit = 200
    import_count = 0

    index = 'catalogue'
    doc_type = 'skf'
    mapping = {
        'properties': {
            'product_brand': {
                'type': 'text',
                'analyzer': 'ik_max_word',
            },
            'product_model': {
                'type': 'text',
                'analyzer': 'ik_max_word',
            },
            'product_label': {
                'type': 'text',
                'analyzer': 'ik_max_word',
            },
            'product_brand_old': {
                'type': 'text',
                'analyzer': 'ik_max_word',
            },
            'product_model_old': {
                'type': 'text',
                'analyzer': 'ik_max_word',
            },
            'product_class': {
                'type': 'text',
                'analyzer': 'ik_max_word',
            },
            'ind': {
                'type': 'integer',
            },
            'oud': {
                'type': 'integer',
            },
            'wid': {
                'type': 'integer',
            },
            'speed_g': {
                'type': 'integer',
            },
            'speed_o': {
                'type': 'integer',
            },
            'weight': {
                'type': 'scaled_float',
                'scaling_factor': 1000
            },
            'serie': {
                'type': 'text',
            },
            'accuracy': {
                'type': 'text',
            },
            'preload': {
                'type': 'text',
            },
            'seal': {
                'type': 'text',
            },
            'angle': {
                'type': 'text',
            },
            'r_size': {
                'type': 'text',
            },
            'r_matel': {
                'type': 'text',
            },
            'assembly_no': {
                'type': 'text',
            },
            'assembly_type': {
                'type': 'text',
            },
            'note': {
                'type': 'text',
            },
            'tag': {
                'type': 'keyword',
            },
        }
    }

    es.create_index(index)
    es.create_mapping(index, doc_type, mapping)
    while 1:
        rows = get_catalogue_limit_rows_by_last_id(pk_id, limit)
        if not rows:
            break
        for row in rows:
            import_count += 1
            pk_id = row.id

            body = {
                'product_brand': row.product_brand,
                'product_model': row.product_model,
                'product_label': row.product_label,
                'product_brand_old': row.product_brand_old,
                'product_model_old': row.product_model_old,
                'product_class': row.product_class,
                'ind': row.ind,
                'oud': row.oud,
                'wid': row.wid,
                'speed_g': row.speed_g,
                'speed_o': row.speed_o,
                'weight': row.weight,
                'serie': row.serie,
                'accuracy': row.accuracy,
                'preload': row.preload,
                'seal': row.seal,
                'angle': row.angle,
                'r_size': row.r_size,
                'r_matel': row.r_matel,
                'assembly_no': row.assembly_no,
                'assembly_type': row.assembly_type,
                'note': row.note,
                'tag': row.tag.split(' '),
            }
            es.add_index(index, doc_type, body, row.id)
        print('import count: %s' % import_count)


if __name__ == '__main__':
    import_catalogue()
