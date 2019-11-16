'''
Created on 2016/05/14

@author: ka-kurosawa
'''
from bisect import bisect
from random import random


class AntMotion(object):
    
    '初期化'
    def __init__(self, initial_position, fields, alpha, beta):
        self.initial_position = initial_position
        self.fields = fields
        self.ALPHA = alpha
        self.BETA = beta
        self.before_run()
        
    def before_run(self):
        self.next_coodinate = -1
        self.current_coordinate = self.initial_position
        self.tour_len = 0.0
        self.paths = []
    
    'メイン処理'
    def run(self):
        self.before_run()
        available_positions = list(range(len(self.fields['coordinates'])))
        available_positions.pop(self.initial_position)
        
        while available_positions:
            self.next_coodinate = self.select_next_position(available_positions)
            self.paths.append(self.current_coordinate)
            self.tour_len += self.fields['districts'][self.current_coordinate][self.next_coodinate]
            self.current_coordinate = self.next_coodinate
            available_positions.remove(self.next_coodinate)
        
        self.tour_len += self.fields['districts'][self.current_coordinate][self.initial_position]
        self.paths.append(self.current_coordinate)
        
        return self.paths

    def get_path_value(self, cur, to):
        pheromone = self.fields['pheromones'][cur][to]
        distance = self.fields['districts'][cur][to]
        return pheromone ** self.ALPHA * ((1.0 / distance) ** self.BETA)

    '移動する座標を決定'
    def select_next_position(self, coordinates):
        weights = []
        for candidate in coordinates:
            weights.append(self.get_path_value(self.current_coordinate, candidate))
        total = sum(weights)
        
        cumulation = 0
        cdf_vals = []
        for w in weights:
            cumulation += w
            cdf_vals.append(cumulation / total)
            
        return coordinates[bisect(cdf_vals, random())]
