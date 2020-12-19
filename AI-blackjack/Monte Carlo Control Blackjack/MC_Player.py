# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 21:52:21 2020

@author: naive
"""

import sys
sys.path.append("..")
from blackjack.utils import get_dict, set_dict, epsilon_greedy_policy
from blackjack.Arena import Arena
from blackjack.Player import Player
from blackjack.Dealer import Dealer
from blackjack.Gamer import Gamer
import math


class MC_Player(Player):
    '''
    构建一个具备蒙特卡洛控制的玩家
    '''
    def __init__(self, name = "", action_space = None, display = False):
        super(MC_Player, self).__init__(name, action_space, display)
        self.Q = {} # 跟之前的V类似，这里是每一状态行为对所对应的行为价值函数
        self.Nsa = {} # 对每一个(s,a) 记录出现的次数
        self.total_learning_times = 0
        self.policy = self.epsilon_greedy_policy
        self.learning_methods = self.learning_Q # 自己的学习方法
    
    
    def learning_Q(self, episode, r):
        '''
        其中episode是一个完整的序列，r是该序列对应的reward
        '''
        for s, a in episode:
            nsa = get_dict(self.Nsa, s, a)
            q = get_dict(self.Q, s, a)
            set_dict(self.Nsa, nsa + 1, s, a)
            set_dict(self.Q, q + (r - q) / (nsa + 1), s, a)
        self.total_learning_times += 1
        
    def reset_memory(self):
        '''
        忘记过往的学习
        '''
        self.Q.clear()
        self.Nsa.clear()
        self.total_learning_times = 0
        
        
    
    def epsilon_greedy_policy(self, dealer, epsilon = None):
        player_points, _ = self.get_points()
        if player_points >= 21:
            return self.action_space[1]
        elif player_points <= 11:
            return self.action_space[0]
        
        else:
            A, Q = self.action_space, self.Q
            s = self.get_state_name(dealer)
            if epsilon is None:
                epsilon = 1 / (1 + 4 * math.log10(1 + self.total_learning_times))
        
        
        return epsilon_greedy_policy(A, s, Q, epsilon)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        