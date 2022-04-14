from src.utils.parser import parse_information
from src.utils.draw import draw_graph
from src.utils.solution import check_solution


if __name__ == "__main__":
    router = parse_information('./files/input.txt')
    #print(router.graph.junctions[1].coords)
    #draw_graph(router.graph)
    print(check_solution(router,[2,1,0,3,0,1,2]))
