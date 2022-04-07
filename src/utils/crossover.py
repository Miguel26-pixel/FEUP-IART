from typing import List
from . import graph
import random


def get_common_junctions(list1, list2):
    return (set(list1) & set(list2))


def get_crossover_point(parent1: List[int], parent2: List[int]):
    common_junctions = get_common_junctions(parent1, parent2)

    if(len(common_junctions) == 0):
        return None

    chosen_junction = random.choice(tuple(common_junctions))
    junction_indexes = set()

    for idx, junction in enumerate(parent1):
        if junction == chosen_junction:
            junction_indexes.add(idx)

    chosen_idx1 = random.choice(tuple(junction_indexes))
    junction_indexes.clear()

    for idx, junction in enumerate(parent2):
        if junction == chosen_junction:
            junction_indexes.add(idx)

    chosen_idx2 = random.choice(tuple(junction_indexes))

    return (chosen_idx1, chosen_idx2)

# should we remove cycles?


def singlepoint_crossover(parent1: List[int], parent2: List[int], graph: graph.Graph):
    points = get_crossover_point(parent1, parent2)

    if points == None:
        return parent1

    (idx1, idx2) = points

    return parent2[:idx2] + parent1[idx1:]

# one offspring version of SA


def SA_crossover(parent1: List[int], parent2: List[int], graph: graph.Graph):
    neighbours = set()
    match_point_list = set()

    for junction_num in parent2:
        neighbours.update(graph.junctions[junction_num].neighbours)

    for idx, junction_num in enumerate(parent1):
        junction = graph.junctions[junction_num]

        if junction in neighbours:
            match_point_list.add(idx)

    chosen_j = random.choice(tuple(match_point_list))
    chosen_junction_j = graph.junctions[parent1[chosen_j]]

    cross_point_list = set()

    for idx, junction_num in enumerate(parent2):
        junction = graph.junctions[junction_num]

        if chosen_junction_j in junction.neighbours:
            cross_point_list.add(idx)

    chosen_i = random.choice(tuple(cross_point_list))

    return parent2[:chosen_i + 1] + parent1[chosen_j:]
