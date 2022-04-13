import random
from typing import List
from .graph import Graph, Street
from .routing import Router


def greedy_solve(problem_info: Router):
    solutions = [[problem_info.initial_junction]
                 for _ in range(problem_info.num_cars)]
    problem_info.graph.reset_streets()
    
    for car in range(problem_info.num_cars):
        last_junction = problem_info.graph.junctions[solutions[car][-1]]
        non_visited: List[Street] = []

        for street in last_junction.streets:
            if not street.visited:
                non_visited.append(street)

        street: Street = None

        if len(non_visited) > 0:
            street = random.choice(non_visited)
            street.visited = True
        else:
            street = random.choice(last_junction.streets)

        solutions[car].append(
            street.final.id if street.initial.id == last_junction.id else street.initial.id)

    return solutions


def get_initial_pop(problem_info: Router, size: int, queen_num: int):
    pass
