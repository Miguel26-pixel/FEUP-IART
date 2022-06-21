from copy import deepcopy
from typing import List


from model.piece import KingPiece, PawnPiece, Piece
from model.position import Position
import pprint


class Board:
    def __init__(self, horizontal_size: int, vertical_size: int, gap: int, board: List[List[Piece]]) -> None:
        self.horizontal_size: int = horizontal_size + gap * 2
        self.vertical_size: int = vertical_size + gap * 2
        self.board: List[List[Piece]] = board
        self.initial_board: List[List[Piece]] = deepcopy(board)

    def __str__(self) -> str:
        return "\n".join(
            [
                f"Horizontal size: {self.horizontal_size}",
                f"Vertical size: {self.vertical_size}",
                f"------------- Board -------------",
                "",
                pprint.pformat(self.board, width=self.horizontal_size * 4 + 20)
            ]
        )

    def get_cell(self, pos: Position) -> Piece:
        if (not self.is_valid_position(pos)):
            raise ValueError(
                "Invalid position")
        return self.board[pos.y][pos.x]

    def set_cell(self, pos: Position, piece: Piece):
        if (not self.is_valid_position(pos)):
            raise ValueError(
                "Invalid position")

        self.board[pos.y][pos.x] = piece

    def is_valid_position(self, pos: Position):
        return not(pos.x < 0 or pos.x >= self.horizontal_size or pos.y <
                   0 or pos.y >= self.vertical_size)

    def copy(self):
        return Board(self.horizontal_size, self.vertical_size, 0, deepcopy(self.board))

    def reset(self):
        self.board = deepcopy(self.initial_board)
        return self


class SimpleBoardBuilder():
    def __init__(self, horizontal_size: int, vertical_size: int, gap: int) -> None:
        self.horizontal_size: int = horizontal_size
        self.vertical_size: int = vertical_size
        self.gap = gap
        if (horizontal_size < 2):
            raise ValueError(
                "Invalid horizontal_size: must be greater or equal than 2")

    def __init_board(self) -> List[List[Piece]]:

        board = [[None for _x in range(self.horizontal_size + self.gap * 2)]
                 for _y in range(self.gap)]
        for _x in range(self.vertical_size):
            line = [None for _ in range(self.gap)]
            for _y in range(self.horizontal_size):
                line.append(PawnPiece(False))
            print(len(line))
            line.extend([None for _ in range(self.gap)])
            board.append(line)
        board.extend([[None for _ in range(self.horizontal_size + self.gap * 2)]
                     for _ in range(self.gap)])

        return board

    def build(self) -> Board:
        board = self.__init_board()

        return Board(self.horizontal_size, self.vertical_size, self.gap, board)


class OriginalBoardBuilder():
    def __init__(self, horizontal_size: int, gap: int) -> None:
        self.horizontal_size: int = horizontal_size
        self.vertical_size: int = horizontal_size + 1
        self.gap = gap
        if (horizontal_size < 3 or horizontal_size % 2 == 0):
            raise ValueError(
                "Invalid horizontal_size: must be greater or equal than 5 and odd")

    def __is_king(self, index: int) -> bool:
        valid_king_x = self.horizontal_size // 2
        valid_king_first_y = self.vertical_size // 2 - 1
        valid_king_second_y = self.vertical_size // 2
        valid_first_king = valid_king_x + valid_king_first_y * self.horizontal_size
        valid_second_king = valid_king_x + valid_king_second_y * self.horizontal_size

        return index == valid_first_king or index == valid_second_king

    def __init_board(self) -> List[List[Piece]]:
        board = [[None for _ in range(self.horizontal_size + self.gap * 2)]
                 for _ in range(self.gap)]
        for y in range(self.vertical_size):
            line = [None for _ in range(self.gap)]
            for x in range(self.horizontal_size):
                current = x + y * self.horizontal_size
                is_black = current % 2 == 0

                if (self.__is_king(current)):
                    piece = KingPiece(is_black)
                else:
                    piece = PawnPiece(is_black)

                line.append(piece)
            line.extend([None for _ in range(self.gap)])
            board.append(line)
        board.extend([[None for _ in range(self.horizontal_size + self.gap * 2)]
                     for _ in range(self.gap)])

        return board

    def build(self) -> Board:
        board = self.__init_board()

        return Board(self.horizontal_size, self.vertical_size, self.gap, board)


class UniColoredBoardBuilder():
    def __init__(self, horizontal_size: int, vertical_size: int, gap: int) -> None:
        self.horizontal_size: int = horizontal_size
        self.vertical_size: int = vertical_size
        self.gap = gap
        if (horizontal_size < 3 or horizontal_size % 2 == 0):
            raise ValueError(
                "Invalid horizontal_size: must be greater or equal than 5 and odd")

    def __is_king(self, index: int) -> bool:
        valid_king_x = self.horizontal_size // 2
        valid_king_first_y = self.vertical_size // 2 - 1
        valid_king_second_y = self.vertical_size // 2
        valid_first_king = valid_king_x + valid_king_first_y * self.horizontal_size
        valid_second_king = valid_king_x + valid_king_second_y * self.horizontal_size

        return index == valid_first_king or index == valid_second_king

    def __init_board(self) -> List[List[Piece]]:
        board = [[None for _ in range(self.horizontal_size + self.gap * 2)]
                 for _ in range(self.gap)]
        for y in range(self.vertical_size):
            line = [None for _ in range(self.gap)]
            for x in range(self.horizontal_size):
                current = x + y * self.horizontal_size

                if (self.__is_king(current)):
                    piece = KingPiece(False)
                else:
                    piece = PawnPiece(False)

                line.append(piece)
            line.extend([None for _ in range(self.gap)])
            board.append(line)
        board.extend([[None for _ in range(self.horizontal_size + self.gap * 2)]
                     for _ in range(self.gap)])

        return board

    def build(self) -> Board:
        board = self.__init_board()

        return Board(self.horizontal_size, self.vertical_size, self.gap, board)
