import gym
from controller.game_controller import GameController
from model.board import Board
from model.position import Transformation
from model.state import StateFactory
from view.BoardViewer import BoardViewer


class SplinterEnv(gym.Env):
    def __init__(self, board: Board, game_controller: GameController, action_factory: StateFactory, board_viewer : BoardViewer):
        self.action_space = gym.spaces.Discrete(
            action_factory.state_size() *
            board.horizontal_size *
            board.vertical_size)
        # self.observation_space = gym.spaces.Discrete(2)
        self.board = board
        self.game_controller = game_controller
        self.action_factory = action_factory
        self.board_viewer = board_viewer

    def step(self, action: Transformation, player: int):
        valid, penalty = self.game_controller.check_valid_move(action)
        if (not valid):
            return self.board, penalty, True, {}

        self.game_controller.move(action)

        # groups_size, groups, pieces_group = self.game_controller.get_groups()

        # # Bug where if you play a piece directly outside, no end detection
        # if (groups_size > 1):
        #     is_winner = self.game_controller.winner(
        #         action, groups, pieces_group)

        #     if (is_winner):
        #         # Better score if bigger group
        #         reward = 10 * max(map(lambda x: len(x), groups))
        #     else:
        #         reward = 1 if is_winner != None else 5
        #     done = True

        done, reward = self.game_controller.check_end_game(action)

        player = (player + 1) % 2

        return self.board, reward, done, {"player": player}

    def render(self):
        self.board_viewer.render(self.board)
        print(self.board)

    def reset(self):
        self.last_obs = self.board.copy()
        return self.board.reset()
