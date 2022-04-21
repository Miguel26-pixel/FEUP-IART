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
sol = greedy_solve(router, 10000, router.time_itinerary*1.2)

print(router.num_cars)
print(check_solution(router, sol))


def temp_var(initial, i):
    return initial / (1 + math.log(1 + i))


final_sol = simulated_annealing(
    router, 10000, 10000, temp_var, neighbour_single_car, 1, sol)


print(check_solution(router, final_sol))
