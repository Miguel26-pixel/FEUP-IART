from utils.parser import parse_information
from utils.draw import draw_graph
from utils.genetic import greedy_solve
from utils.crossover import SA_crossover
from utils.solution import check_solution

router = parse_information('../files/input2.txt')
sol = greedy_solve(router, 10000, router.time_itinerary*1.2)
print(len(sol[0]))
print(check_solution(router, sol))