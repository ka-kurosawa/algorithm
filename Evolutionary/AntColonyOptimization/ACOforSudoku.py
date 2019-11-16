'''
Created on 2016/05/14

@author: ka-kurosawa
'''



from Ant import AntMotion
import math
import sys
import scipy as sci


class AntColonySolver:
    '''
    蟻コロニー最適化で数独を解く
    '''

    def __init__(self):
        self.ALPHA = 1.0  # フェロモンを優先させる定数
        self.BETA = 2.0  # ヒューリスティックな情報を優先させる定数
        self.RHO = 0.5  # フェロモンの蒸発率
        self.Q = 100
        self.ANT_NUM = 30
        self.MAX_ITER = 500

        self.coordinates = sci.array([[0, 0],
                              [1, 3],
                              [3, 3],
                              [2, 5],
                              [6, 1],
                              [1, 0],
                              [2, 9],
                              [9, 12],
                              [8, 6],
                              [10, 2],
                              [7, 7],
                              [20, 5],
                              [15, 14],
                              [4, 19],
                              [30, 30],
                              [15, 22],
                              [23, 20],
                              [17, 0],
                              [1, 18],
                              [25, 25],
                              [10, 30],
                              [30, 16],
                              [6, 18],
                              [12, 13],
                              [7, 23],
                              [16, 4],
                              [27, 15],
                              [11, 21],
                              [16, 8],
                              [19, 11]])
        self.coords_num = len(self.coordinates)
        self.districts = self.calc_eval(self.coordinates)
        self.pheromones = self.get_pheromones()
        self.fields = dict(coordinates=self.coordinates,
                           coords_num=self.coords_num,
                           districts=self.districts,
                           pheromones=self.pheromones
                           )

    def calc_eval(self, coordinates):
        evals = sci.zeros(shape=(self.coords_num, self.coords_num))
        for i in range(self.coords_num):
            for j in range(i, self.coords_num):
                eval = 0
                if i != j : 
                    p1 = coordinates[i]
                    p2 = coordinates[j]
                    eval = math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
                evals[i][j] = evals[j][i] = eval
        
        return evals
    
    def get_pheromones(self):
        phers = sci.empty(shape=(self.coords_num, self.coords_num))
        phers[:] = 0.1
        return phers
    
    def get_ants(self, ant_num, alpha, beta):
        ants = []
        for _ in range(ant_num):
            ant = AntMotion(sci.random.randint(0, self.coords_num - 1), self.fields, alpha, beta)
            ants.append(ant)
        return ants
    
    def decay_pheromon(self, pheromon):
        pheromon *= (1.0 - self.RHO)
        return pheromon

    def delta_pheromon(self, tour_len):
        delta = self.Q / tour_len
        return delta
    
    # フェロモン情報の更新
    def update_pheromons(self, fields, ants):
        for i in range(len(fields['coordinates'])):
            for j in range(i, len(fields['coordinates'])):
                if i != j : 
                    pheromon = self.decay_pheromon(fields['pheromones'][i][j])
                    fields['pheromones'][i][j] = fields['pheromones'][j][i] = pheromon
        for ant in ants:
            for i in range(len(ant.paths)):
                f = ant.paths[i]
                t = ant.paths[i - 1]
                delta = self.delta_pheromon(ant.tour_len)
                fields['pheromones'][f][t] += delta
                fields['pheromones'][t][f] = fields['pheromones'][f][t]    
    
    def start(self, fields, ants):
        best_ant = None
        min_len = sys.maxsize
        for i in range(self.MAX_ITER):
            self.update_pheromons(fields, ants)
            for ant in ants:
                ant.run()
                if ant.tour_len < min_len:
                    best_ant = ant
                    min_len = ant.tour_len
                    print ("count" + str(i) + " : " + str(min_len))
        return best_ant
    
    def main(self):
        # 蟻
        ants = self.get_ants(self.ANT_NUM, self.ALPHA, self.BETA)
        # 最短距離を通った蟻
        best_ant = self.start(self.fields, ants)
        
        print (best_ant.paths)
     
if __name__ == '__main__':
    ant = AntColonySolver()
    ant.main()
