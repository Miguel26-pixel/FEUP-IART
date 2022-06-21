import gym
import pygame
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from pygame.locals import *
import os, sys
from controller.ai_controller import Learner, QLearner, SARSALearner
from controller.game_controller import GameController, UniColoredGameController
from controller.reward_system import BiggestDiffUniColoredRewardSystem, SimpleRewardSystem
from model.board import UniColoredBoardBuilder
from model.gym import SplinterEnv
from model.state import StateFactory
from view.BoardViewer import Board, BoardViewer
from view.loading import loading_screen
from threading import Thread


def start_game():

        move_factory = StateFactory()
        board: Board = UniColoredBoardBuilder(3, 4, 1).build()
        reward_system: SimpleRewardSystem = BiggestDiffUniColoredRewardSystem()
        game_controller: GameController = UniColoredGameController(
        board, True, reward_system)
        board_viewer: BoardViewer = BoardViewer(board)
        print(board)

        env: gym.Env = SplinterEnv(board, game_controller, move_factory, board_viewer)

        learner: QLearner = QLearner(env, board, move_factory)

        learner.train()
        app = Ursina()

        thread = Thread(target=learner.run)
        thread.start()
        app.run()
        thread.join()

# Text Renderer
def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(message, 0, textColor)
 
    return newText
 
 
# Colors
white=(255, 255, 255)
black=(0, 0, 0)
gray=(50, 50, 50)
red=(255, 0, 0)
green=(0, 255, 0)
blue=(0, 0, 255)
yellow=(255, 255, 0)
 
# Game Fonts
font = "./view/Bangers-Regular.ttf"
 
 
# Game Framerate
clock = pygame.time.Clock()
FPS=30

# Main Menu
def main_menu(screen,screen_width,screen_height):
 
    menu=True
    selected="start"
 
    while menu:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    selected="start"
                elif event.key==pygame.K_DOWN:
                    selected="quit"
                if event.key==pygame.K_RETURN:
                    if selected=="start":
                        #loading_screen(screen, screen_width, screen_height, clock)
                        pygame.quit()
                        start_game()
                        
                    if selected=="quit":
                        pygame.quit()
                        quit()
 
        # Main Menu UI
        ship = pygame.image.load("./view/black.jpg")
        ship = pygame.transform.scale(ship,(screen_width,screen_height))
        ship_top = screen.get_height() - ship.get_height()
        ship_left = screen.get_width()/2 - ship.get_width()/2

        screen.blit(ship, (ship_top,ship_left))

        title=text_format("SPLINTER", font, 90, yellow)
        if selected=="start":
            text_start=text_format("START", font, 95, black)
        else:
            text_start = text_format("START", font, 75, black)
        if selected=="quit":
            text_quit=text_format("QUIT", font, 95, black)
        else:
            text_quit = text_format("QUIT", font, 75, black)    
 
        title_rect=title.get_rect()
        start_rect=text_start.get_rect()
        quit_rect=text_quit.get_rect()
 
        # Main Menu Text
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80))
        screen.blit(text_start, (screen_width/2 - (start_rect[2]/2), 300))
        screen.blit(text_quit, (screen_width/2 - (quit_rect[2]/2), 390))
        pygame.display.update()
        clock.tick(FPS)
        pygame.display.set_caption("IART - The Splinter")



