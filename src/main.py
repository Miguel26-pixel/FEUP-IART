from utils.parser import parse_information
from utils.draw import draw_graph
from meta.genetic import genetic


router = parse_information('../files/input2.txt')
print(len(router.graph.streets))
genetic(router, 100, 0.4)