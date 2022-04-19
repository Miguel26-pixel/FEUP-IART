from utils import graph
from utils.crossover import singlepoint_crossover, SA_crossover, order_crossover, crossover
from testing.profiling import profile_crossover
import kernprof
import line_profiler

# SA_crossover = profile(SA_crossover)

network = graph.Graph()

network.add_junction((0, 0))
network.add_junction((1, 1))
network.add_junction((2, 2))
network.add_junction((3, 3))
network.add_junction((4, 4))
network.add_junction((5, 4))
network.add_junction((6, 4))
network.add_junction((7, 4))

network.add_street(0, 1, 1, 1, True)
network.add_street(0, 2, 1, 1, False)
network.add_street(2, 4, 1, 1, False)
network.add_street(3, 4, 1, 1, False)
network.add_street(4, 5, 1, 1, False)
network.add_street(5, 6, 1, 1, False)
network.add_street(5, 7, 1, 1, False)
network.add_street(7, 6, 1, 1, True)


print(crossover([[0,2,4,5,6],[0,2,4,5,6]], [[0, 1, 3], [0, 1, 3]], network, SA_crossover))


# print(SA_crossover([0,2,4,5,6], [0, 1, 3], network))
#print(order_crossover([0,2,4,5,6], [1,3,7,8], network))
#print(singlepoint_crossover([1,2,3,4,5,6], [1,7,8,4,9,10], None))
# print(profile_crossover(singlepoint_crossover, 100000, 80000, 20))
#print(profile_crossover(SA_crossover, 100000, 80000, 20))
