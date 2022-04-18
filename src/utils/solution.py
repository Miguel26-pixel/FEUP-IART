from unicodedata import bidirectional
from .graph import Graph, Junction, Street
from .routing import Router

def check_street(graph,initial,final):
    for i in graph.streets:
        if ((i.initial.id == initial and i.final.id == final) or i.bidirectional == True):
            return i.length, i.time, i
    
    return None


def check_solution(router, sol):
    number_cars = len(sol)
    total_length = 0
    if (number_cars != router.num_cars) :
        return False, total_length

    for i in range(number_cars):
        total_time = 0
        number_of_junctions = len(sol[i])

        first_junction = sol[i][0]
        
        if (first_junction != router.initial_junction):
            return False, total_length

        if (number_of_junctions == 1):
            continue

        for j in range(number_of_junctions-1):

            fj = sol[i][j]
            k = j + 1
            sj = sol[i][k]

            if (check_street(router.graph,fj,sj) == None):
                return False, total_length

            length, time, street = check_street(router.graph,fj,sj)

            total_time += time
            
            if  not street.visited :
                temp_length += length
                street.visited = True

            total_length += length
        
            if (total_time > router.time_itinerary):
                break

            if  not street.visited :
                street.visited = True

    
    return True, total_length



#def score_solution(graph,sol):

