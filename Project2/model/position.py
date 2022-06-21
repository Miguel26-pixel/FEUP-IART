class Direction:
    def __init__(self, x: int, y: int) -> None:
        self.x = x // abs(x) if x != 0 else 0
        self.y = y // abs(y) if y != 0 else 0
        pass

    def __str__(self) -> str:
        return f"Direction[x={self.x}, y={self.y}]"


class Position:
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y

    def __eq__(self, __o) -> bool:
        if not isinstance(__o, Position):
            return False
        return self.x == __o.x and self.y == __o.y

    def __str__(self) -> str:
        return f"Position[x={self.x}, y={self.y}]"

    def add_direction(self, direction: Direction):
        self.x += direction.x
        self.y += direction.y


class Transformation:
    def __init__(self, position: Position, direction: Direction) -> None:
        self.position = position
        self.direction = direction

    def __str__(self) -> str:
        return f"Transformation[{self.position}, {self.direction}]"

    def apply_position(self) -> Position:
        self.position = Position(
            self.position.x + self.direction.x, self.position.y + self.direction.y)
        return self.position

    def copy(self):
        position = Position(self.position.x, self.position.y)
        direction = Direction(self.direction.x, self.direction.y)
        return Transformation(position, direction)
