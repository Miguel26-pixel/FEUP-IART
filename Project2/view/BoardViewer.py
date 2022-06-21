from time import sleep
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from model.piece import KingPiece, PawnPiece, Piece
from typing import List
from view.threeDPieces import *


class BoardViewer() :
    
    def __init__(self, board: Board):
        self.board = board
        

    def _init_camera(self,x,y,z):
        entity = Entity(model="cube", color=None, collider="box", ignore=True,
                position = (x, y, z),
                parent = scene)
        #player = FirstPersonController(x=x, y=y, z=z)
        camera.position = (x,y,z)
        camera.rotation_x = 20
        camera.rotation_y = 90
        blue_player = Entity(model="./view/9244_open3dmodel/1/10.3DS", color=color.blue, collider="box", ignore=True,
                position = (4, -2, -3),
                parent = scene,
                scale = 15)

        red_player = Entity(model="./view/9244_open3dmodel/1/10.3DS", color=color.red, collider="box", ignore=True,
                    position = (4, -2, 9),
                    parent = scene,
                    scale = 15)
        red_player.rotation=(0,180,0)
        

    def render(self, board : Board):
        move = board.board
        scene.clear()
        Sky(texture="./view/space.jpg")
        self._init_camera(-23,13,4.5)
        for x in range(board.horizontal_size):
            for z in range(board.vertical_size):
                if (board.board[z][x] == None):
                    Entity(model="cube", color=color.white, collider="box", ignore=True,
                    position = (x, 0, z),
                    parent = scene,
                    texture='black.jpg')

                elif (isinstance(board.board[z][x], PawnPiece)):
                    Entity(model="cube", color=color.white, collider="box", ignore=True,
                    position = (x, 0, z),
                    parent = scene,
                    texture='black.jpg')
                    BlackPawn((x-0.5,1,z))

                else:
                    Entity(model="cube", color=color.white, collider="box", ignore=True,
                    position = (x, 0, z),
                    parent = scene,
                    texture='black.jpg')
                    BlackKing((x-0.5,1,z))

