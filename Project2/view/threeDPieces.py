from ursina import *
from model.board import Board

class BlackPawn(Button):
    def __init__(self, position):
        self.entity = Entity(model='cube', color=color.gray, collider="box", ignore=True,
                position = position,
                scale = .5,
                parent = Board)

    def update_position(self,x,y,z):
        self.position = (x,y,z)



class BlackKing(Button):
    def __init__(self, position):
        self.entity = Entity(model='cube', color=color.black, collider="box", ignore=True,
                position = position,
                scale = .5,
                parent = Board)

    def update_position(self,x,y,z):
        self.position = (x,y,z)