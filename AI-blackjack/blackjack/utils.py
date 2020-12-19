#!/usr/bin/env python
# coding: utf-8

# In[3]:

import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def str_key(*args):
    """
    将参数用 _ 连起来作为字典的键，需注意参数本身是tuple或者list型，比如类似((a,b,c), d)
    """
    new_arg = []
    for arg in args:
        if type(arg) in [list, tuple]:
            new_arg += [str(a) for a in arg]
        else:
            new_arg.append(str(arg))
    return '_'.join(new_arg)    


# In[2]:


def set_dict(target_dict, value, *args):
    target_dict[str_key(*args)] = value

def get_dict(target_dict, *args):
    return target_dict.get(str_key(*args), 0)    

def set_prob(P, s, a, s1, p = 1.0):
    set_dict(P, p, s, a, s1)

def get_prob(P, s, a, s1):
    return P.get(str_key(s, a, s1), 0)

def set_reward(R, s, a, r):
    set_dict(R, r, s, a)
    
def get_reward(R, s, a):
    return R.get(str_key(s, a),0)

def display_dict(target_dict):
    for key in target_dict.keys():
        print("{}: {:.2f}".format(key, target_dict[key]))
    print("")
    
def set_value(V, s, v):
    set_dict(V, v, s)
    
def get_value(V, s):
    return V.get(str_key(s), 0)

def set_pi(Pi, s, a, p = 0.5):
    set_dict(Pi, p, s, a)

def get_pi(Pi, s, a):
    return Pi.get(str_key(s, a), 0)


def greedy_pi(A, s, Q, a):
    '''
    在行为空间A中，在状态s下，贪婪选择a行为的概率
    要考虑多个行为的价值相同的情况
    '''
    max_q, max_a = -float("inf"), []
    #q = get_dict(Q,s)
    for opt_a in A:
        opt_q = get_dict(Q, s, opt_a)
        if opt_q > max_q:
            max_q = opt_q
            max_a = [opt_a]
        elif opt_q == max_q:
            max_a.append(opt_a)
    n = len(max_a)
    if n == 0:
        return 0
    # 如果 a 是唯一最大的，n = 1, 返回的就是1. 如果a 不是唯一最大的就返回 1 / n
    # 如果 a 不是最大的，返回 0
    return 1.0 / n if a in max_a else 0.0


def greedy_policy(A, s, Q):
    '''
    给定一个状态空间A, 求一个状态s的贪婪策略
    '''
    max_q, max_a = -float("inf"), []
    for opt_a in A:
        q = get_dict(Q, s, opt_a)
        if q > max_q:
            max_q = q
            max_a = [opt_a]
        elif q == max_q:
            max_a.append(opt_a)
    return random.choice(max_a)


def epsilon_greedy_pi(A, s, Q, a, epsilon = 0.1):
    '''
    求在给定的A空间内，在状态s下，选择a行为，在epsilon-greedy策略下的概率为多少
    '''
    prob_a = greedy_pi(A, s, Q, a)
    m = len(A)
    if prob_a == 0:
        return epsilon / m
    n = int( 1 / prob_a )
    return (1 - epsilon) * prob_a + epsilon / m


def epsilon_greedy_policy(A, s, Q, epsilon, show_random_num = False):
    '''
    在给定的状态空间，给定的状态s下,根据epsilon-greedy策略选出的策略a是什么
    '''
    pis = []
    m = len(A)
    for i in range(m):
        pis.append(epsilon_greedy_pi(A, s, Q, A[i], epsilon))
    random_value = random.random()
    for i in range(m):
        if show_random_num:
            print("产生随机数为：{:.2f}, 拟减去概率{}".format(random_value, pis[i]))
        random_value -= pis[i] # 注意每次循环都要减一次
        if random_value < 0:
            return A[i] # 如果第一次出现了小于 0 的情况，直接就返回了 
    
    

def draw_value(value_dict, usable_ace = True, is_q_dict = False, A = None):
    fig = plt.figure()
    ax = Axes3D(fig)
    x = np.arange(1, 11, 1)
    y = np.arange(12, 22, 1)
    X, Y = np.meshgrid(x, y)
    row, col = X.shape
    Z = np.zeros((row, col))
    if is_q_dict:
        n = len(A)
    for i in range(row):
        for j in range(col):
            state_name = str(X[i,j]) + '_' + str(Y[i,j]) + '_' + str(usable_ace)
            if not is_q_dict:
                Z[i,j] = get_dict(value_dict, state_name)
            else:
                assert(A is not None)
                for a in A:
                    new_state_name = state_name + '_' + str(a)
                    q = get_dict(value_dict, new_state_name)
                    if q >= Z[i,j]:
                        Z[i,j] = q

    ax.plot_surface(X, Y, Z, rstride = 1, cstride = 1, color = 'lightgray')
    plt.show()

    
def draw_policy(policy, A, Q, epsilon, useable_ace = False):
    def value_of(a):

        if a == A[0]:

            return 0

        else:

            return 1

    rows, cols = 11, 10

    useable_ace = bool(useable_ace)

    Z = np.zeros((rows, cols))

    dealer_first_card = np.arange(1, 12) # 庄家第一张牌

    player_points = np.arange(12,22)

    for i in range(11, 22): # 玩家总牌点

        for j in range(1, 11): # 庄家第一张牌 

            s = j, i, useable_ace

            s = str_key(s)

            a = policy(A, s, Q, epsilon)

            Z[i-11,j-1] = value_of(a)

            #print(s, a)

    

    plt.imshow(Z, cmap=plt.cm.cool, interpolation=None, origin="lower", extent=[0.5,11.5,10.5,21.5])
    
    
    
    
    
    
    
    
