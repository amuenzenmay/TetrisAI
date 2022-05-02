from tetris_model import BOARD_DATA, Shape
import math
from datetime import datetime
import numpy as np
import random


class gameState:
    def __init__(self, holes, board, shape):
        self.shape = shape
        self.holes = holes
        self.board = board


class TetrisAI(object):
    def nextMove(self):
        if BOARD_DATA.nextShape == Shape.shapeNone:
            return None

        if BOARD_DATA.currentShape.shape in (Shape.shapeI, Shape.shapeZ, Shape.shapeS):
            currDirRange = [0, 1]
        elif BOARD_DATA.currentShape.shape == Shape.shapeO:
            currDirRange = [0, ]
        else:
            currDirRange = [0, 1, 2, 3]

        if BOARD_DATA.nextShape.shape in (Shape.shapeI, Shape.shapeZ, Shape.shapeS):
            nextDirRange = [0, 1]
        elif BOARD_DATA.nextShape.shape == Shape.shapeO:
            nextDirRange = [0, ]
        else:
            nextDirRange = [0, 1, 2, 3]

        random.shuffle(currDirRange)
        randDir = currDirRange[0]

        minX, maxX, minY, maxY = BOARD_DATA.currentShape.getBoundingOffsets(randDir)
        validX = list(range(-minX, BOARD_DATA.width - maxX))
        random.shuffle(validX)
        randX = validX[0]
        print(self.bumpyness())

        return (randDir, randX, 0)

    def bumpyness(self):
        board = np.array(BOARD_DATA.getData()).reshape((BOARD_DATA.height, BOARD_DATA.width))
        bumpyness = [BOARD_DATA.height] * BOARD_DATA.width
        for col in range(BOARD_DATA.width):
            for row in range(0, BOARD_DATA.height):
                if board[row, col]:
                    if row < bumpyness[col]:
                        bumpyness[col] = row
        return bumpyness


TETRIS_AI = TetrisAI()
