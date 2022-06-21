
from abc import ABC, abstractmethod
from typing import List

from model.piece import Piece


class RewardSystem(ABC):
    @abstractmethod
    def invalid_move():
        pass


class SimpleRewardSystem(RewardSystem):

    @abstractmethod
    def score(self, is_winner: bool, groups: List[List[Piece]]) -> float:
        pass


class BiggerGroupRewardSystem(SimpleRewardSystem):
    def score(self, is_winner: bool, groups: List[List[Piece]]) -> float:
        if (is_winner):
            reward = 10 * max(map(lambda x: len(x), groups))
        else:
            reward = 1 if is_winner != None else 5
        return reward

    def invalid_move(self) -> float:
        return -10


class UniColoredRewardSystem(RewardSystem):

    @abstractmethod
    def score(self, is_winner: bool, groups: List[List[Piece]], score_diff: int) -> float:
        pass


class BiggestDiffUniColoredRewardSystem(UniColoredRewardSystem):
    def score(self, is_winner: bool, groups: List[List[Piece]], score_diff: int) -> float:
        if (is_winner):
            reward = 10 * score_diff
        else:
            reward = -1 if is_winner != None else 0
        return reward

    def invalid_move(self) -> float:
        return -1000
