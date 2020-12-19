# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 01:41:22 2020

@author: naive
"""

import sys
sys.path.append("..")
from MC_Player import MC_Player
from blackjack.Arena import Arena
from blackjack.Player import Player
from blackjack.Dealer import Dealer
from blackjack.Gamer import Gamer
import math



A = ["继续叫牌", "停止叫牌"]
display = False
player = MC_Player(action_space = A, display = display)
dealer = Dealer(action_space = A, display = display)
arena = Arena(action_space = A, display = display)
arena.play_games(dealer = dealer, player = player, num = 200000, show_statistics = True)

player.Q