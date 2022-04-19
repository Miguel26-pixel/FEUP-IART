from math import floor
from time import time
from typing import List
from utils.routing import Router
from utils.genetic import get_initial_pop

def genetic_loop(problem_info : Router, population : List[List[int]], run_time : int):
    init_time = time()

    while(time() - init_time < run_time):

        pass

def genetic(problem_info : Router, min_pop_size : int, pop_size : int, queen_ratio : float, run_time : int):
    n_streets = len(problem_info.graph.streets)
    queen_num = floor(pop_size * queen_ratio)
    print("Generating Population...")
    start_time = time()
    population = get_initial_pop(problem_info, max(pop_size, min_pop_size), queen_num, n_streets * 2, problem_info.time_itinerary * 1.2)
    print(f"Population generated in {time() - start_time} seconds!")
    
    return genetic_loop(problem_info, population, run_time)