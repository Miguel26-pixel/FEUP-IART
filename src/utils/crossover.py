from typing import List
import random
import time

# def get_common_junctions(list1: List[int], list2: List[int]):
#     junctions_in_list1 = {}
#     common_junctions = {}

#     for idx, junction in enumerate(list1):
#         if junction in junctions_in_list1.keys():
#             junctions_in_list1[junction].append(idx)
#         else:
#             junctions_in_list1[junction] = [idx]

#     for idx, junction in enumerate(list2):
#         if junction in junctions_in_list1.keys():
#             if junction in common_junctions.keys():
#                 common_junctions[junction][1].append(idx)
#             else:
#                 common_junctions[junction] = [junctions_in_list1[junction], [idx]]
    
#     return common_junctions

def get_common_junctions(list1, list2):
    return (set(list1) & set(list2))

def get_crossover_point(parent1 : List[int], parent2 : List[int]):
    common_junctions = get_common_junctions(parent1, parent2)

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

def singlepoint_crossover(parent1 : List[int], parent2 : List[int]):
    (idx1, idx2) = get_crossover_point(parent1, parent2)

    return parent2[:idx2] + parent1[idx1:]


# sum = 0

# for i in range(0, 100):
#     list1 = [random.randint(0,1000) for i in range(0, random.randint(10000, 100000))]
#     list2 = [random.randint(0,1000) for i in range(0, random.randint(10000, 100000))]

#     start = time.time()
#     singlepoint_crossover(list1, list2)
#     end = time.time()

#     sum += (end - start)

# print(sum/100)7


print(singlepoint_crossover([1,2,3,4,5,6], [6,4,3,5,7,3]))