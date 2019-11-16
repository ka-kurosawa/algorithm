# -*- coding: UTF-8 -*-
'''
Created on 2016/05/28

@author: ka-kurosawa
'''
import random
import copy
import scipy as sci

class Sudoku:
    def __init__(self):
        self.line_list = sci.array([[0, 2, 7, 0, 0, 9, 0, 0, 0],
                                 [0, 0, 0, 2, 0, 0, 0, 0, 1],
                                 [0, 0, 0, 0, 0, 6, 3, 0, 8],
                                 [6, 8, 2, 0, 3, 0, 0, 0, 0],
                                 [0, 1, 0, 0, 0, 2, 0, 7, 0],
                                 [0, 4, 0, 6, 1, 0, 0, 3, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 4, 0, 7],
                                 [0, 0, 3, 9, 0, 0, 0, 1, 0]])

        # 数字の空白部分の位置を保持する配列
        self.empty_list = []

        # まだ使われていない(=使う候補)数字の配列
        self.kouho_list = []
        for i in range(1, 10):
            for j in range(1, 10):
                self.kouho_list.append(i)
                
        for i, line in enumerate(self.line_list):
            temp_list = (line == 0)
            for j in line:
                if (j != 0):
                    # 既に使われている数字を候補から除外
                    self.kouho_list.remove(j)
            self.empty_list.append([[i], sci.where(temp_list)[0]])
        self.geanSize = []
        geanCount = 0
        
        # 遺伝子長(=空欄の数)を求めておく
        for temp in self.empty_list:
            geanCount += temp[1].size
        self.geanSize = geanCount

    # 評価関数
    def eval_func(self, gean):
        line_list = self.line_list.copy()
        count = 0
 
        for i, empty in enumerate(self.empty_list):
            for j in empty[1]:
                line_list[i][j] = gean[count]
                count += 1
                
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
    
        value = 0
        """
        各縦、横、ブロックをそれぞれ見ていき、数字の種類につき加算する。
        もし完成していたら、9×9×3=243のスコアになるはず(9×9の場合)
        """
        "縦"
        for line in line_list:
            value += len(sci.intersect1d(line, [1, 2, 3, 4, 5, 6, 7, 8, 9]))
        "横"
        for row in row_list:
            value += len(sci.intersect1d(row, [1, 2, 3, 4, 5, 6, 7, 8, 9]))
        "ブロック"
        for block in block_list:
            value += len(sci.intersect1d(block, [1, 2, 3, 4, 5, 6, 7, 8, 9]))
        return value

    # 遺伝アルゴリズム
    def genetic_optimize(self):
        """
        maxiter: 世代数
        popsize: 個体数
        popnum: 遺伝子長
        elite: 生き残る遺伝子の割合
        cross: 交叉確率
        mutation: 突然変異確率
        """
        maxiter = 10000
        popsize = 20
        popnum = self.geanSize
        elite = 0.3
        cross = 0.3
        mutation = 0.1
        line_list = self.line_list.copy()
 
        
        # 遺伝子の初期化
        pop = []
        for i in range(popsize):
            random.shuffle(self.kouho_list)
            vec = self.kouho_list.copy()
            pop.append(vec)
        
        # 交叉アルゴリズムの選択
        crossover = self.two_point_crossover
     
        # メインループ
        topelite = int(elite * popsize)
        for i in range(maxiter):
            scores = [(self.eval_func(v), v) for v in pop]
            scores.sort()
            
            # スコアの小さいものから淘汰するため
            scores.reverse()
            ranked = [v for (s, v) in scores]
            # 自然淘汰
            pop = ranked[0:topelite]
            # 突然変異、交叉
            while len(pop) < popsize:
                if random.SystemRandom().random() < mutation:
                    # 突然変異
                    c = random.SystemRandom().randint(0, topelite)
                    pop.append(self.mutate(popnum, ranked[c]))
     
                if random.SystemRandom().random() < cross:
                    # 交叉
                    c1 = random.SystemRandom().randint(0, topelite)
                    c2 = random.SystemRandom().randint(0, topelite)
                    pop.append(crossover(popnum, ranked[c1], ranked[c2]))

            # 解が発見されたら探索終了
            if scores[0][0] == 243:
                break
            # 500回ごとに出力してみる
            if i % 500 == 0:
                print ("count " + str(i) + "  Interim:", scores[0])

        count = 0
        for i, empty in enumerate(self.empty_list):
            for j in empty[1]:
                line_list[i][j] = scores[0][1][count]
                count += 1
        print("End  Result:", scores[0])
        return line_list
    
    # 突然変異
    def mutate(self, popnum, vec):
        i = random.SystemRandom().randint(0, popnum - 1)
        return vec[:i] + [random.SystemRandom().randint(1, 9)] + vec[i + 1:]
    
    # 1点交叉
    def one_point_crossover(self, popnum, r1, r2):
        i = random.SystemRandom().randint(1, popnum - 2)
 
        return random.SystemRandom().choice((r1[0:i] + r2[i:], r2[0:i] + r1[i:]))
 
    # 2点交叉
    def two_point_crossover(self, popnum, r1, r2):
        i, j = sorted(random.SystemRandom().sample(range(popnum), 2))
        return random.SystemRandom().choice((r1[0:i] + r2[i:j] + r1[j:] , r2[0:i] + r1[i:j] + r2[j:]))
 
    # 一様交叉
    def uniform_crossover(self, popnum, r1, r2):
        q1 = copy.copy(r1)
        q2 = copy.copy(r2)
        for i in range(len(r1)):
            if random.SystemRandom().random() < 0.5:
                q1[i], q2[i] = q2[i], q1[i]
        return random.SystemRandom().choice([q1, q2])

    def main(self):
        ans = self.genetic_optimize()
        print("Answer:")
        print(ans)
        
if __name__ == '__main__':
    sudoku = Sudoku()
    sudoku.main()

