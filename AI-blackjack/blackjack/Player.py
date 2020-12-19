# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
from blackjack.Gamer import Gamer
from blackjack.Dealer import Dealer
from blackjack.utils import str_key
class Player(Gamer):
    
    def __init__(self, name = "", action_space = None, display = False):
        super(Player, self).__init__(name, action_space, display)
        self.policy = self.player_policy
        self.role = "玩家"
        
    def get_state(self, dealer: Dealer):
        '''
        根据定义，每个状态是一个三元组(庄家的第一张牌，玩家的点数和，是否有usable ace)
        '''
        dealer_first_card_value = dealer.first_card_value()
        total_points, is_usable = self.get_points()
        return (dealer_first_card_value, total_points, is_usable)
    
    def get_state_name(self, dealer: Dealer):
        return str_key(self.get_state(dealer))
        
        
    
    def player_policy(self, dealer = None):
        '''
        玩家的策略:
            如果点数和少于20，就一直继续摸牌
        '''
        action = ''
        if self.get_points()[0] < 20:
            action = self.action_space[0]
        else:
            action = self.action_space[1]
        return action