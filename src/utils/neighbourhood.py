from copy import deepcopy
import heapq
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


def remove_middle_node(solution: List[int], graph: graph.Graph):
    solutions = []

    for idx in range(1, len(solution) - 1):

        prev_node = graph.junctions[solution[idx-1]]
        next_node_id = solution[idx+1]
        if next_node_id in prev_node.neighbours:
            solutions.append(solution[:idx] + solution[idx+1:])

    return solutions



def add_multiple_nodes(solution: List[int], graph: graph.Graph):
    if len(solution) < 2:
        return []

    initial = random.randint(0, len(solution) - 2)
    final = random.randint(initial + 1, len(solution) - 1)
    initial_node = graph.junctions[solution[initial]].id
    final_node = graph.junctions[solution[final]].id

    dists = inverse_dijkstra(graph, initial_node)
    if not (final_node in dists.keys()):
        return [solution]

    path = []

    while final_node != initial_node:
        (_, next_node, _) = dists[final_node]
        path.append(next_node)
        final_node = next_node

    path.reverse()

    return [solution[:initial] + path + solution[final:]]


def remove_multiple_nodes(solution: List[int], graph: graph.Graph):
    if len(solution) < 2:
        return []

    initial = random.randint(0, len(solution) - 2)
    final = random.randint(initial + 1, len(solution) - 1)
    initial_node = graph.junctions[solution[initial]].id
    final_node = graph.junctions[solution[final]].id

    dists = dijkstra(graph, initial_node)
    if not (final_node in dists.keys()):
        return [solution]

    path = []

    while final_node != initial_node:
        (_, next_node, _) = dists[final_node]
        path.append(next_node)
        final_node = next_node

    path.reverse()

    return [solution[:initial] + path + solution[final:]]


def remove_end_nodes(solution: List[int], graph: graph.Graph):
    cuttoff = random.randint(1, len(solution))

    return [solution[:cuttoff]];

def random_growth(solution: List[int], graph: graph.Graph):
    max_growth = max((len(graph.streets) - len(solution)) // 2, 0)
    growth = random.randint(0, max_growth)
    copy = solution.copy()

    for i in range(growth):
        junction = graph.junctions[copy[-1]]

        street = random.choice(junction.streets)
        copy.append(street.final.id if street.initial.id == junction.id else street.initial.id)

    return [copy]


NEIGHBOURHOOD_FUNCTIONS = [
    remove_end_nodes, random_growth, add_multiple_nodes, remove_multiple_nodes
]


def select_car_solution(solutions: List[int], _: graph.Graph):
    return random.choice(solutions)


def neighbour_multiple_cars(solution: List[List[int]], graph: graph.Graph, action_ratio: float):
    output = []

    for car in solution:
        if random.random() < action_ratio:
            f = random.choice(NEIGHBOURHOOD_FUNCTIONS)
            sols = f(car, graph)
            if sols == []:
                selected = car.copy()
            else:
                selected = select_car_solution(sols, graph)
            output.append(selected)
        else:
            output.append(car)
    return output


def neighbour_single_car(solution: List[int], graph: graph.Graph, _: float):
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


def inverse_dijkstra(graph: graph.Graph, start: int, ):
    """Visit all nodes and calculate the shortest paths to each from start"""
    queue = [(0, 0, start)]
    distances = {start: (0, None, 1)}
    visited = set()

    idx = 0

    while queue:
        _, _, node = heapq.heappop(queue)  # (distance, node), ignore distance
        if node in visited:
            continue
        visited.add(node)
        (dist, _, path_size) = distances[node]

        for street in graph.junctions[node].streets:
            junction = street.final.id
            neighbour_dist = street.time / street.length
            if junction in visited:
                continue
            neighbour_dist += dist
            if neighbour_dist / path_size < distances.get(junction, (float('inf'), None, 1))[0]:
                idx += 1
                heapq.heappush(
                    queue, (neighbour_dist / path_size, idx, junction))
                distances[junction] = (
                    neighbour_dist / path_size, node, path_size + 1)

    return distances


def dijkstra(graph: graph.Graph, start: int, ):
    """Visit all nodes and calculate the shortest paths to each from start"""
    queue = [(0, 0, start)]
    distances = {start: (0, None, 1)}
    visited = set()

    idx = 0

    while queue:
        _, _, node = heapq.heappop(queue)  # (distance, node), ignore distance
        if node in visited:
            continue
        visited.add(node)
        (dist, _, path_size) = distances[node]

        for street in graph.junctions[node].streets:
            junction = street.final.id
            neighbour_dist = street.length
            if junction in visited:
                continue
            neighbour_dist += dist
            if neighbour_dist < distances.get(junction, (float('inf'), None, 1))[0]:
                idx += 1
                heapq.heappush(
                    queue, (neighbour_dist, idx, junction))
                distances[junction] = (
                    neighbour_dist, node, path_size + 1)

    return distances