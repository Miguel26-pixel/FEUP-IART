from abc import ABC, abstractmethod
import math
import random
from time import sleep
from typing import List
import gym
import numpy as np
from model.board import Board
from model.gym import SplinterEnv
from model.position import Position, Transformation
from model.qtable import QTable
from model.state import State, StateFactory


class Learner(ABC):
    def __init__(self, env: gym.Env, board: Board, action_factory: StateFactory) -> None:
        super().__init__()

        self.board = board
        self.env = env
        self.action_factory = action_factory
        self._board_dict = {}
        self._max_dict = 0

        grid_size = board.horizontal_size * board.vertical_size
        action_size = action_factory.state_size() * grid_size

        self._q_table = QTable(action_size)

    def is_invalid_move(self, action):
        pure_action = self.parse_action(action)
        result = not self.env.game_controller.check_valid_move(pure_action)[
            0]
        return result

    def choose_method(self, state, epsilon):
        exp_exp_tradeoff = random.uniform(0, 1)

        if exp_exp_tradeoff > epsilon:
            actions_scores = self._q_table.get_state(state)
            invalid_moves = [x for x in range(
                actions_scores.size) if self.is_invalid_move(x)]
            mask = np.zeros(actions_scores.size, dtype=bool)
            mask[invalid_moves] = True
            return np.argmax(
                np.ma.array(actions_scores, mask=mask))
        
        return self.env.action_space.sample()

    def parse_state(self, state: Board) -> int:
        key = str(state.board)
        result = self._board_dict.get(key)

        if (result == None):
            self._board_dict.update({key: self._max_dict})
            result = self._max_dict
            self._max_dict += 1
        return result

    def parse_action(self, action: int) -> Transformation:
        actions_size = self.action_factory.state_size()
        piece_idx = action // actions_size
        x, y = piece_idx % self.board.horizontal_size, piece_idx // self.board.horizontal_size
        move_idx = action % actions_size

        position = Position(x, y)
        move = self.action_factory.build(move_idx)

        return move.get_move(position)

    @abstractmethod
    def train(self):
        pass

    def run(self):
        for episode in range(5):
            pure_state = self.env.reset()
            state = self.parse_state(pure_state)

            step = 0
            done = False
            print("\n\n\n****************************************************")
            print("****************************************************")
            print("****************************************************")
            print("EPISODE ", episode + 1)

            episode_reward = 0

            for step in range(20):
                # Take the action (index) that have the maximum expected future reward given that state
                self.env.render()
                action = self.choose_method(state, 0)
                pure_action = self.parse_action(action)
                print("ACTION TAKEN:", pure_action)

                new_pure_state, reward, done, info = self.env.step(
                    pure_action, 0)

                episode_reward += reward

                if done:
                    break
                state = self.parse_state(new_pure_state)
                sleep(2)
            print("\nEPISODE REWARD", episode_reward)
            print("STEPS TAKEN", step + 1)

            self.env.render()
            sleep(5)
        self.env.close()


class QLearner(Learner):
    def __init__(self,  env: SplinterEnv, board: Board, action_factory: StateFactory) -> None:
        super().__init__(env, board, action_factory)

    def train(self):
        total_episodes = 30000    # Total episodes
        max_steps = 20                # Max steps per episode

        learning_rate = 1           # Learning rate
        gamma = 0.95                  # Discounting rate

        # Exploration parameters
        epsilon = 1.0                 # Exploration rate
        max_epsilon = 1.0             # Exploration probability at start
        min_epsilon = 0.01            # Minimum exploration probability
        decay_rate = 0.000035

        # List of rewards
        rewards = []

        # For life or until learning is stopped
        for episode in range(total_episodes):
            print("Episode:", episode+1)
            # Reset the environment
            pure_state = self.env.reset()
            state = self.parse_state(pure_state)

            step = 0
            player = 0
            done = False
            total_rewards = 0

            for step in range(max_steps):
                action = self.choose_method(state, epsilon)                

                pure_action = self.parse_action(action)

                new_pure_state, reward, done, info = self.env.step(
                    pure_action, player)

                new_state = self.parse_state(new_pure_state)

                # Update Q(s,a):= Q(s,a) + lr [R(s,a) + gamma * max Q(s',a') - Q(s,a)]
                # qtable[new_state, :] : all the actions we can take from new state

                best_new_action = np.max(self._q_table.get_state(new_state))
                current_action = self._q_table.get(state, action)
                new_value = current_action + learning_rate * (
                    reward + gamma * best_new_action - current_action)

                self._q_table.update(state, action, new_value)

                # self.__q_table[state, action] = self.__q_table[state, action] + learning_rate * \
                #     (reward + gamma *
                #      np.max(self.__q_table[new_state, :]) - self.__q_table[state, action])

                total_rewards = total_rewards + reward

                # Our new state is state
                state = new_state

                # If done (if we're dead) : finish episode
                if done == True:
                    break

            # reduce epsilon (because we need less and less exploration)
            epsilon = min_epsilon + \
                (max_epsilon - min_epsilon)*np.exp(-decay_rate*episode)
            print(epsilon)

            rewards.append(total_rewards)

        print("Score/time: " + str(sum(rewards)/total_episodes))
        print(self._q_table.get_q_table())
        print(epsilon)

        self.env.reset()


class SARSALearner(Learner):
    def __init__(self,  env: SplinterEnv, board: Board, action_factory: StateFactory) -> None:
        super().__init__(env, board, action_factory)

    def train(self):
        total_episodes = 10000    # Total episodes
        max_steps = 20                # Max steps per episode

        learning_rate = 1           # Learning rate
        gamma = 0.95                  # Discounting rate

        # Exploration parameters
        epsilon = 1.0                 # Exploration rate
        max_epsilon = 1.0             # Exploration probability at start
        min_epsilon = 0.01            # Minimum exploration probability
        decay_rate = 0.000035

        # List of rewards
        rewards = []

        # For life or until learning is stopped
        for episode in range(total_episodes):
            print("Episode:", episode+1)
            # Reset the environment
            pure_state = self.env.reset()
            state = self.parse_state(pure_state)
            action1 = self.choose_method(state, epsilon)

            step = 0
            player = 0
            done = False
            total_rewards = 0

            for step in range(max_steps):
                pure_action = self.parse_action(action1)

                new_pure_state, reward, done, info = self.env.step(
                    pure_action, player)

                new_state = self.parse_state(new_pure_state)

                action2 = self.choose_method(new_state, epsilon)

                best_new_action = self._q_table.get(new_state, action2)
                current_action = self._q_table.get(state, action1)
                new_value = current_action + learning_rate * (
                    reward + gamma * best_new_action - current_action)

                self._q_table.update(state, action1, new_value)

                total_rewards = total_rewards + reward

                # Our new state is state
                state = new_state
                action1 = action2

                if done == True:
                    break

            # reduce epsilon (because we need less and less exploration)
            epsilon = min_epsilon + \
                (max_epsilon - min_epsilon)*np.exp(-decay_rate*episode)
            print(epsilon)

            rewards.append(total_rewards)

        print(self._q_table.get_q_table())

        self.env.reset()
