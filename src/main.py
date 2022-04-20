from time import time
from utils.parser import parse_information
from utils.draw import draw_graph
from utils.genetic import greedy_solve
from utils.solution import check_solution
from testing.profiling import function_time
from meta.genetic import GeneticSolver


router = parse_information('../files/input2.txt')
solver = GeneticSolver(router, 600)
solver.pop_size = len(router.graph.streets) // router.num_cars // 4
solver.mutation_chance = 0.3
solver.queen_ratio = 0.8
print(solver.solve())


# sol = greedy_solve(router, 100000, router.time_itinerary * 1.2)

# print(function_time(lambda : check_solution(router, sol), 10) * 200)