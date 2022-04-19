from math import floor
from time import time
from typing import List
from utils.routing import Router
from utils.genetic import get_initial_pop

class GeneticSolver:
    def __init__(self, problem_info : Router, run_time : int):
        self._problem_info = problem_info
        self._run_time = run_time
        self._pop_size = len(problem_info.graph.streets) // problem_info.num_cars // 10
        self._min_pop_size = 100
        self._queen_ratio = 0.4
        self._run_time = run_time

    def set_pop_size(self, pop_size):
        self._pop_size = pop_size

    def set_min_pop_size(self, min_size):
        self._min_pop_size = min_size

    def set_queen_ratio(self, queen_ratio):
        self._queen_ratio = queen_ratio

    def genetic_loop(self, population : List[List[int]]):
        init_time = time()

        while(time() - init_time < self._run_time):
            pass

    def solve(self):
        n_streets = len(self._problem_info.graph.streets)
        queen_num = floor(self._pop_size * self._queen_ratio)
        print("Generating Population...")
        start_time = time()
        population = get_initial_pop(self._problem_info, max(self._pop_size, self._min_pop_size), queen_num, n_streets * 2, self._problem_info.time_itinerary * 1.2)
        print(f"Population generated in {time() - start_time} seconds!")
        
        return self.genetic_loop(population)

    pop_size = property(fset=set_pop_size)
    min_pop_size = property(fset=set_min_pop_size)
    queen_ratio = property(fset=set_queen_ratio)
