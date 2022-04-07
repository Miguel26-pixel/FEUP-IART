from utils import graph
from utils.crossover import singlepoint_crossover, SA_crossover
from .profiling import best_of_profillings

network = graph.Graph()

junction1 = graph.Junction((0,0))
junction2 = graph.Junction((1,1))
junction3 = graph.Junction((2,2))
junction4 = graph.Junction((3,3))
junction5 = graph.Junction((4,4))
junction6 = graph.Junction((5,5))
junction7 = graph.Junction((6,6))
junction8 = graph.Junction((7,7))

network.junctions = [junction1, junction2, junction3, junction4, junction5, junction6, junction7, junction8]

network.add_street(0, 1, 1, 1, True)
network.add_street(0, 2, 1, 1, False)
network.add_street(2, 4, 1, 1, False)
network.add_street(3, 4, 1, 1, False)
network.add_street(4, 5, 1, 1, False)
network.add_street(5, 6, 1, 1, False)
network.add_street(5, 7, 1, 1, False)
network.add_street(7, 6, 1, 1, True)

print(SA_crossover([0, 1, 3], [0,2,4,5,6], network))
# print(singlepoint_crossover([1,2,3,4,5,6], [1,7,8,4,9,10]))
# print(best_of_profillings(singlepoint_crossover, 20))
