from abc import ABC, abstractmethod
from model.position import Transformation, Position, Direction


class State(ABC):

    @abstractmethod
    def get_move(self, position: Position) -> Transformation:
        pass


class StateFactory():
    def state_size(self):
        return 8

    def build(self, move) -> State:
        if move == 'q' or move == 0:
            return LeftUp()
        if move == 'w' or move == 1:
            return Up()
        if move == 'e' or move == 2:
            return RightUp()
        if move == 'a' or move == 3:
            return Left()
        if move == 'd' or move == 4:
            return Right()
        if move == 'z' or move == 5:
            return LeftDown()
        if move == 'x' or move == 6:
            return Down()
        if move == 'c' or move == 7:
            return RightDown()
        raise TypeError(f"Invalid Move: {move}")


class LeftUp(State):
    def get_move(self, position: Position):
        return Transformation(position, Direction(-1, -1))


class Up(State):
    def get_move(self, position: Position):
        return Transformation(position, Direction(0, -1))


class RightUp(State):
    def get_move(self, position: Position):
        return Transformation(position, Direction(1, -1))


class Left(State):
    def get_move(self, position: Position):
        return Transformation(position, Direction(-1, 0))


class Right(State):
    def get_move(self, position: Position):
        return Transformation(position, Direction(1, 0))


class LeftDown(State):
    def get_move(self, position: Position):
        return Transformation(position, Direction(-1, 1))


class Down(State):
    def get_move(self, position: Position):
        return Transformation(position, Direction(0, 1))


class RightDown(State):
    def get_move(self, position: Position):
        return Transformation(position, Direction(1, 1))
