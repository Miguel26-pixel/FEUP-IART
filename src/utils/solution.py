from typing import List
from utils.graph import Graph, Junction, Street
from utils.routing import Router


def check_street(graph: Graph, initial, final):
    for street in graph.junctions[initial].streets:
        if (street.initial.id == final or street.final.id == final):
            return street

    return None


def check_single_car(router: Router, car: List[int]):
    total_length = 0

    number_of_junctions = len(car)

    if len(number_of_junctions) == 0:
        return 0

    first_junction = car[0]

    if (first_junction != router.initial_junction):
        return 0

    if (number_of_junctions == 1):
        return 0

    for j in range(number_of_junctions-1):
        fj = car[j]
        k = j + 1
        sj = car[k]

        street = check_street(router.graph, fj, sj)

        if (street == None):
            break

        if not street.visited:
            total_length += street.length
            street.visited = True

    return total_length


def check_solution(router: Router, sol: List[List[int]]):
    number_cars = len(sol)
    total_length = 0
    router.graph.reset_streets()

    if (number_cars != router.num_cars):
        return False, total_length
    for i in range(number_cars):
        total_time = 0
        number_of_junctions = len(sol[i])

        if len(sol[i]) == 0:
            continue
        first_junction = sol[i][0]

        if (first_junction != router.initial_junction):
            break

        if (number_of_junctions == 1):
            continue

        for j in range(number_of_junctions-1):
            fj = sol[i][j]
            k = j + 1
            sj = sol[i][k]

            street = check_street(router.graph, fj, sj)

            if (street == None):
                break

            total_time += street.time

            if (total_time > router.time_itinerary):
                break

            if not street.visited:
                total_length += street.length
                street.visited = True

    return True, total_length
