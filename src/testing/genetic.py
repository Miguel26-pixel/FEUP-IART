from utils.parser import parse_information
from testing.profiling import profile_solve
from utils.draw import draw_graph
from utils.genetic import greedy_solve
from utils.crossover import SA_crossover
import kernprof
import line_profiler

router = parse_information('../files/input2.txt')
# print(router.graph.junctions[1].coords)
streets = len(router.graph.streets)
print("done!")
print(profile_solve(lambda : greedy_solve(router, streets * 2, router.time_itinerary * 1.2) ,10))
print("done!")


# draw_graph(router.graph)
