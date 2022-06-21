import os
import pygame
from model.board import SimpleBoardBuilder, Board, OriginalBoardBuilder, UniColoredBoardBuilder
from view.BoardViewer import BoardViewer
from view.menu import main_menu
import math
import gym
from controller.ai_controller import Learner, QLearner, SARSALearner
from controller.game_controller import GameController, SimpleGameController, SimpleRewardSystem, UniColoredGameController
from controller.reward_system import BiggerGroupRewardSystem, BiggestDiffUniColoredRewardSystem
from model.board import OriginalBoardBuilder, Board, SimpleBoardBuilder, UniColoredBoardBuilder
from model.gym import SplinterEnv
from model.position import Direction, Position, Transformation
from model.state import LeftDown, Right, StateFactory, Up


def test_game_1():
    board: Board = OriginalBoardBuilder(5, 2).build()
    print(board)

    game_controller: GameController = GameController(board, True)

    game_controller.move(Position(2, 3), Direction(0, -1))
    game_controller.move(Position(2, 2), Direction(0, -1))
    game_controller.move(Position(2, 1), Direction(0, -1))
    game_controller.move(Position(6, 7), Direction(1, 1))
    game_controller.move(Position(5, 7), Direction(1, 1))
    print(board)
    print(game_controller.get_groups())


def test_game_2():
    board: Board = SimpleBoardBuilder(3, 3, 1).build()
    print(board)

    game_controller: GameController = GameController(board, True)

    game_controller.move(Up().get_move(Position(2, 3)))
    game_controller.move(Up().get_move(Position(2, 2)))
    game_controller.move(Up().get_move(Position(2, 1)))
    print(board)
    print(game_controller.get_groups())


def test_game_3():
    board: Board = SimpleBoardBuilder(3, 2, 1).build()
    print(board)

    game_controller: GameController = GameController(board, True)

    game_controller.move(LeftDown().get_move(Position(2, 1)))
    game_controller.move(Right().get_move(Position(3, 1)))
    print(board)
    print(game_controller.get_groups())


def test_game_4(horizontal, vertical, gap):
    board: Board = UniColoredBoardBuilder(horizontal, vertical, gap).build()
    print(board)


def test_parser():
    move_factory = StateFactory()
    board: Board = SimpleBoardBuilder(2, 2, 0).build()
    game_controller: GameController = GameController(board, True)
    print(board)

    learner: Learner = QLearner(board, move_factory)

    print("0 :", learner.parse_action(0))
    print("1 :", learner.parse_action(1))
    print("10:", learner.parse_action(10))
    print("20:", learner.parse_action(20))
    print("25:", learner.parse_action(25))


def num_states():
    sum = 0
    HORIZONTAL = 5
    VERTICAL = 4
    GAP = 2
    SPACES = (HORIZONTAL + GAP * 2) * (VERTICAL + GAP * 2)
    PIECES_1 = (HORIZONTAL) * (VERTICAL)
    PIECES_2 = PIECES_1 - 2
    KINGS = 2

    for i in range(PIECES_1 + 1):  # 5 pieces, 6 spaces
        sum += math.comb(SPACES, i)

    print(sum)
    sum = 0

    for i in range(PIECES_2 + 1):  # 3 pieces, 2 kings, 6 spaces
        temp = math.comb(SPACES, i)
        inner_sum = 0
        for r in range(KINGS + 1):
            inner_sum += math.comb(SPACES-i, r)
        sum += temp * inner_sum

    print(sum)

    test_game_4(HORIZONTAL, VERTICAL, GAP)


if __name__ == '__main__':

    # Game Initialization
    pygame.init()
 
    # Center the Game Application
    os.environ['SDL_VIDEO_CENTERED'] = '1'
 
    # Game Resolution
    screen_width=800
    screen_height=600

    screen = pygame.display.set_mode((screen_width, screen_height))

    main_menu(screen,screen_width,screen_height)
    pygame.quit()
    quit()



    # player = 0

    # while 1:
    #     print("Player:", player)

    #     try:
    #         position = Position(
    #             *map(int, input("Input position x y: ").split()))
    #         raw_m = input(
    #             "Input move: q,w,e,a,d,z,x,c from top left to right down: ")
    #         move_generator = move_factory.build(raw_m)
    #     except TypeError:
    #         continue

    #     move = move_generator.get_move(position)
    #     if (not game_controller.move(move)):
    #         continue

    #     print(board)

    #     (game_controller.check_end_game(move))

    #     player = (player + 1) % 2

