# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
from blackjack.utils import str_key
class Gamer:
    def __init__(self, name, action_space, display = False):
        self.name = name
        self.action_space = action_space
        self.display = display
        self.cards = [] # 手上的牌
        self.cards_sum = 0 # 手上所有牌的总分
        self.policy = None # 策略
        self.learning_methods = None # 学习方法
        
    def __str__(self): # 返回姓名的属性, 我们print(当前对象)输出的东西就为name
        return self.name
    
    def _value_of(self, card):
        """
        根据牌的字符输出牌的实际值
        2-10 为 其原本数值
        J K Q为10
        A 取为 1
        
        card: str  
        表示牌的字符
        """
        try:
            v = int(card)
        except:
            if card in ['J', 'K', 'Q']:
                v = 10
            elif card == 'A':
                v = 1
            else:
                v = 0
        finally:
            return v
    
    def get_points(self):
        """
        统计手上牌的总分
        如果用到了A = 11，同时返回usable_ace = true
        
        """
        total_point = 0
        usable_ace = 0 # 开始时默认为false，如果有了就usable_ace + 1, 这么做可以方便处理碰上多个Ace的情况
        if self.cards is None:
            return 0, False
        
        for card in self.cards:
            # 首先判断当前的牌是不是A
            if card == 'A':
                # 如果是，那么要判断下A应该取11还是1
                if 11 + total_point > 21:
                    total_point += 1
                else:
                    total_point += 11
                    usable_ace += 1
            else:
                total_point += self._value_of(card)
        return total_point, bool(usable_ace)
    
    def receive(self, cards):
        # 玩家收到一张或多张牌
        cards = list(cards)
        for card in cards:
            self.cards.append(card)
            
    def discharge_cards(self):
        # 玩家把手上的牌清空
        self.cards.clear()
    
    def cards_info(self):
        # 展示玩家手上的牌的信息
        if self.display:
            print("{} current cards: {}\n".format(self, self.cards), end = "")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        