import sys
sys.path.append("..")
from blackjack.Arena import Arena
from blackjack.Dealer import Dealer
from blackjack.Player import Player
from blackjack.Gamer import Gamer
from utils import *

A = ["停止叫牌", "继续叫牌"]
display = False
player = Player(action_space = A, display = display)
dealer = Dealer(action_space = A, display = display)
arena = Arena(display = display, action_space = A)

arena.play_games(dealer, player, num = 200000)

def policy_evaluation(episodes, V, Ns):
    for episode, r in episodes:
        for s, a in episode:
            ns = get_dict(Ns, s)  # 状态s 在该序列中出现了多少遍
            v = get_dict(V, s)
            set_dict(Ns, ns + 1, s)
            set_dict(V, v + (r - v) / (ns + 1), s)

V = {}
Ns = {}
policy_evaluation(arena.episodes, V, Ns)
