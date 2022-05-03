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
    def __init__(self):
        self.qvs = {} # May need to use a Counter instead
        self.epsilon = 0.5
        self.alpha = 0
        self.discord = 0.7
    
    def get_qv(self, state, move):
        if (state, move) in self.qvs:
          return self.qvs[(state, move)]
        else:
          return 0.0

    def val_from_qvs(self, state):
        legal = state.getLegalMoves()
        return max([self.get_qv(state, move) for move in legal])

    def move_from_qvs(self, state):
        moves = {}
        for move in self.getLegalMoves():
            moves[move] = self.get_qv(state, move)
        pass # Need to return the arg max of moves[move]

    def get_move(self, state):
        legal = state.getLegalMoves()
        if not len(legal):
            return None
        randy = random.random()
        if randy > self.epsilon:
          return random.choice(legal)
        else:
          return self.policy(state)

    def update(self, state, move, nextState, reward):
        # How do we get the next state?
        q = self.get_qv(state, move)
        value = self.get_value(nextState)
        new_q = (1-self.alpha) * q + self.alpha * (reward + self.discount*value)
        self.qvs[(state, move)] = new_q

    def get_policy(self, state):
        return self.move_from_qvs(state)

    def get_value(self, state):
        return self.val_from_qvs(state)

    def nextMove(self, state):
        if state.nextShape == Shape.shapeNone:
            return None
        legalMoves = state.getLegalMoves()
        random.shuffle(legalMoves)

        print('Bumps: ', state.bumps)
        print('Holes: ', state.holes)
        print('Moves: ', legalMoves)
        d, x = legalMoves[0]
    
        return (d, x, 0)

TETRIS_AI = TetrisAI()
