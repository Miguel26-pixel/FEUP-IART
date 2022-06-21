from utils.parser import parse_information
from testing.profiling import profile_solve, function_time
from utils.draw import draw_graph
from utils.genetic import greedy_solve, random_solve, get_initial_pop
from utils.crossover import SA_crossover
import kernprof
import line_profiler

router = parse_information('../files/input2.txt')
# print(router.graph.junctions[1].coords)
streets = len(router.graph.streets)
print("done!")
# print(profile_solve(lambda : greedy_solve(router, streets * 2, router.time_itinerary * 1.2) ,50))
# print(profile_solve(lambda : random_solve(router, streets * 2, router.time_itinerary * 1.2) ,50))
# print(get_initial_pop(router, 100, 20, streets*2, router.time_itinerary*1.2))
print(function_time(lambda : get_initial_pop(router, 100, 20, streets*2, router.time_itinerary*1.2), 5))
print("done!")


# draw_graph(router.graph)
