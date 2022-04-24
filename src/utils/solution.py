from .graph import Graph
from .routing import Router

def check_street(graph: Graph,initial,final):
    for street in graph.streets:
        if ((street.initial.id == initial and street.final.id == final) or (street.final.id == initial and street.initial.id == final)):
            return street
    
    return None


def check_solution(router : Router, sol):
    number_cars = len(sol)
    total_length = 0
    router.graph.reset_streets()

    if (number_cars != router.num_cars) :
        return False, total_length

    for i in range(number_cars):
        total_time = 0
        number_of_junctions = len(sol[i])

        first_junction = sol[i][0]
        
        if (first_junction != router.initial_junction):
            break

        if (number_of_junctions == 1):
            continue

        for j in range(number_of_junctions-1):
            fj = sol[i][j]
            k = j + 1
            sj = sol[i][k]

            street = check_street(router.graph,fj,sj) 
            
            if (street == None):
                break

            total_time += street.time
        
            if (total_time > router.time_itinerary):
                break

            if  not street.visited :
                total_length += street.length
                street.visited = True

    
    return True, total_length
