from copy import deepcopy
import heapq
import random
from typing import List

from utils import graph
from utils import routing
from utils.routing import Router
from utils.solution import check_solution


def add_node(solution: List[int], router: Router) -> List[List[int]]:
    graph = router.graph
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


def remove_node(solution: List[int], _: Router):
    if len(solution) < 1:
        return []
    return [solution.copy()[:-1]]


def add_middle_node(solution: List[int], router: Router):
    solutions = []

    graph = router.graph

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


def remove_middle_node(solution: List[int], router: Router):
    solutions = []

    graph = router.graph

    for idx in range(1, len(solution) - 1):

        prev_node = graph.junctions[solution[idx-1]]
        next_node_id = solution[idx+1]
        if next_node_id in prev_node.neighbours:
            solutions.append(solution[:idx] + solution[idx+1:])

    return solutions


def add_multiple_nodes(solution: List[int], router: Router):
    if len(solution) < 2:
        return []

    graph = router.graph

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

def add_multiple_nodes_crossover(solution: List[int], solution2: List[int], router: Router):
    if len(solution) < 2 or len(solution2) < 2:
        return []

    graph = router.graph

    initial = random.randint(0, len(solution) - 1)
    final = random.randint(0, len(solution2) - 1)
    initial_node = graph.junctions[solution[initial]].id
    final_node = graph.junctions[solution2[final]].id

    dists = inverse_dijkstra(graph, initial_node)
    if not (final_node in dists.keys()):
        return [solution, solution2]

    path = []

    while final_node != initial_node:
        (_, next_node, _) = dists[final_node]
        path.append(next_node)
        final_node = next_node

    path.reverse()

    return [solution[:initial] + path + solution2[final:]]

def remove_multiple_nodes(solution: List[int], router: Router):
    if len(solution) < 2:
        return []

    graph = router.graph

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


def remove_end_nodes(solution: List[int], router: Router):
    graph = router.graph
    cuttoff = random.randint(1, len(solution))

    return [solution[:cuttoff]];

def random_growth(solution: List[int], router: Router):
    graph = router.graph
    max_growth = max(len(graph.streets) - len(solution), 0)
    growth = random.randint(0, max_growth)
    copy = solution.copy()

    if len(solution) == 0:
        return [copy]

    for i in range(growth):
        junction = graph.junctions[copy[-1]]

        street = random.choice(junction.streets)
        copy.append(street.final.id if street.initial.id == junction.id else street.initial.id)

    return [copy]

NEIGHBOURHOOD_FUNCTIONS = [
    remove_end_nodes, random_growth, add_multiple_nodes, remove_multiple_nodes
]


def remove_multiple_nodes(solution: List[int], router: Router):
    if len(solution) < 2:
        return []

    graph = router.graph

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

def select_car_solution(solutions: List[List[int]], _: Router):
    return random.choice(solutions)


def select_best_car_solution(solutions: List[List[int]], router: Router):
    best_score = 0
    best_sol = []

    for sol in solutions:
        (_, score) = check_solution(router, sol)
        print(sol,)
        if score > best_score:
            best_sol = sol
            best_score = score
    return best_sol


def neighbour_multiple_cars(solution: List[List[int]], router: Router, action_ratio: float, functions):
    output = []

    graph = router.graph

    for car in solution:
        if random.random() < action_ratio:
            f = random.choice(functions)
            sols = f(car, router)
            if sols == []:
                selected = car.copy()
            else:
                selected = select_car_solution(sols, router)
            output.append(selected)
        else:
            output.append(car)
    return output


def neighbour_single_car(solution: List[int], router: Router, _: float, functions):
    if (len(solution) == 0):
        return []

    graph = router.graph

    idx = random.randint(0, len(solution) - 1)

    output = deepcopy(solution)

    f = random.choice(functions)

    sols = f(output[idx], router)

    if (sols == []):
        return []

    selected = select_car_solution(sols, graph)
    output[idx] = selected

    return output


def neighbour_hill_climb_single_car(solution: List[int], router: Router, _: float, functions):
    if (len(solution) == 0):
        return []

    idx = random.randint(0, len(solution) - 1)

    best_score = 0
    best_sol = []

    for f in functions:
        output = deepcopy(solution)

        sols = f(output[idx], router)

        if (sols == []):
            continue

        selected = select_car_solution(sols, router)
        output[idx] = selected

        (_, score) = check_solution(router, output)

        if score > best_score:
            best_sol = output
            best_score = score

    return best_sol


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
