from src.utils.parser import parse_information
from src.utils.draw import draw_graph


if __name__ == "__main__":
    router = parse_information()
    print(router.graph.junctions[1].coords)
    draw_graph(router.graph)
    