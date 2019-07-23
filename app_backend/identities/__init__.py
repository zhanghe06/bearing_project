#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: __init__.py.py
@time: 2019-06-27 00:50
"""

from __future__ import unicode_literals

from app_backend.permissions import SectionNeed, SectionActionNeed


def setup_section(identity, section_name):
    identity.provides.add(SectionNeed(section_name))


def setup_section_action(identity, section_name, *actions):
    for action in actions:
        identity.provides.add(SectionActionNeed(section_name, action))
