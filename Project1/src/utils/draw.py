from typing import List
from prettytable import PrettyTable
import pygame
from math import pi
from utils.graph import Graph, Junction, Street
from utils.solution import check_solution, check_street, check_single_car
from utils.routing import Router

def write_output(solution: List[List[int]], router : Router, file):
    file.write(f"{len(solution)}\n")
    for car in solution:
        time_accum = 0
        past_junct = car[0]

        for idx in range(1, len(car)):
            junct = car[idx]
            time_accum += check_street(router.graph, past_junct, junct).time
            past_junct = junct

            if time_accum > router.time_itinerary:
                car = car[:idx]
                break

        file.write(f"{len(car)}\n")
        for junct in car:
            file.write(f"{junct}\n")

def print_annealing(iteration, time, score, curr_score):
    x = PrettyTable()
    x.field_names = ["Iteration", "Score", "Iteration score", "Elapsed Time"]
    x.add_row([iteration, score, curr_score, int(round(time, 0))])
    print(x)


def print_genetic(iteration, time, score):
    x = PrettyTable()
    x.field_names = ["Iteration", "Score", "Elapsed Time"]
    x.add_row([iteration, score, int(round(time, 0))])
    print(x)


def draw_graph(graph):

    pygame.init()

    # Define the colors we will use in RGB format
    BLACK = (0,   0,   0)
    WHITE = (255, 255, 255)
    BLUE = (0,   0, 255)
    GREEN = (0, 255,   0)
    RED = (255,   0,   0)
    background = pygame.image.load("images/image.jpg")
    street_image = pygame.image.load("images/road.png")

    size = [1000, 600]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("IA City")

    #pygame.transform.scale(screen,(1,1))
    
    #Loop until the user clicks the close button.
    done = False
    clock = pygame.time.Clock()

    junctions = graph.junctions

    clock.tick(10)

    screen.fill(WHITE)
    pygame.display.update()

    for junction in junctions :
        pygame.draw.circle(screen, BLUE, list(junction.coords), 10)
        pygame.display.update()
        for street in junction.streets:
            pygame.draw.line(screen,BLACK,street.initial.coords,street.final.coords, 2)

    

    pygame.display.flip()
    #pygame.transform.scale(screen,(1,1))
    
    # Be IDLE friendly
    while not done:
        continue

    pygame.quit()
