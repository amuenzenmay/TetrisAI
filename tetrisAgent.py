from tetris_model import BOARD_DATA, Shape
import math
from datetime import datetime
import numpy as np

class gameState:
    def __init__(self, shape, direction, nextShape, board):
        self.shape = shape
        self.direction = direction
        self.nextShape = nextShape
        self.board = board

class TetrisAI(object):
    def nextMove(self):
        if BOARD_DATA.nextShape == Shape.shapeNone:
            return None
