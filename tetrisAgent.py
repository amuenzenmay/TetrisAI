from tetris_model import BOARD_DATA, Shape
import math
from datetime import datetime
import numpy as np
import random
import util


class GameState:
<<<<<<< HEAD
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



=======
    def __init__(self, board, shape, nextShape=None):
        self.currentShape = shape
        self.nextShape = nextShape
        self.board = board
        self.bumps = self.get_bumpyness()
        self.holes = self.get_holes()
>>>>>>> 68198ccede06878af0edc7aa5c9a622f14133852

    def get_bumpyness(self):
        bumps = [BOARD_DATA.height] * BOARD_DATA.width
        for col in range(BOARD_DATA.width):
            for row in range(0, BOARD_DATA.height):
                if self.board[row, col]:
                    if row < bumps[col]:
                        bumps[col] = row
        return bumps

<<<<<<< HEAD
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
=======
    def get_holes(self):
        holes = [0] * BOARD_DATA.width
        for col in range(BOARD_DATA.width):
            for row in range(BOARD_DATA.height - 1, self.bumps[col], -1):
                if not self.board[row, col]:
                    holes[col] += 1
        return holes
>>>>>>> 68198ccede06878af0edc7aa5c9a622f14133852

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

<<<<<<< HEAD
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
=======
>>>>>>> 68198ccede06878af0edc7aa5c9a622f14133852

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