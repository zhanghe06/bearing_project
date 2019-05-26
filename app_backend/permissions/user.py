#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: user.py
@time: 2019-05-12 09:57
"""

from __future__ import unicode_literals

from functools import partial

import six

from app_backend.permissions import SectionActionNeed, BasePermission, SectionActionItemNeed

# -------------------------------------------------------------
# 用户板块操作权限（创建、查询、导出、统计）
UserSectionNeed = partial(SectionActionNeed, 'user')
UserSectionNeed.__doc__ = """A need with the section preset to `"user"`."""

permission_user_section_add = BasePermission(UserSectionNeed('add'))
permission_user_section_search = BasePermission(UserSectionNeed('search'))
permission_user_section_export = BasePermission(UserSectionNeed('export'))
permission_user_section_stats = BasePermission(UserSectionNeed('stats'))


# -------------------------------------------------------------
# 用户明细操作权限(读取、更新、删除、打印)
UserItemNeed = partial(SectionActionItemNeed, 'user')
UserItemNeed.__doc__ = """A need with the section preset to `"user"`."""

UserItemGetNeed = partial(UserItemNeed, 'get')
UserItemEditNeed = partial(UserItemNeed, 'edit')
UserItemDelNeed = partial(UserItemNeed, 'del')
UserItemPrintNeed = partial(UserItemNeed, 'print')


class UserItemGetPermission(BasePermission):
    def __init__(self, user_id):
        need = UserItemGetNeed(six.text_type(user_id))
        super(UserItemGetPermission, self).__init__(need)


class UserItemEditPermission(BasePermission):
    def __init__(self, user_id):
        need = UserItemEditNeed(six.text_type(user_id))
        super(UserItemEditPermission, self).__init__(need)


class UserItemDelPermission(BasePermission):
    def __init__(self, user_id):
        need = UserItemDelNeed(six.text_type(user_id))
        super(UserItemDelPermission, self).__init__(need)


class UserItemPrintPermission(BasePermission):
    def __init__(self, user_id):
        need = UserItemPrintNeed(six.text_type(user_id))
        super(UserItemPrintPermission, self).__init__(need)