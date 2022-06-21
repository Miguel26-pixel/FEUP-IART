from abc import ABC, abstractmethod
from typing import Tuple, List
from controller.reward_system import RewardSystem, SimpleRewardSystem
from model.board import Board
from model.position import Direction, Position, Transformation
from model.piece import KingPiece, Piece


class GameController(ABC):
    def __init__(self, board: Board, black_first: bool, reward_system: RewardSystem) -> None:
        self._board: Board = board
        self.__current: bool = black_first
        self._reward_system: RewardSystem = reward_system

    def move(self, move: Transformation) -> bool:
        current_move = move.copy()
        if (not self._board.is_valid_position(current_move.position)):
            return False

        piece = self._board.get_cell(current_move.position)

        if (piece == None):
            return False

        self._board.set_cell(current_move.position, None)

        while 1:
            current_move.apply_position()

            if (not self._board.is_valid_position(current_move.position)):
                break

            temp_piece = self._board.get_cell(current_move.position)

            if (temp_piece is None):
                break

            self._board.set_cell(current_move.position, piece)
            piece = temp_piece

        if (not self._board.is_valid_position(current_move.position)):
            return True

        self._board.set_cell(current_move.position, piece)

        return True

    def check_valid_move(self, move: Transformation) -> Tuple[bool, int]:
        pos = move.position

        if self._board.is_valid_position(move.position) and self._board.board[pos.y][pos.x] is not None:
            return True, 0
        return False, self._reward_system.invalid_move()

    def get_groups(self) -> Tuple[int, List[Piece], dict]:
        pieces_groups: dict = dict()
        groups: List[List[Piece]] = []
        for y in range(self._board.vertical_size):
            for x in range(self._board.horizontal_size):
                self.update_groups_cell(Position(x, y), pieces_groups, groups)

        return len(list(filter(lambda a: len(a) > 0, groups))), groups, pieces_groups

    def merge_groups(self, target_group_idx: int, responsible_pieces: List[Piece], pieces_groups: dict, groups: List[List[Piece]]):
        target_group = groups[target_group_idx]
        for piece in responsible_pieces:
            group_idx = pieces_groups.get(piece)

            if (group_idx == target_group_idx):
                continue

            for old_piece in groups[group_idx]:
                pieces_groups.update({old_piece: target_group_idx})
            target_group.extend(groups[group_idx])
            pieces_groups.update({piece: target_group_idx})
            groups[group_idx] = []

    def update_groups_cell(self, position: Position, pieces_groups: dict, groups: List[List[Piece]]) -> None:
        piece = self._board.get_cell(position)
        if (piece == None):
            return

        responsible_pieces = []

        counter = 0
        for y in range(- 1, 1):
            if (counter > 3):  # Analyse only top row and left
                break
            for x in range(-1, 2):
                if (counter > 3):  # Analyse only top row and left
                    break
                counter += 1
                current_pos = Position(position.x + x, position.y + y)
                if (not self._board.is_valid_position(current_pos)):
                    continue

                current_piece = self._board.get_cell(current_pos)

                if (current_piece == None or current_pos == position):
                    continue

                responsible_pieces.append(current_piece)
            if (counter == 4):
                break

        if (len(responsible_pieces) == 0):
            pieces_groups.update({piece: len(groups)})
            groups.append([piece])

            return

        main_group_idx = pieces_groups.get(responsible_pieces[0])
        groups[main_group_idx].append(piece)
        pieces_groups.update({piece: main_group_idx})

        self.merge_groups(
            main_group_idx, responsible_pieces[1:], pieces_groups, groups)

    @abstractmethod
    def check_end_game(self, played_move: Transformation) -> Tuple[bool, int]:
        pass

    @abstractmethod
    def winner(self, played_move: Transformation, groups: List[List[Piece]], pieces_group: dict):
        pass


class SimpleGameController(GameController):
    def __init__(self, board: Board, black_first: bool, _reward_system: SimpleRewardSystem) -> None:
        self._board: Board = board
        self.__current: bool = black_first
        self._reward_system = _reward_system

    def check_end_game(self, played_move: Transformation) -> Tuple[bool, int]:
        groups_size, groups, pieces_group = self.get_groups()

        ended = False
        reward = 0

        if (groups_size > 1):
            is_winner = self.winner(
                played_move, groups, pieces_group)

            reward = self._reward_system.score(is_winner, groups)
            ended = True

        return ended, reward

    def winner(self, played_move: Transformation, groups: List[List[Piece]], pieces_group: dict):
        move = played_move.copy()
        position = move.apply_position()

        if (not self._board.is_valid_position(position)):
            """ If the piece that caused the splinter is removed 
                from the board consider a loss
            """
            return False

        piece = self._board.get_cell(position)
        piece_idx = pieces_group.get(piece)
        piece_score = len(groups[piece_idx])

        scores = list(map(lambda x: len(x), groups))
        is_max_score = max(scores) == piece_score

        if (is_max_score and scores.count(piece_score) > 1):
            return None  # TIE

        return is_max_score


class UniColoredGameController(GameController):
    def __get_kings_groups(self, groups) -> Tuple[int, int]:
        kings = []
        for idx, g in enumerate(groups):
            filtered = list(filter(lambda p: isinstance(p, KingPiece), g))
            for _ in range(len(list(filtered))):
                kings.append(idx)
        return kings

    def check_end_game(self, played_move: Transformation) -> Tuple[bool, int]:
        _, groups, pieces_group = self.get_groups()

        kings = self.__get_kings_groups(groups)

        if (len(kings) < 2):
            return True, self._reward_system.invalid_move()

        k1, k2 = kings

        if (k1 == k2):
            return False, 0

        move = played_move.copy()
        position = move.apply_position()

        if (not self._board.is_valid_position(position)):
            return True, self._reward_system.invalid_move()

        piece = self._board.get_cell(position)
        piece_idx = pieces_group.get(piece)

        if (k1 != piece_idx and k2 != piece_idx):
            return True, 0

        other = k2 if k1 == piece_idx else k1

        score_diff = len(groups[piece_idx]) - len(groups[other])
        if (score_diff > 0):
            is_winner = True
        elif (score_diff == 0):
            is_winner = None
        else:
            is_winner = False

        reward = self._reward_system.score(is_winner, groups, score_diff)

        return True, reward

    def winner(self, played_move: Transformation, groups: List[List[Piece]], pieces_group: dict):
        pass
