from tetris_model import BOARD_DATA, Shape
import math
from datetime import datetime
import numpy as np
import random
import util


class GameState:
    def __init__(self, board):
        self.board = BOARD_DATA
        self.bumpyness = TetrisAI.bumpyness()
        self.holes = TetrisAI.get_holes
        self.shape = BOARD_DATA.currentShape


        self.legalActions = TetrisAI.getLegalActions()

    def calcStep1Board(self, d0, x0):
        board = np.array(BOARD_DATA.getData()).reshape((BOARD_DATA.height, BOARD_DATA.width))
        self.dropDown(board, BOARD_DATA.currentShape, d0, x0)
        return board

    def reward(self):
        survival = False
        gameOver = False
        t1 = datetime.now()





class TetrisAI(object):

    def __init__(self):
        self.qValues = util.Counter()

    def getQValue(self, state, action, successor):
        return self.qValues[state, action, successor]

    def getState(self, GameState):
        state = GameState





    def nextMove(self, gameState):
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
        bumpyness = self.bumpyness()
        print('Bumpyness: ', bumpyness)
        holes = self.get_holes(bumpyness)
        print('Holes: ', holes)
        legalActions = self.getLegalActions()
        print('actions ', legalActions)

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

    def get_holes(self, bumpyness):
        board = np.array(BOARD_DATA.getData()).reshape((BOARD_DATA.height, BOARD_DATA.width))
        holes = [0] * BOARD_DATA.width
        for col in range(BOARD_DATA.width):
            for row in range(BOARD_DATA.height -1, bumpyness[col], -1):
                if not board[row, col]:
                    holes[col] += 1
        return holes


    def getLegalActions(self):
        legalActions = []
        if BOARD_DATA.currentShape == Shape.shapeNone:
            '''print('ShapeNone')'''
            return None
        currentDirection = BOARD_DATA.currentDirection
        currentY = BOARD_DATA.currentY
        _, _, minY, _ = BOARD_DATA.nextShape.getBoundingOffsets(0)
        nextY = -minY
        if BOARD_DATA.currentShape.shape in (Shape.shapeI, Shape.shapeZ, Shape.shapeS):
            d0Range = (0, 1)
        elif BOARD_DATA.currentShape.shape == Shape.shapeO:
            d0Range = (0,)
        else:
            d0Range = (0, 1, 2, 3)

        if BOARD_DATA.nextShape.shape in (Shape.shapeI, Shape.shapeZ, Shape.shapeS):
            d1Range = (0, 1)
        elif BOARD_DATA.nextShape.shape == Shape.shapeO:
            d1Range = (0,)
        else:
            d1Range = (0, 1, 2, 3)
        for d0 in d0Range:
            minX, maxX, _, maxY = BOARD_DATA.currentShape.getBoundingOffsets(d0)
            for x0 in range(-minX, BOARD_DATA.width - maxX):
                legalActions.append((d0, x0))
        return legalActions


    def setNewBoard(self, d0Range, step1Board, d1Range):
        for d0 in d0Range:
            minX, maxX, _, maxY = BOARD_DATA.currentShape.getBoundingOffsets(d0)
            for x0 in range(-minX, BOARD_DATA.width - maxX):
                board = self.calcStep1Board(d0, x0)
                for d1 in d1Range:
                    minX, maxX, _, _ = BOARD_DATA.nextShape.getBoundingOffsets(d1)
                    dropDist = self.calcNextDropDist(board, d1, range(-minX, BOARD_DATA.width - maxX))
                    for x1 in range(-minX, BOARD_DATA.width - maxX):
                        score = self.calculateScore(np.copy(board), d1, x1, dropDist)
                        if not strategy or strategy[2] < score:
                            strategy = (d0, x0, score)
        return strategy

    def getAction(self, gameState):
        legalActions = []

        return 0

TETRIS_AI = TetrisAI()