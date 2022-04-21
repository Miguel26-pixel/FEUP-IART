import functools
import math
from time import time
from utils.parser import parse_information
from utils.draw import draw_graph
from utils.genetic import greedy_solve, random_solve
from utils.solution import check_solution
from testing.profiling import function_time
from meta.genetic import GeneticSolver
import matplotlib.pyplot as plt



# best=0
router = parse_information('../files/input2.txt')

# while(True):
#     sol = random_solve(router, len(router.graph.streets) * 2, router.time_itinerary*1.2)
#     _, val = check_solution(router, sol)

#     if val > best:
#         best = val
#         print(best)

solver = GeneticSolver(router, 60)
solver.pop_size = len(router.graph.streets) // router.num_cars
solver.mutation_chance = 0.35
solver.queen_ratio = 0.8
e, x, y, y_worst = solver.solve()

fig, ax = plt.subplots()
ax.bar(x, y, width=0.5, edgecolor="white", linewidth=0.7)

ax.set(ylim=(min(y), max(y)+1000))

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
