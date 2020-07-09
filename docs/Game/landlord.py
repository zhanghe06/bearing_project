#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: landlord.py
@time: 2020-09-29 10:09
"""


# 角色定义
ROLE_LANDLORD = 1  # landlord 地主
ROLE_FARMER = 2  # farmer 农民
ROLE_FARMER_UP = 3  # up farmer 上游农民
ROLE_FARMER_DOWN = 4  # down farmer 下游农民
ROLE_VIEWER = 5  # viewer 观众

ROLES = {
    ROLE_LANDLORD: 'landlord',
    ROLE_FARMER: 'farmer',
    ROLE_FARMER_UP: 'farmer(up)',
    ROLE_FARMER_DOWN: 'farmer(down)',
    ROLE_VIEWER: 'viewer',
}


class Landlord(object):
    """斗地主"""
    def __init__(self):
        pass

    def cards(self):
        """台面"""
        pass

    def roles(self):
        """角色"""
        pass

    def start(self):
        """开局"""
        pass

    def close(self):
        """清盘"""
        pass

    def chase(self):
        """追击(争抢地主)"""
        pass

    def check(self):
        """让牌(不抢地主)"""
        pass

    def hand(self):
        """起牌(地主底牌)"""
        pass

    def wait(self):
        """等牌"""
        pass

    def call(self):
        """出牌(首牌/跟牌)"""
        pass

    def fold(self):
        """弃牌(盖牌/不跟)"""
        pass


if __name__ == '__main__':
    ll = Landlord()
    # 全新开局（1、洗牌；2、根据上一局结果确定发牌顺序；3、留3张底牌）
    ll.start()
    # 争抢地主（地主添加底牌）
    ll.chase() or ll.check()
    # 出牌弃牌（地主首先出牌）
    ll.call() or ll.fold()
    # 清盘计分
    ll.close()
