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

def singlepoint_crossover(parent1 : List[int], parent2 : List[int]):
    return get_common_junctions(parent1, parent2)


sum = 0

for i in range(0, 100):
    list1 = [random.randint(0,1000) for i in range(0, random.randint(10000, 100000))]
    list2 = [random.randint(0,1000) for i in range(0, random.randint(10000, 100000))]

    start = time.time()
    get_common_junctions2(list1, list2)
    end = time.time()

    sum += (end - start)

print(sum/100)


# print(singlepoint_crossover([1,2,1], [3,1,1]))