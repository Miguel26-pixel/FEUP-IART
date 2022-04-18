from unicodedata import bidirectional
from .graph import Graph, Junction, Street
from .routing import Router

def check_street(graph,initial,final):
    for i in graph.streets:
        if ((i.initial.id == initial and i.final.id == final) or i.bidirectional == True):
            return i.length, i.time, i
    
    return None


def check_solution(router, sol):
    number_cars = sol[0]
    total_length = 0
    if (number_cars != router.num_cars) :
        return False, total_length
    i = 1
    for _ in range(number_cars):
        total_time = 0
        temp_length = 0
        number_of_junctions = sol[i]
        i += 1
        first_junction = sol[i]
        
        if (first_junction != router.initial_junction):
            return False, total_length

        if (number_of_junctions == 1):
            i += 1
        else: 
            for _ in range(number_of_junctions-1):

                fj = sol[i]
                i += 1
                sj = sol[i]

                if (check_street(router.graph,fj,sj) == None):
                    return False, total_length

                length, time, street = check_street(router.graph,fj,sj)

                total_time += time
                
                if  not street.visited :
                    temp_length += length
                    street.visited = True
        
        if (total_time > router.time_itinerary):
            break
        else :
            total_length += temp_length

    
    return True, total_length



#def score_solution(graph,sol):

