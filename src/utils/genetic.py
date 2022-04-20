import random
from typing import List
from .graph import Graph, Street
from .routing import Router

def greedy_solve(problem_info: Router, max_iterations : int, time_out : int):
    solutions = [[problem_info.initial_junction]
                 for _ in range(problem_info.num_cars)]
    current_time_out = [time_out for _ in range(problem_info.num_cars)]
    cars = list(range(problem_info.num_cars))
    non_visited_num = len(problem_info.graph.streets)
    problem_info.graph.reset_streets()

    while non_visited_num > 0 and max_iterations > 0 and len(cars) > 0:
        max_iterations -= 1

        for car in cars:
            last_junction = problem_info.graph.junctions[solutions[car][-1]]
            non_visited: List[Street] = []

            for street in last_junction.streets:
                if not street.visited:
                    non_visited.append(street)

            street: Street = None

            if len(non_visited) > 0:
                street = random.choice(non_visited)
                street.visited = True
                non_visited_num -= 1
            else:
                street = random.choice(last_junction.streets)

            solutions[car].append(
                street.final.id if street.initial.id == last_junction.id else street.initial.id)
            current_time_out[car] -= street.time

            if current_time_out[car] < 0:
                cars.remove(car)

    return solutions


def random_solve(problem_info: Router, max_iterations : int, time_out : int):
    solutions = [[problem_info.initial_junction]
                 for _ in range(problem_info.num_cars)]
    current_time_out = [time_out for _ in range(problem_info.num_cars)]
    cars = list(range(problem_info.num_cars))
    problem_info.graph.reset_streets()

    while max_iterations > 0 and len(cars) > 0:
        max_iterations -= 1

        for car in cars:
            last_junction = problem_info.graph.junctions[solutions[car][-1]]

            street = random.choice(last_junction.streets)

            solutions[car].append(
                street.final.id if street.initial.id == last_junction.id else street.initial.id)
            current_time_out[car] -= street.time

            if current_time_out[car] < 0:
                cars.remove(car)

    return solutions


def get_initial_pop(problem_info: Router, size: int, queen_num: int, max_iterations, time_out):
    population = []
    total = size - queen_num

    for _ in range(queen_num):
        population.append(greedy_solve(problem_info, max_iterations, time_out))

    for _ in range(total):
        population.append(random_solve(problem_info, max_iterations, time_out))

    return population

def normalize_solutions(evals: List[int]):
    sum_evals = sum(evals)
    return [x / sum_evals for x in evals]

def selection_ga(evals: List[int], solutions):
    normalized = normalize_solutions(evals)
    return random.choices(solutions, normalized)
