# -*- coding: utf-8 -*-

# 从Gamer中继承dealer
import sys
sys.path.append("..")
from blackjack.Gamer import Gamer

class Dealer(Gamer):
    def __init__(self, name = "", action_space = None, display = False):
        super(Dealer, self).__init__(name, action_space, display)
        self.role = '庄家'
        self.policy = self.dealer_policy # 庄家的策略
        
    def first_card_value(self):
        # 展示第一张牌的值
        if self.cards is None or len(self.cards) == 0:
            return 0
        else:
            return self._value_of(self.cards[0])
        
    
    def dealer_policy(self):
        '''
        庄家的策略，知道点数超过17小于等于21则停止
        或者当点数超过21也停止
        返回的是action
        '''
        action = ''
        if self.get_points()[0] < 17:
            action = self.action_space[0]
        else:
            action = self.action_space[1]
            
        return action