from utils.graph import Graph, Junction, Street
from utils.routing import Router
from utils.solution import check_street
import random
import math

def check_junction(graph,junction):
    for i in graph.junctions:
        if (i.coords == junction.coords):
            return True
    return False

def check_lonely_junction(graph):
    for i in graph.junctions:
        if (len(i.streets) == 0):
            return True
    return False

def get_initial_junction(graph):
    initial_junction = random.randint(0,len(graph.junctions)-1)
    for i in graph.streets:
        if (i.initial == initial_junction or (i.final == initial_junction and i.bidirectional)):
            return initial_junction
    return get_initial_junction(graph)

def create_problem():
    graph = Graph()

    number_of_junctions = random.randint(50,100)
    number_of_cars = random.randint(1,10)
    max_street_time = 0

    for i in range (number_of_junctions):
        
        #coords
        random_x = random()*random.randint(1,200)
        random_y = random()*random.randint(1,200)

        junction = Junction((random_x,random_y),i)

        if not check_junction(graph,junction) :
            graph.add_junction(junction)
        
    while (check_lonely_junction(graph)) :

        random_junction1 = random.randint(0,number_of_junctions-1)
        random_junction2 = random.randint(0,number_of_junctions-1)

        if (check_street(graph,random_junction1,random_junction2) == None):

            length_x1,length_y1 = graph.junctions[random_junction1].coords
            length_x2,length_y2 = graph.junctions[random_junction2].coords
            length = math.sqrt((length_y2-length_y1)**2 + (length_x2-length_x1)**2)

            bidirectional = True if (random()<=0.2) else False

            speed = random.randint(10,120)

            time = length/speed

            if (time > max_street_time):
                max_street_time = time

            graph.add_street(Street(graph.junctions[random_junction1],graph.junctions[random_junction2],length,time,bidirectional))

    max_street_time = max_street_time * random()*10

    initial_junction = get_initial_junction(graph)

    router = Router(max_street_time,number_of_cars,initial_junction,graph)

    return router


        
    




