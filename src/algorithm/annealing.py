import math
from random import random
from typing import List, Callable

from utils import graph
from utils.routing import Router
from utils.solution import check_solution


def simulated_annealing(
        problem_info: Router,
        max_iterations: int,
        initial_temp: float,
        temp_variation: Callable[[int], float],
        neighbour_function: Callable[[List[List[int]], graph.Graph, float], List[int]],
        action_ratio: float,
        sol: List[List[int]]):

    f = open("temp.csv", "x")

    curr_sol = sol
    curr_best = 0  # calculate solution
    curr_temp = initial_temp
    initial = check_solution(problem_info, sol)[1]

    for i in range(max_iterations):
        curr_temp = temp_variation(initial_temp, i)

        if curr_temp <= 0:
            return curr_sol

        new_sol = neighbour_function(
            curr_sol, problem_info.graph, action_ratio)

        # Calculate solution
        (valid, new_sol_score) = check_solution(problem_info, new_sol)

        if valid and new_sol_score > curr_best:
            curr_sol = new_sol
            curr_best = new_sol_score

        delta = new_sol_score - curr_best

        print(i, curr_temp, delta, math.exp(float(delta) /
              curr_temp), curr_best, new_sol_score, initial)

        f.write(f"{i},{curr_best},{new_sol_score},{curr_temp}\n")

        prob = math.exp(float(delta) / curr_temp)
        if valid and (delta > 0) or (random() < prob):
            curr_sol = new_sol
            curr_best = new_sol_score

    return curr_sol
