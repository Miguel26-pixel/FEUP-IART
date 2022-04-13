import pygame
from math import pi
from .graph import Graph, Junction, Street
from .routing import Router


def draw_graph(graph):

    pygame.init()
    
    # Define the colors we will use in RGB format
    BLACK = (  0,   0,   0)
    WHITE = (255, 255, 255)
    BLUE =  (  0,   0, 255)
    GREEN = (  0, 255,   0)
    RED =   (255,   0,   0)


    size = [600, 600]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Example code for the draw module")
    
    #Loop until the user clicks the close button.
    done = False
    clock = pygame.time.Clock()

    junctions = graph.junctions
    
    clock.tick(10)
    
    screen.fill(WHITE)

    for junction in junctions :
        pygame.draw.circle(screen, BLUE, list(junction.coords), 1)

    pygame.display.flip()
    
    # Be IDLE friendly
    while not done:
        continue

    pygame.quit()

