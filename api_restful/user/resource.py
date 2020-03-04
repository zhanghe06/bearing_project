#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: resource.py
@time: 2020-02-28 21:26
"""


from __future__ import unicode_literals

from flask import jsonify, make_response
from flask_restful import Resource, marshal, reqparse, abort
from werkzeug.exceptions import NotFound, BadRequest
from app_common.decorators.resource import api_response
from api_restful import app
from api_restful.user.api import (
    get_user_row_by_id,
    delete_user,
    get_user_pagination,
    add_user,
    edit_user,
)
from api_restful.user.request import (
    structure_key_item,
    request_parser,
    request_post,
    request_put,
    request_delete,
)
from api_restful.user.response import fields_item
from app_common.maps.status_delete import STATUS_DEL_OK, STATUS_DEL_NO

DEFAULT_PAGE = app.config['DEFAULT_PAGE']
DEFAULT_SITE = app.config['DEFAULT_SITE']

SUCCESS_MSG = app.config['API_SUCCESS_MSG']
FAILURE_MSG = app.config['API_FAILURE_MSG']


class UserResource(Resource):
    """
    UserResource
    """
    decorators = [
        # token_auth.login_required,
    ]

    def get(self, pk):
        """
        Example:
            curl http://0.0.0.0:8000/user/1
        :param pk:
        :return:
        """
        data = get_user_row_by_id(pk)

        if not data:
            abort(NotFound.code, msg='没有记录', status=False)
        if data.status_delete == STATUS_DEL_OK:
            abort(NotFound.code, msg='已经删除', status=False)

        result = marshal(data, fields_item, envelope=structure_key_item)
        return jsonify(result)

    def put(self, pk):
        """
        Example:
            curl http://0.0.0.0:8000/user/1 -H "Content-Type: application/json" -X PUT -d '
            {
                "user": {
                    "name": "user name put"
                }
            }'
        :param pk:
        :return:
        """
        request_args = request_parser.parse_args()
        request_item_args = request_put.parse_args(req=request_args)

        if not request_item_args:
            abort(BadRequest.code, msg='参数错误', status=False)

        # 是否存在
        data = get_user_row_by_id(pk)

        if not data:
            abort(NotFound.code, msg='没有记录', status=False)
        if data.status_delete == STATUS_DEL_OK:
            abort(NotFound.code, msg='已经删除', status=False)

        # 更新数据
        request_data = request_item_args
        result = edit_user(pk, request_data)

        if not result:
            abort(NotFound.code, msg='更新失败', status=False)

        success_msg = SUCCESS_MSG.copy()
        success_msg['msg'] = '更新成功'
        return make_response(jsonify(success_msg), 200)

    def delete(self, pk):
        """
        Example:
            curl http://0.0.0.0:8000/user/1 -X DELETE
        :param pk:
        :return:
        """
        # 是否存在
        data = get_user_row_by_id(pk)

        if not data:
            abort(NotFound.code, msg='没有记录', status=False)
        if data.status_delete == STATUS_DEL_OK:
            abort(NotFound.code, msg='已经删除', status=False)

        # 删除数据
        result = delete_user(pk)

        if not result:
            abort(BadRequest.code, msg='删除失败', status=False)

        success_msg = SUCCESS_MSG.copy()
        success_msg['msg'] = '删除成功'
        return make_response(jsonify(success_msg), 200)


class UsersResource(Resource):
    """
    UsersResource
    """
    decorators = [
        # token_auth.login_required,
        api_response,
    ]

    def get(self):
        """
        Example:
            curl http://0.0.0.0:8000/user
            curl http://0.0.0.0:8000/user?page=1&size=20
        :return:
        """
        # 条件参数
        filter_parser = reqparse.RequestParser(bundle_errors=True)
        filter_parser.add_argument('page', type=int, default=DEFAULT_PAGE, location='args')
        filter_parser.add_argument('size', type=int, default=DEFAULT_SITE, location='args')
        filter_parser_args = filter_parser.parse_args()

        if not filter_parser_args:
            abort(BadRequest.code, msg='参数错误', status=False)

        pagination_obj = get_user_pagination(
            status_delete=STATUS_DEL_NO,
            **filter_parser_args
        )

        result = marshal(pagination_obj.items, fields_item, envelope=structure_key_item)
        result['total'] = pagination_obj.total
        return jsonify(result)

    def post(self):
        """
        Example:
            curl http://0.0.0.0:8000/user -H "Content-Type: application/json" -X POST -d '
            {
                "user": {
                    "name": "tom",
                    "salutation": "先生",
                    "mobile": "http://www.baidu.com",
                    "tel": "021-62345678",
                    "fax": "021-62345678",
                    "email": "haha@haha.com"
                }
            }'
        :return:
        """
        request_args = request_parser.parse_args()
        request_item_args = request_post.parse_args(req=request_args)

        if not request_item_args:
            abort(BadRequest.code, msg='参数错误', status=False)

        request_data = request_item_args
        result = add_user(request_data)

        if not result:
            abort(BadRequest.code, msg='创建失败', status=False)

        success_msg = SUCCESS_MSG.copy()
        success_msg['id'] = result
        success_msg['msg'] = '创建成功'
        return make_response(jsonify(success_msg), 200)

    def delete(self):
        """
        Example:
            curl http://0.0.0.0:8000/user -X DELETE -d '
            {
                "user": {
                    "id": [1, 2]
                }
            }'
        :return:
        """
        # 是否存在
        request_args = request_parser.parse_args()
        request_item_args = request_delete.parse_args(req=request_args)

        if not request_item_args:
            abort(BadRequest.code, msg='参数错误', status=False)

        request_data = request_item_args
        result = delete_user(request_data['id'])

        if not result:
            abort(BadRequest.code, msg='删除失败', status=False)

        success_msg = SUCCESS_MSG.copy()
        success_msg['msg'] = '删除成功'
        return make_response(jsonify(success_msg), 200)
