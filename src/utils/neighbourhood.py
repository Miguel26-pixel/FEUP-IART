from typing import List

from utils import graph


def add_node(solution: List[int], graph: graph.Graph):
    if len(graph.junctions == 0):
        return []

    last_node = graph.junctions[solution[-1]]

    solutions = []

    for node_id in last_node.neighbours:
        node = graph.junctions[node_id]
        solutions.append(solution.copy() + [node])

    return solutions


def remove_node(solution: List[int]):
    if len(solution) <= 1:
        return []
    return solution.copy()[:-1]
