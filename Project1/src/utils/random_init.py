from utils.graph import Graph, Junction, Street
from utils.routing import Router
from utils.solution import check_street
import random
import math

def check_junction(graph,junction):
    for i in graph.junctions:
        if (i.coords == junction.coords or (i.coords[0] - 10 <= junction.coords[0] <= i.coords[0] + 10) or (i.coords[1] - 10 <= junction.coords[1] <= i.coords[1] + 10)):
            return True
    return False

def check_lonely_junction(graph):
    for i in graph.junctions:
        if (len(i.streets) == 0):
            return True
    return False

def get_initial_junction(graph):
    return random.randint(0,len(graph.junctions)-1)

def create_problem():
    graph = Graph()

    number_of_junctions = random.randint(50,100)
    number_of_cars = random.randint(1,10)
    max_street_time = 0

    for i in range (number_of_junctions):
        
        #coords
        random_x = random.random()*random.randint(60,1000)
        random_y = random.random()*random.randint(120,600)

        junction = Junction((random_x,random_y),i)

        if not check_junction(graph,junction) :
            graph.add_junction((random_x,random_y))
    
    number_of_junctions = len(graph.junctions)
        
    while (check_lonely_junction(graph)) :

        random_junction1 = random.randint(0,number_of_junctions-1)
        random_junction2 = random.randint(0,number_of_junctions-1)

        if random_junction1 == random_junction2:
            continue

        if (check_street(graph,random_junction1,random_junction2) == None):
            (length_x1,length_y1) = graph.junctions[random_junction1].coords
            (length_x2,length_y2) = graph.junctions[random_junction2].coords
            length = math.sqrt((length_y2-length_y1)**2 + (length_x2-length_x1)**2)

            bidirectional = random.random()<=0.2

            speed = random.randint(10,120)

            time = length/speed

            if (time > max_street_time):
                max_street_time = time

            graph.add_street(graph.junctions[random_junction1].id,graph.junctions[random_junction2].id,length,time,bidirectional)

    max_street_time = max_street_time * random.random()*10

    initial_junction = get_initial_junction(graph)

    router = Router(max_street_time,number_of_cars,initial_junction,graph)

    return router


        
    




