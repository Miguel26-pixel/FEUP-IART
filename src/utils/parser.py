from .graph import Graph, Junction, Street
from .routing import Router


def parse_information(file_path) :
    graph = Graph()

    f = open(file_path, 'r')

    first_config = f.readline().strip().split(" ")

    number_of_junctions = int(first_config[0])
    number_of_streets = int(first_config[1])
    max_time = int(first_config[2])
    number_of_cars = int(first_config[3])
    start_junction = int(first_config[4])

    for i in range(number_of_junctions):
        junction_config = f.readline().strip().split(" ")
        junction = Junction((float(junction_config[0]),float(junction_config[1])), i)
        graph.junctions.append(junction)

    for i in range(number_of_streets):
        street_config = f.readline().strip().split(" ")
        graph.add_street(int(street_config[0]),int(street_config[1]),int(street_config[4]),int(street_config[3]), False) if int(street_config[2]) == 1 else graph.add_street(int(street_config[0]),int(street_config[1]),int(street_config[4]),int(street_config[3]), True)

    router = Router(max_time, number_of_cars, start_junction, graph)

    return router





