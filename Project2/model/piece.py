from model.position import Position


class Piece:
    def __init__(self, is_black: bool) -> None:
        self.__is_black: bool = is_black

    def is_opposite(self, other: "Piece") -> bool:
        return other.is_black != self.__is_black

    is_black: bool = property(fget=lambda self: self.__is_black)

    def __repr__(self):
        return str(self)


class KingPiece(Piece):
    def __init__(self, is_black: bool) -> None:
        super().__init__(is_black)

    def __str__(self) -> str:
        return "B   " if self.is_black else "W   "


class PawnPiece(Piece):
    def __init__(self, is_black: bool) -> None:
        super().__init__(is_black)

    def __str__(self) -> str:
        return "b   " if self.is_black else "w   "