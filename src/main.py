from utils.parser import parse_information
from utils.draw import draw_graph


router = parse_information('../files/input.txt')
print(router.graph.junctions[1].coords)
draw_graph(router.graph)
