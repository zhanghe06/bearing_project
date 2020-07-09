#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: poker.py
@time: 2020-09-29 10:44
"""

from itertools import product
import random

# 花色 suit
SUIT_HEART = 1  # heart 红桃(春) 红
SUIT_DIAMOND = 2  # diamond 方片(夏) 红
SUIT_CLUB = 3  # club 梅花(秋) 黑
SUIT_SPADE = 4  # spade 黑桃(冬) 黑

SUIT = {
    SUIT_HEART: '♥',
    SUIT_DIAMOND: '♦',
    SUIT_CLUB: '♣',
    SUIT_SPADE: '♠',
}
# 部分玩法区分花色大小 顺序: 黑红梅方

# 顺序牌 sequence
SEQUENCE = {
    3: '3',
    4: '4',
    5: '5',
    6: '6',
    7: '7',
    8: '8',
    9: '9',
    10: '10',
    11: 'J',
    12: 'Q',
    13: 'K',
    14: 'A',
}

# 王牌 trump
TRUMP = {
    15: '2',
}

# 鬼牌 joker
JOKER = {
    16: 'BJ',  # 小王/黑鬼
    17: 'CJ',  # 大王/花鬼
}


class Poker(object):
    """扑克牌"""

    prefix_first = '┌──'
    prefix_second = '│'
    prefix_third = '│'
    prefix_fourth = '│'
    prefix_last = '└──'

    suffix_first = '───┐'
    suffix_second = '   │'
    suffix_third = '   │'
    suffix_fourth = '   │'
    suffix_last = '───┘'

    def __init__(self, packs=1):
        """
        初始化
        :param packs: 默认一副牌
        """
        card_list = SEQUENCE.values() + TRUMP.values()
        jock_list = JOKER.values()
        suit_list = SUIT.values()
        self.cards = ([' '.join(c) for c in product(card_list, suit_list)] + jock_list) * packs

    def shuffle(self):
        """洗牌"""
        random.shuffle(self.cards)
        print(self.cards)

    def deal(self, n=1):
        """发牌"""
        if n > len(self.cards):
            raise Exception('牌数不够')
        deal_cards = []
        for i in range(0, n):
            deal_cards.append(self.cards.pop())
        self.show(deal_cards)

    def show(self, cards):
        """扇牌"""
        list_first = []
        list_second = []
        list_third = []
        list_fourth = []
        list_last = []
        for i, card in enumerate(cards):
            first = self.prefix_first
            items = card.split()
            sequence = items[0]
            suit = ''
            if len(items) == 2:
                sequence, suit = items
            second = self.prefix_second + '{:<2s}'.format(sequence)
            third = self.prefix_third + ('{:<4s}'.format(suit) if suit else '  ')
            fourth = self.prefix_fourth + '  '
            last = self.prefix_last
            list_first.append(first)
            list_second.append(second)
            list_third.append(third)
            list_fourth.append(fourth)
            list_last.append(last)
            # 是否最后一张
            if i < len(cards) - 1:
                continue
            list_first.append(self.suffix_first)
            list_second.append(self.suffix_second)
            list_third.append(self.suffix_third)
            list_fourth.append(self.suffix_fourth)
            list_last.append(self.suffix_last)
        line_first = ''.join(list_first)
        line_second = ''.join(list_second)
        line_third = ''.join(list_third)
        line_fourth = ''.join(list_fourth)
        line_last = ''.join(list_last)
        print('\n'.join([line_first, line_second, line_third, line_fourth, line_last]))


if __name__ == '__main__':
    poker = Poker()
    poker.shuffle()
    poker.deal(3)
    # poker.show()
