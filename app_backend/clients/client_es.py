#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: client_es.py
@time: 2018-04-10 20:27
"""


from elasticsearch import Elasticsearch
from app_backend import app

# app.config['']
# es_client = Elasticsearch(
#     ['192.168.4.1'],
#     http_auth=('elastic', 'changeme'),
# )

es_client = Elasticsearch()
