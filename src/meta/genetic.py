from math import floor
from utils.routing import Router

def get_initial_pop(problem_info: Router, size: int, queen_num: int, max_iterations, time_out):
    return [[] for _ in range(size)]

def genetic(problem_info : Router, min_pop_size : int, queen_ratio : float):
    n_streets = len(problem_info.graph.streets)
    pop_size = n_streets // problem_info.num_cars // 10
    queen_num = floor(pop_size * queen_ratio)

    population = get_initial_pop(problem_info, max(pop_size, min_pop_size), queen_num, problem_info.graph.streets * 2, problem_info.time_itinerary * 1.2)