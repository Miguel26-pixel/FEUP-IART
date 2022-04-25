from prettytable import PrettyTable
import pygame
from math import pi
from .graph import Graph, Junction, Street
from .routing import Router


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

    size = [600, 600]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Example code for the draw module")

    # Loop until the user clicks the close button.
    done = False
    clock = pygame.time.Clock()

    junctions = graph.junctions

    clock.tick(10)

    screen.fill(WHITE)

    for junction in junctions:
        pygame.draw.circle(screen, BLUE, list(junction.coords), 1)

    pygame.display.flip()

    # Be IDLE friendly
    while not done:
        continue

    pygame.quit()
