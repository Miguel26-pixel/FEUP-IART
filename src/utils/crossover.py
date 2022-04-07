from typing import List
import graph
import random
import time
import cProfile
import re

def get_common_junctions(list1, list2):
    return (set(list1) & set(list2))

def get_crossover_point(parent1 : List[int], parent2 : List[int]):
    common_junctions = get_common_junctions(parent1, parent2)

    if(len(common_junctions) == 0):
        return None

    chosen_junction = random.choice(tuple(common_junctions))
    junction_indexes = []

    for idx, junction in enumerate(parent1):
        if junction == chosen_junction:
            junction_indexes.append(idx)

    chosen_idx1 = random.choice(junction_indexes)
    junction_indexes.clear()

    for idx, junction in enumerate(parent2):
        if junction == chosen_junction:
            junction_indexes.append(idx)

    chosen_idx2 = random.choice(junction_indexes)

    return (chosen_idx1, chosen_idx2)

# should we remove cycles?

def singlepoint_crossover(parent1 : List[int], parent2 : List[int], graph : graph.Graph):
    points = get_crossover_point(parent1, parent2)

    if points == None:
        return parent1

    (idx1, idx2) = points

    return parent2[:idx2] + parent1[idx1:]

# one offspring version of SA

def SA_crossover(parent1 : List[int], parent2 : List[int], graph : graph.Graph):
    cross_point_list = []
    match_point_list = {}

    for i, junction_i_num in enumerate(parent1):
        junction_i = graph.junctions[junction_i_num]
        for j, junction_j_num in enumerate(parent2):
            junction_j = graph.junctions[junction_j_num]
            if junction_j in junction_i.neighbours:
                cross_point_list.append(i)

                if i in match_point_list.keys():
                    match_point_list[i].append(j)
                else:
                    match_point_list[i] = [j]

    if len(cross_point_list) == 0:
        return parent1

    chosen_i = random.choice(cross_point_list)
    chosen_j = random.choice(match_point_list[chosen_i])

    return parent1[:chosen_i + 1] + parent2[chosen_j:]

def SA_crossover2(parent1 : List[int], parent2 : List[int], graph : graph.Graph):
    neighbours = set()
    match_point_list = set()

    for junction_num in parent1:
        neighbours = neighbours.union(graph.junctions[junction_num].neighbours)

    for idx, junction_num in enumerate(parent2):
        junction = graph.junctions[junction_num]

        if junction in neighbours:
            match_point_list.add(idx)

    chosen_j = random.choice(tuple(match_point_list))
    chosen_junction_j = graph.junctions[parent2[chosen_j]]

    cross_point_list = set()

    for idx, junction_num in enumerate(parent1):
        junction = graph.junctions[junction_num]

        if chosen_junction_j in junction.neighbours:
            cross_point_list.add(idx)

    chosen_i = random.choice(tuple(cross_point_list))

    return parent1[:chosen_i + 1] + parent2[chosen_j:]

network = graph.Graph()

junction1 = graph.Junction((0,0))
junction2 = graph.Junction((1,1))
junction3 = graph.Junction((2,2))
junction4 = graph.Junction((3,3))
junction5 = graph.Junction((4,4))
junction6 = graph.Junction((5,5))
junction7 = graph.Junction((6,6))
junction8 = graph.Junction((7,7))

network.junctions = [junction1, junction2, junction3, junction4, junction5, junction6, junction7, junction8]

network.add_street(0, 1, 1, 1, True)
network.add_street(0, 2, 1, 1, False)
network.add_street(2, 4, 1, 1, False)
network.add_street(3, 4, 1, 1, False)
network.add_street(4, 5, 1, 1, False)
network.add_street(5, 6, 1, 1, False)
network.add_street(5, 7, 1, 1, False)
network.add_street(7, 6, 1, 1, True)


def test():
    sum = 0

    for i in range(0, 100):
        list1 = [random.randint(0,1000) for i in range(0, random.randint(10000, 50000))]
        list2 = [random.randint(0,1000) for i in range(0, random.randint(10000, 50000))]

        network = graph.Graph()

        network.junctions = [graph.Junction((random.randint(1,10000),1)) for i in range(1001)]

        for j in range(0, 1000):
            network.add_street(random.randint(0, 1000), random.randint(0, 1000), 1, 1, bool(random.getrandbits(1)))

        start = time.time()
        SA_crossover2(list1, list2, network)
        end = time.time()

        sum += (end - start)

    print(sum/100)


# print(SA_crossover2([0, 1, 3], [0,2,4,5,6], network))
# print(singlepoint_crossover([1,2,3,4,5,6], [1,7,8,4,9,10]))
cProfile.run('test()')
