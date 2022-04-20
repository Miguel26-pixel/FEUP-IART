from utils.parser import parse_information
from utils.draw import draw_graph
from utils.genetic import greedy_solve, normalize_solutions, selection_ga
from utils.crossover import SA_crossover
from utils.solution import check_solution

print(selection_ga([1,2,3,4,5], [12,23,2,25,13]))

