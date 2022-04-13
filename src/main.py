from utils.parser import parse_information
from utils.draw import draw_graph
from utils.genetic import greedy_solve


router = parse_information('../files/input2.txt')
# print(router.graph.junctions[1].coords)
print(greedy_solve(router))
# draw_graph(router.graph)
