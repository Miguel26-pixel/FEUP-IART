from src.utils.parser import parse_information
from src.utils.draw import draw_graph
from src.utils.solution import check_solution
from src.utils.random_init import create_problem


if __name__ == "__main__":
    #router = parse_information("files/input2.txt")
    router = create_problem()
    #print(router.graph.junctions[1].coords)
    draw_graph(router.graph)
    #print(check_solution(router,[[0],[0,1,2]]))
