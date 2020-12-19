# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
from queue import Queue
from random import shuffle
from blackjack.Dealer import Dealer
from blackjack.Player import Player
from tqdm import tqdm
class Arena:
    '''
    负责游戏管理
    '''
    def __init__(self, display = None, action_space = None):
        self.display = display
        self.action_space = action_space
        self.cards = ['A','2','3','4','5','6','7','8','9','10',
                      'J', 'Q', 'K'] * 4
        self.card_q = Queue(maxsize = 52) # 洗好的牌
        self.cards_in_pool = [] # 已经用出去的公开的牌
        self.episodes = [] # 产生的对局信息列表
        self.load_card(self.cards) # 把牌装进发牌器
        
    def load_card(self, cards):
        '''
        把牌洗一洗，装进发牌器里
        '''
        shuffle(cards)
        for card in cards:
            self.card_q.put(card)
        cards.clear() # 原来的牌清空
        
    def reward_of(self, dealer: Dealer, player: Player):
        '''
        根据庄家和玩家手上牌的点数判断谁最终获胜了
        '''
        dealer_total_point, dealer_usable_ace = dealer.get_points()
        player_total_point, player_usable_ace = player.get_points()
        
        if player_total_point > 21:
            reward = -1
        else:
            if player_total_point > dealer_total_point or dealer_total_point > 21:
                reward = 1
            elif player_total_point == dealer_total_point:
                reward = 0
            else:
                reward = -1
        return reward, player_total_point, dealer_total_point, player_usable_ace


    def serve_card_to(self, gamer, n = 1):
        '''
        实现向玩家或者庄家发牌, 如果牌不够，就将公开区域的牌洗一遍重发
        n 为 一次连续发牌的数量
        '''
        cards = []
        for _ in range(n):
            # 考虑没有牌的情况
            if self.card_q.empty():
                self._info("发牌器没有牌了，整理废牌，重新洗牌")
                shuffle(self.cards_in_pool)
                self._info("一共整理了{}张废牌，重新投入发牌器\n".format(len(self.cards_in_pool)))
                assert(len(self.cards_in_pool) > 20)
                self.load_card(self.cards_in_pool)
            cards.append(self.card_q.get())
        self._info("发了{}张牌({})给{}{}".format(n, cards, gamer.role, gamer))
        gamer.receive(cards) # 玩家收到牌
        gamer.cards_info()
    
    
    
    def _info(self, message):
        if self.display:
            print(message, end = "")
    
    
    def recycle_card(self, *players):
        """
        当一局结束以后，Arena还需要将玩家和庄家的手牌都收到牌池中
        """
        if len(players) == 0:
            return
        for player in players:
            for card in player.cards:
                self.cards_in_pool.append(card)
            player.discharge_cards()
        
        
        
    def play_game(self, dealer: Dealer, player: Player):
        '''
        使得玩家和庄家进行一次对局, 生成一个状态序列以及最终奖励
        '''
        self._info("=========开始新一局=========\n")
        self.serve_card_to(dealer, 2)
        self.serve_card_to(player, 2)
        episode = [] # 记录每一轮游戏的信息
        if player.policy == None:
            self._info("玩家需要一个策略")
            return 
        if dealer.policy == None:
            self._info("庄家需要一个策略")
            return
        while True:
            # 对玩家产生一个行为
            action = player.policy(dealer)
            self._info("{}{}选择：{}".format(player.role, player, action))
            # 记录下当前的状态s 以及对应的行为 a
            episode.append((player.get_state_name(dealer), action))
            if action == player.action_space[0]:
                # 如果继续叫牌
                self.serve_card_to(player, 1)
            else:
                # 停止游戏
                break
        # 玩家停止叫牌以后要判断玩家有没有爆点
        reward, player_total_point, dealer_total_point, player_usable_ace = self.reward_of(dealer, player)
            
        if player_total_point > 21:
            self._info("玩家{}爆点, 得分{}\n".format(player, reward))
            self.recycle_card(player, dealer)
            self.episodes.append((episode, reward)) # 将这一轮游戏的信息添加进episodes里
            self._info("=======本局结束======\n")
            return episode, reward
        
        # 若没有超过21点
        self._info("\n")   
        while True:
            # 计算庄家得分
            action = dealer.policy()
            self._info("{}{}选择：{}".format(dealer.role, dealer, action))
            if action == dealer.action_space[0]:
                # 如果庄家继续叫牌
                self.serve_card_to(dealer, 1)
            else:
                break
        self._info("\n双方均停止叫牌\n")
        reward, player_total_point, dealer_total_point, player_usable_ace = self.reward_of(dealer, player)
        player.cards_info()
        dealer.cards_info()
        if reward == 1:
            self._info("玩家赢了")
        elif reward == 0:
            self._info("庄家赢了")
        else:
            self._info("双方平局")
        self._info("玩家{}点, 庄家{}点".format(player_total_point, dealer_total_point))
        self._info("=======本局结束=======")
        self.recycle_card(player, dealer)
        self.episodes.append((episode, reward))
        return episode, reward
    
    def play_games(self, dealer: Dealer, player: Player, num = 2, show_statistics = True):
        '''
        生成多次对局
        '''
        results = [0,0,0] # 玩家负和胜的局数
        self.episodes.clear()
        for i in tqdm(range(num)):
            episode, reward = self.play_game(dealer, player)
            results[reward + 1] += 1
            if player.learning_methods is not None:
                # 每打一盘就进行一次学习
                player.learning_methods(episode, reward)
                
        if show_statistics:
            print("一共玩了{}局，其中玩家获胜{}，平局{}，输局{}，胜率{:.2f}，不输率{}".format(num, results[2], results[1],
                  results[0], results[2] / num, (results[2] + results[1])/num ))
        
    
    
    
    
    
    
    
    
    