from tetris_model import BOARD_DATA, Shape
import math
from datetime import datetime
import numpy as np
import random


class GameState:
    def __init__(self, board, shape, nextShape=None):
        self.currentShape = shape
        self.nextShape = nextShape
        self.board = board
        self.bumps = self.get_bumpyness()
        self.holes = self.get_holes()

    def get_bumpyness(self):
        bumps = [BOARD_DATA.height] * BOARD_DATA.width
        for col in range(BOARD_DATA.width):
            for row in range(0, BOARD_DATA.height):
                if self.board[row, col]:
                    if row < bumps[col]:
                        bumps[col] = row
        return bumps

    def get_holes(self):
        holes = [0] * BOARD_DATA.width
        for col in range(BOARD_DATA.width):
            for row in range(BOARD_DATA.height - 1, self.bumps[col], -1):
                if not self.board[row, col]:
                    holes[col] += 1
        return holes

    def getLegalMoves(self):
        if self.currentShape.shape in (Shape.shapeI, Shape.shapeZ, Shape.shapeS):
            directions = [0, 1]
        elif self.currentShape.shape == Shape.shapeO:
            directions = [0, ]
        else:
            directions = [0, 1, 2, 3]

        legalMoves = []
        for d in directions:
            minX, maxX, minY, maxY = self.currentShape.getBoundingOffsets(d)
            validX = list(range(-minX, BOARD_DATA.width - maxX))
            for x in validX:
                legalMoves.append((d, x))
        return legalMoves


class TetrisAI(object):
    def nextMove(self, gameState):
        if gameState.nextShape == Shape.shapeNone:
            return None

        legalMoves = gameState.getLegalMoves()
        random.shuffle(legalMoves)

        print('Bumps: ', gameState.bumps)
        print('Holes: ', gameState.holes)
        print('Moves: ', legalMoves)
        d, x = legalMoves[0]

        return (d, x, 0)


TETRIS_AI = TetrisAI()
