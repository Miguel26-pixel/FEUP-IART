from utils.parser import parse_information
from utils.draw import draw_graph
from meta.genetic import GeneticSolver


router = parse_information('../files/input2.txt')
solver = GeneticSolver(router, 2)

solver.solve()
