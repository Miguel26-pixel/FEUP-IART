import math
from time import time
from utils.parser import parse_information
from utils.draw import draw_graph
from utils.crossover import SA_crossover, order_crossover, SA_crossover_reversed, singlepoint_crossover
from utils.genetic import greedy_solve, random_solve
from utils.solution import check_solution
from testing.profiling import function_time
from meta.genetic import GeneticSolver
import matplotlib.pyplot as plt
import cython

if cython.compiled:
    print("hey")


# best=0
router = parse_information('../files/input2.txt')
print(len(router.graph.junctions))
# while(True):
#     sol = random_solve(router, len(router.graph.streets) * 2, router.time_itinerary*1.2)
#     _, val = check_solution(router, sol)

#     if val > best:
#         best = val
#         print(best)

# dist = [[math.inf for v in range(len(router.graph.junctions))] for u in range(len(router.graph.junctions))]

# for street in router.graph.streets:
#     dist[street.initial.id][street.final.id] = street.time / street.length

#     if street.bidirectional:
#         dist[street.final.id][street.initial.id] = street.time/ street.length

# for junction in router.graph.junctions:
#     dist[junction.id][junction.id] = 0

# for k in range(len(router.graph.junctions)):
#     print(k)
#     for i in range(len(router.graph.junctions)):
#         for j in range(len(router.graph.junctions)):
#             if dist[i][j] > dist[i][k] + dist[k][j]:
#                 dist[i][j] = dist[i][k] + dist[k][j]

its = 50
samples = 4
poll_rate = 100
x_orig = [x for x in range(0, its)]

cum_y = [0 for _ in range(0, its)]
cum_y_worst = [0 for _ in range(0, its)]

for i in range(0, samples):
    solver = GeneticSolver(router, its*poll_rate + 1)
    solver.pop_size = len(router.graph.streets) // router.num_cars // 3
    print( len(router.graph.streets) // router.num_cars // 3)
    solver.mutation_chance = 0.6
    solver.queen_ratio = 0.85
    solver.poll_rate = poll_rate
    solver.crossover_function = [singlepoint_crossover]

    e, _, y, y_worst = solver.solve()
    cum_y = [prev + new for prev, new in zip(cum_y, y)]
    cum_y_worst = [prev + new for prev, new in zip(cum_y_worst, y_worst)]

cum_y = [a / samples for a in cum_y]
cum_y_worst = [a / samples for a in cum_y_worst]

fig, ax = plt.subplots()
x = [a - 0.375/2 for a in x_orig]
ax.bar(x, cum_y, width=0.375, edgecolor="white", linewidth=0.7)
x = [a + 0.375 for a in x]
ax.bar(x, cum_y_worst, width=0.375, edgecolor="white", linewidth=0.7, color="orange")

ax.set(ylim=(max(min(cum_y_worst)-100000, 0), max(cum_y)+100000), xlim=(-0.5, x_orig[-1]+0.5))

plt.xticks([x for x in range(0, its, its//10)])
plt.show()

# a = [10, 9, 8, 2, 1]
# max_a = max(a)
# sum_i = functools.reduce(lambda acc, new: acc + 1/(max_a - new + 1), a, 0)
# sum_l = functools.reduce(lambda acc, new: acc + 1/(math.log(max_a - new + 1,100)+1), a, 0)
# sum_a = sum(a)
# print(sum_i)
# print(sum_l)
# print(sum_a)
# eval_i = [1/(max_a - i + 1)/sum_i  for i in a]
# eval_l = [1/(math.log(max_a - i + 1,100)+1)/sum_l for i in a]
# eval_a = [i/sum_a for i in a]
# print(eval_i)
# print(eval_l)
# print(eval_a)
# print(sum(eval_i))
# print(sum(eval_l))
# print(sum(eval_a))


# sol = greedy_solve(router, 100000, router.time_itinerary * 1.2)

# print(function_time(lambda : check_solution(router, sol), 10) * 200)
