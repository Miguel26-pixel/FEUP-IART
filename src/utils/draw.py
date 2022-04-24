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

    ship_top = screen.get_height() - background.get_height()
    ship_left = screen.get_width()/2 - background.get_width()/2
    
    #screen.blit(background,(0,0))
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

