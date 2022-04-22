import math
from algorithm.annealing import simulated_annealing
from testing.test_dijkstra import test_multiple
from utils.neighbourhood import neighbour_multiple_cars, neighbour_single_car
from utils.parser import parse_information
from utils.draw import draw_graph
from utils.genetic import greedy_solve
from utils.crossover import SA_crossover
from utils.solution import check_solution

router = parse_information('../files/input2.txt')

curr_best = 0

print("GENERATING SOLUTION")

for x in range(100):
    sol = greedy_solve(router, len(router.graph.streets) * 2,
                       router.time_itinerary*1.2)
    score = check_solution(router, sol)[1]
    print(x, score)
    if score > curr_best:
        curr_best = score
        curr_sol = sol

print("END GENERATING SOLUTION")

print(router.num_cars)
print(check_solution(router, curr_sol))


ALPHA = 1.5

TEMP_VARIATION = [
    lambda initial, i: initial / (1 + math.log(1 + i)),
    lambda initial, i: initial / (1 + ALPHA * math.log(1 + i)),
    lambda initial, i: initial / (1 + ALPHA * math.log(1 + math.pow(i, 2))),
]


final_sol = simulated_annealing(
    router, 10000, 10000, TEMP_VARIATION[2], neighbour_single_car, 1, curr_sol)


print(check_solution(router, final_sol))
