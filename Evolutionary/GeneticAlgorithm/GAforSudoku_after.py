# -*- coding: UTF-8 -*-
'''
Created on 2014/03/16

@author: kurosawakazuma
'''
import random  # ランダムモジュール
import copy
import scipy as sci
import itertools as iter
 
def nimotu_init():
    line_list = sci.array([[0, 2, 7, 0, 0, 9, 0, 0, 0],
                             [0, 0, 0, 2, 0, 0, 0, 0, 1],
                             [0, 0, 0, 0, 0, 6, 3, 0, 8],
                             [6, 8, 2, 0, 3, 0, 0, 0, 0],
                             [0, 1, 0, 0, 0, 2, 0, 7, 0],
                             [0, 4, 0, 6, 1, 0, 0, 3, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 4, 0, 7],
                             [0, 0, 3, 9, 0, 0, 0, 1, 0]])
        
    empty_list = []
    kouho_list = []
    for i in range(1, 10):
        for j in range(1, 10):
            kouho_list.append(i)
            
    for i, line in enumerate(line_list):
        temp_list = (line == 0)
#         print (i)
#         print (temp_list)
        for j in line:
            if (j != 0):
                kouho_list.remove(j)
                
        empty_list.append([[i], sci.where(temp_list)[0]])
    geanCount = 0
    for temp in empty_list:
        geanCount += temp[1].size
    geanSize = 4 * geanCount
    return [line_list, empty_list, kouho_list, geanSize]
# #評価関数
def eval_func(line_list, empty_list, geanSize):
# #    gean = [0,0,1,0,1,1,1,0,1,1]
    line_list, empty_list, kouho_list, geanSize = nimotu_init()
    print (sorted(set(list(iter.permutations(kouho_list , 3)))))
    count = 0
    for i, empty in enumerate(empty_list):
        for j in empty[1]:
            cell = ""
            for k in geanSize[count:count + 4]:
                cell += str(int(k))
            if (0 < int(cell, 2) and int(cell, 2) < 10):
                line_list[i][j] = int(cell, 2)
            count += 4
            
    row_list = sci.array([line_list[:, 0],
                  line_list[:, 1],
                  line_list[:, 2],
                  line_list[:, 3],
                  line_list[:, 4],
                  line_list[:, 5],
                  line_list[:, 6],
                  line_list[:, 7],
                  line_list[:, 8]])
 
    block_list = sci.array([sci.append(line_list[0:3, 0:1], [line_list[0:3, 1:2], line_list[0:3, 2:3]]),
                       sci.append(line_list[0:3, 3:4], [line_list[0:3, 4:5], line_list[0:3, 5:6]]),
                       sci.append(line_list[0:3, 6:7], [line_list[0:3, 7:8], line_list[0:3, 8:9]]),
                        sci.append(line_list[3:6, 0:1], [line_list[3:6, 1:2], line_list[3:6, 2:3]]),
                        sci.append(line_list[3:6, 3:4], [line_list[3:6, 4:5], line_list[3:6, 5:6]]),
                        sci.append(line_list[3:6, 6:7], [line_list[3:6, 7:8], line_list[3:6, 8:9]]),
                        sci.append(line_list[6:9, 0:1], [line_list[6:9, 1:2], line_list[6:9, 2:3]]),
                        sci.append(line_list[6:9, 3:4], [line_list[6:9, 4:5], line_list[6:9, 5:6]]),
                        sci.append(line_list[6:9, 6:7], [line_list[6:9, 7:8], line_list[6:9, 8:9]])])

#     print(line_list)
    value = 0
    for line in line_list:
        value += len(sci.intersect1d(line, [1, 2, 3, 4, 5, 6, 7, 8, 9]))
#         value -= len(sci.where(line == 0))
    for row in row_list:
        value += len(sci.intersect1d(row, [1, 2, 3, 4, 5, 6, 7, 8, 9]))
#         value -= len(sci.where(row == 0))
    for block in block_list:
        value += len(sci.intersect1d(block, [1, 2, 3, 4, 5, 6, 7, 8, 9]))
#         value -= len(sci.where(block == 0))
#     print ("value:" + str(value))
    return value
 
def geneticoptimize(line_list, empty_list, geanSize):
    """
    maxiter = 1, 繰り返し数
    maximize = True,    スコアを最大化
    popsize = 50,   個体数
    popnum = 10,    遺伝子数（長さ）
    elite = 0.2,    生き残る遺伝子の割合
    mutprob =0.2    突然変異のおこる確率
    """
    maxiter = 10
    maximize = True
    popsize = 40
    popnum = geanSize
    elite = 0.4
    mutprob = 0.01
    # 突然変異
    def mutate(vec):
        i = random.SystemRandom().randint(0, popnum - 1)
        if vec[i] == 0:
            return vec[:i] + [1] + vec[i + 1:]
        else:
            return vec[:i] + [0] + vec[i + 1:]
     # 1点交叉 非推奨
    def one_point_crossover(r1, r2):
        i = random.SystemRandom().randint(1, popnum - 2)
 
        return random.SystemRandom().choice((r1[0:i] + r2[i:], r2[0:i] + r1[i:]))
 
    # 2点交叉
    def two_point_crossover(r1, r2):
        i, j = sorted(random.SystemRandom().sample(range(popnum), 2))
        return random.SystemRandom().choice((r1[0:i] + r2[i:j] + r1[j:] , r2[0:i] + r1[i:j] + r2[j:]))
 
    # 一様交叉
    def uniform_crossover(r1, r2):
        q1 = copy.copy(r1)
        q2 = copy.copy(r2)
        for i in range(len(r1)):
            if random.SystemRandom().random() < 0.5:
                q1[i], q2[i] = q2[i], q1[i]
 
        return random.SystemRandom().choice([q1, q2])
    # 遺伝子の初期化
    pop = []
    for i in range(popsize):
        vec = [random.SystemRandom().randint(0, 1) for i in range(popnum)]
        # print vec
        pop.append(vec)
    # 遺伝子の初期化
 
    # 交叉アルゴリズムの選択
    # crossover = two_point_crossover
    crossover = two_point_crossover
 
    # メインループ
    topelite = int(elite * popsize)
    for i in range(maxiter):
        scores = [(eval_func(line_list, empty_list, v), v) for v in pop]
        scores.sort()
        if maximize:
            scores.reverse()
        ranked = [v for (s, v) in scores]
        # 弱い遺伝子は淘汰される
        pop = ranked[0:topelite]
        # 生き残った遺伝子同士で交叉したり突然変異したり
        while len(pop) < popsize:
            if random.SystemRandom().random() < mutprob:
                # 突然変異
                c = random.SystemRandom().randint(0, topelite)
                pop.append(mutate(ranked[c]))
 
            else:
                # 交叉
                c1 = random.SystemRandom().randint(0, topelite)
                c2 = random.SystemRandom().randint(0, topelite)
                pop.append(crossover(ranked[c1], ranked[c2]))
        if scores[0][0] > 220:
            break
# #        # 暫定の値を出力
        # print(scores[0][0])
        # print(scores[0])
    count = 0
    for i, empty in enumerate(empty_list):
        for j in empty[1]:
            cell = ""
            for k in scores[0][1][count:count + 4]:
                cell += str(int(k))
            if (0 < int(cell, 2) and int(cell, 2) < 10):
                line_list[i][j] = int(cell, 2)
            count += 4
    print(line_list)
    return scores[0]

def main():
    line_list, empty_list, kouho_list, geanSize = nimotu_init()
#     gean = sci.ones(geanSize)
#     eval_func(line_list, row_list, block_list, empty_list, gean);
    ans = geneticoptimize(line_list, empty_list, geanSize)
    print("Ans:", ans)
    
if __name__ == '__main__':
    main()
