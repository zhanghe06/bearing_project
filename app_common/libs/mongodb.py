#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: mongodb.py
@time: 2019-03-30 09:50
"""


import json
from datetime import date, datetime

from pymongo.collection import Collection


class MongodbInstance(object):
    """
    自定义mongodb工具
    """
    def __init__(self, conn, database, collection):
        self.conn = conn
        self.database_name = database
        self.collection_name = collection
        self.database = self.conn.get_database(database)
        self.collection = self.database.get_collection(collection)  # type: Collection

    @staticmethod
    def __default(obj):
        """
        支持datetime的json encode
        TypeError: datetime.datetime(2015, 10, 21, 8, 42, 54) is not JSON serializable
        :param obj:
        :return:
        """
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            raise TypeError('%r is not JSON serializable' % obj)

    def close_conn(self):
        """
        关闭连接
        关闭所有套接字的连接池和停止监控线程。
        如果这个实例再次使用它将自动重启和重新启动线程
        """
        self.conn.close()

    def find_one(self, condition=None):
        """
        查询单条记录
        :param condition:
        :return:
        """
        return self.collection.find_one(condition)

    def find_all(self, condition=None):
        """
        查询多条记录
        :param condition: 格式 主键或字典
        :return:
        """
        return self.collection.find(condition)

    def count(self, condition=None):
        """
        查询记录总数
        :param condition:
        :return:
        """
        return self.collection.count_documents(
            {'$and': list(map(dict, zip(condition.items())))} if condition else {}
        )

    def distinct(self, field_name):
        """
        查询某字段去重后值的范围
        :param field_name:
        :return:
        """
        return self.collection.distinct(field_name)

    def insert_one(self, data):
        """
        插入数据
        :param data:
        :return:
        """
        try:
            result = self.collection.insert_one(data)
            return result
        except Exception as e:
            raise Exception('插入失败：%s' % e)

    def insert_many(self, data):
        """
        批量插入数据
        :param data:
        :return:
        """
        try:
            result = self.collection.insert_many(data)
            return result
        except Exception as e:
            raise Exception('插入失败：%s' % e)

    def update_many(self, condition, update_data, update_type='set', upsert=False):
        """
        批量更新数据
        :param condition:
        :param update_data:
        :param update_type: 范围：['inc', 'set', 'unset', 'push', 'pushAll', 'addToSet', 'pop', 'pull', 'pullAll', 'rename']
        :param upsert: 如果不存在update的记录，是否插入；true为插入，默认是false，不插入。
        :return:
        """
        allowed_type = ['inc', 'set', 'unset', 'push', 'pushAll', 'addToSet', 'pop', 'pull', 'pullAll', 'rename']
        if update_type not in allowed_type:
            raise Exception('更新失败，类型错误：%s' % update_type)
        try:
            result = self.collection.update_many(condition, {'$%s' % update_type: update_data}, upsert=upsert)
            # 返回匹配数量、更新数量; 更新数量仅支持 Mongodb 2.6 及以上版本
            return result
        except Exception as e:
            raise Exception('更新失败: %s' % e)

    def delete_one(self, condition=None):
        """
        删除文档记录
        :param condition: 格式 主键或字典
        :return:
        """
        result = self.collection.delete_one(condition)
        if result.get('err') is None:
            # print('删除成功，删除行数%s' % result.get('n', 0))
            return result.get('n', 0), None
        else:
            # print('删除失败：%s' % result.get('err'))
            return 0, result.get('err')

    def output_row(self, condition=None, style=0):
        """
        格式化输出单个记录
        style=0 键值对齐风格
        style=1 JSON缩进风格
        :param condition: 格式 主键或字典
        :param style:
        :return:
        """
        row = self.find_one(condition)
        if style == 0:
            # 获取KEY最大的长度作为缩进依据
            max_len_key = max([len(each_key) for each_key in row.keys()])
            str_format = '{0: >%s}' % max_len_key
            keys = [str_format.format(each_key) for each_key in row.keys()]
            result = dict(zip(keys, row.values()))
            print('**********  表名[%s.%s]  **********' % (self.database_name, self.collection_name,))
            for key, item in result.items():
                print(key, ':', item)
        else:
            print(json.dumps(row, indent=4, ensure_ascii=False, default=self.__default))

    def output_rows(self, condition=None, style=0):
        """
        格式化输出批量记录
        style=0 键值对齐风格
        style=1 JSON缩进风格
        :param condition: 格式 主键或字典
        :param style:
        :return:
        """
        rows = self.find_all(condition)
        total = self.count(condition)
        if style == 0:
            count = 0
            for row in rows:
                # 获取KEY最大的长度作为缩进依据
                max_len_key = max([len(each_key) for each_key in row.keys()])
                str_format = '{0: >%s}' % max_len_key
                keys = [str_format.format(each_key) for each_key in row.keys()]
                result = dict(zip(keys, row.values()))
                count += 1
                print('**********  表名[%s.%s]  [%d/%d]  **********' % (self.database_name, self.collection_name, count, total,))
                for key, item in result.items():
                    print(key, ':', item)
        else:
            for row in rows:
                print(json.dumps(row, indent=4, ensure_ascii=False, default=self.__default))
