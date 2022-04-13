from copy import deepcopy
import random
from typing import List

from utils import graph


def add_node(solution: List[int], graph: graph.Graph) -> List[List[int]]:
    if len(graph.junctions) == 0:
        return []

    if len(solution) == 0:
        return [[random.choice(graph.junctions).id]]

    last_node = graph.junctions[solution[-1]]

    solutions = []

    for node_id in last_node.neighbours:
        node = graph.junctions[node_id].id
        solutions.append(solution.copy() + [node])

    return solutions


def remove_node(solution: List[int], _: graph.Graph):
    if len(solution) < 1:
        return []
    return [solution.copy()[:-1]]


def placebo_solution(solution: List[int], _: graph.Graph):
    return solution


def add_middle_node(solution: List[int], graph: graph.Graph):
    solutions = []

    for (idx, node_id) in enumerate(solution):
        if (idx == len(solution) - 1):
            break

        node = graph.junctions[node_id]
        next_node = graph.junctions[solution[idx+1]]

        for middle_id in node.neighbours:
            middle = graph.junctions[middle_id]
            if next_node.id in middle.neighbours:
                solutions.append(solution[:idx-1] +
                                 [middle_id] + solution[idx+1:])

    return solutions


NEIGHBOURHOOD_FUNCTIONS = [add_node, remove_node]

ACTION_RATIO = 0.8


def select_car_solution(solutions: List[int], _: graph.Graph):
    return random.choice(solutions)


def neighbour_multiple_cars(solution: List[List[int]], graph: graph.Graph):
    output = []

    for car in solution:
        if random.random() < ACTION_RATIO:
            f = random.choice(NEIGHBOURHOOD_FUNCTIONS)
            sols = f(car, graph)
            print(f, sols, car)
            selected = select_car_solution(sols, graph)
            output.append(selected)
        else:
            output.append(car)
    return output


def neighbour_single_car(solution: List[int], graph: graph.Graph):
    if (len(solution) == 0):
        return []

    idx = random.randint(0, len(solution) - 1)

    output = deepcopy(solution)

    f = random.choice(NEIGHBOURHOOD_FUNCTIONS)

    sols = f(output[idx], graph)

    if (sols == []):
        return []

    selected = select_car_solution(sols, graph)
    output[idx] = selected

    return output
