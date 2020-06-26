#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: test_skf_categories.py
@time: 2020-05-19 16:32
"""

import csv

import requests


def test_get_skf_categories(csv_name, category_id):
    params = {
        'id': category_id,
        'language': 'en',
        'source': 'webpim',
        'site': '307',
        'hits': 100,
        'offset': 0,
    }
    url = 'https://search.skf.com/prod/search-skfcom/rest/apps/opc_v1/searchers/categories'
    header = ['Designation', 'd[mm]', 'D[mm]', 'B[mm]', 'C[kN]', 'Co[kN]', 'Pu[kN]', 'G-Speed[r/min]', 'O-Speed[r/min]']
    out = open('skf_%s.csv' % csv_name, 'a')
    csv_write = csv.writer(out, dialect='excel')
    csv_write.writerow(header)
    c = 0
    next_page = 0
    while 1:
        if next_page == -1:
            break
        res = requests.get(url, params=params).json()
        rows = res.get('documentList', {}).get('documents', [])
        for r in rows:
            data = [r['title']] + r['table_values']
            csv_write.writerow(data[:9])
            c += 1
        print(params['hits'] * next_page + len(rows))
        if res.get('documentList', {}).get('numberOfHits', 0) > params['hits'] * next_page + len(rows):
            next_page += 1
        else:
            next_page = -1
        params['offset'] = params['hits'] * next_page
    out.close()
    print('共计%s行记录' % c)


def run():
    category_map = {
        'angular_contact_ball_bearings': 'BA1_010',
        'cylindrical_roller_bearings': 'BC1_010',
        'angular_contact_thrust_ball_bearings_double_direction': 'BEA_010',
        'angular_contact_thrust_ball_bearings_for_screw_drives_single direction': 'BDA_010',
    }
    for k, v in category_map.items():
        test_get_skf_categories(k, v)


if __name__ == '__main__':
    run()
