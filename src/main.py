from utils.parser import parse_information
from utils.draw import draw_graph
from meta.genetic import genetic


router = parse_information('../files/input2.txt')
pop_size = len(router.graph.streets) // router.num_cars // 10
genetic(router, 100, pop_size, 0.4, 2)
