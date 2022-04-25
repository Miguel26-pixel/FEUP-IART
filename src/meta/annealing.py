import math
from random import random
import signal
from time import time
from typing import List, Callable

from utils import graph
from utils.draw import print_annealing, write_output
from utils.genetic import greedy_solve
from utils.routing import Router
from utils.solution import check_solution
from utils.neighbourhood import NEIGHBOURHOOD_FUNCTIONS, add_node, neighbour_hill_climb_single_car, neighbour_multiple_cars, neighbour_single_car, remove_multiple_nodes, remove_node, add_multiple_nodes

finished = False


def handler(signum, frame):
    global finished
    finished = True


def run_annealing(router: Router, parser):

    curr_best = 0

    signal.signal(signal.SIGINT, handler)

    print("GENERATING SOLUTION")

    for x in range(100):
        sol = greedy_solve(router, len(router.graph.streets) * 2,
                           router.time_itinerary*1.2)
        score = check_solution(router, sol)[1]
        print(x, score)
        if score > curr_best:
            curr_best = score
            curr_sol = sol

    print("END GENERATING SOLUTION")

    print(router.num_cars)
    print(check_solution(router, curr_sol))

    ALPHA = 1.5

    TEMP_VARIATION = [
        lambda initial, i: initial / (1 + math.log(1 + i)),
        lambda initial, i: initial / (1 + ALPHA * math.log(1 + i)),
        lambda initial, i: initial /
        (1 + ALPHA * math.log(1 + math.pow(i, 2))),
    ]

    NEIGHBOURHOOD_FUNCTIONS = [
        neighbour_single_car, neighbour_multiple_cars, neighbour_hill_climb_single_car]

    final_sol = simulated_annealing(
        router, parser.i, parser.t, TEMP_VARIATION[parser.tf], NEIGHBOURHOOD_FUNCTIONS[parser.nf], parser.ar, curr_sol)

    print(check_solution(router, final_sol))
    write_output(final_sol, router, open("output.txt", "w"))


def simulated_annealing(
        problem_info: Router,
        max_iterations: int,
        initial_temp: float,
        temp_variation: Callable[[int], float],
        neighbour_function: Callable[[List[List[int]], graph.Graph, float], List[int]],
        action_ratio: float,
        sol: List[List[int]]):
    global finished

    f = open("temp.csv", "w")
    f.write(f"iteration,curr_best,new_sol_score,curr_temp\n")

    finished = False

    start_time = time()

    curr_sol = sol
    curr_best = 0  # calculate solution
    curr_temp = initial_temp
    initial = check_solution(problem_info, sol)[1]

    for i in range(max_iterations):
        if finished:
            break
        curr_temp = temp_variation(initial_temp, i)

        if curr_temp <= 0:
            return curr_sol

        new_sol = neighbour_function(
            curr_sol, problem_info, action_ratio, [add_node, remove_multiple_nodes, remove_node, add_multiple_nodes])

        # Calculate solution
        (valid, new_sol_score) = check_solution(problem_info, new_sol)

        delta = new_sol_score - curr_best

        f.write(f"{i},{curr_best},{new_sol_score},{curr_temp}\n")
        prob = math.exp(float(delta) / curr_temp)
        if valid and (delta > 0) or (random() < prob):
            curr_sol = new_sol
            curr_best = new_sol_score

        print_annealing(i, time() - start_time, curr_best, new_sol_score)
        
    return curr_sol
