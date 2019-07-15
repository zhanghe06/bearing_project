#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: __init__.py.py
@time: 2019-06-27 00:50
"""

from __future__ import unicode_literals

from app_backend.permissions import SectionNeed, SectionActionNeed, SectionActionItemNeed

role_section_action_purchaser = ['add', 'search', 'stats', 'export']
role_section_action_manager = ['add', 'search', 'stats', 'export']
role_section_action_administrator = ['add', 'search', 'stats', 'export']

role_section_action_item_administrator = ['get', 'edit', 'del', 'audit', 'print']


def setup_section(identity, section_name):
    identity.provides.add(SectionNeed(section_name))


def setup_section_action(identity, section_name, *actions):
    for action in actions:
        identity.provides.add(SectionActionNeed(section_name, action))


def setup_section_item_action(identity, section_name, item_id, *actions):
    for action in actions:
        identity.provides.add(SectionActionItemNeed(section_name, action, item_id))


def setup_section_production(identity, *role_section_action):
    """产品"""
    setup_section_action(identity, 'production')
