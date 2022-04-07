from typing import List
import graph
import random
import time


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
    i = j = 0

    while i < len(parent1):
        while j < len(parent2):
            pass
    return 1

# sum = 0

# for i in range(0, 100):
#     list1 = [random.randint(0,1000) for i in range(0, random.randint(10000, 100000))]
#     list2 = [random.randint(0,1000) for i in range(0, random.randint(10000, 100000))]

#     start = time.time()
#     singlepoint_crossover(list1, list2)
#     end = time.time()

#     sum += (end - start)

# print(sum/100)

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
network.add_street(1, 2, 1, 1, False)
network.add_street(2, 3, 1, 1, False)
network.add_street(2, 4, 1, 1, False)
network.add_street(3, 4, 1, 1, False)
network.add_street(4, 5, 1, 1, False)
network.add_street(5, 6, 1, 1, False)
network.add_street(5, 7, 1, 1, False)
network.add_street(7, 6, 1, 1, True)


# for junction in network.junctions:
#     print(junction)
#     for street in junction.streets:
#         print(street)


print(junction3.is_neighbour(junction1))



# print(singlepoint_crossover([1,2,3,4,5,6], [1,7,8,4,9,10]))