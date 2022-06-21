import numpy as np


class QTable:
    def __init__(self, action_size) -> None:
        self.__q_table = np.zeros((0, action_size))
        self.__action_size = action_size
        self.__state_size = 0

    def __init_state(self, state: int):
        diff = state - self.__state_size
        if (diff >= 0):
            self.__state_size += diff + 1
            self.__q_table = np.append(
                self.__q_table, np.zeros((diff + 1, self.__action_size)), axis=0)

    def get_q_table(self):
        return self.__q_table

    def get(self, state: int, action: int):
        self.__init_state(state)
        return self.__q_table[state, action]

    def get_state(self, state: int):
        self.__init_state(state)
        return self.__q_table[state, :]

    def update(self, state: int, action: int, value):
        self.__init_state(state)
        self.__q_table[state, action] = value
