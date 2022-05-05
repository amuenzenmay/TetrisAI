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
        self.contour = self.get_contours()
        # self.mirror = self.mirror
        self.bumps = self.get_bumpyness()
        self.holes = self.get_holes()
        self.linesCleared = 0

    def get_bumpyness(self):
        """Returns a list of each column's highest shape. 0 is the top of the board
        and 20 means the column has no shapes in it."""
        bumps = [0] * BOARD_DATA.width
        for col in range(BOARD_DATA.width):
            for row in range(0, BOARD_DATA.height):
                if self.board[row, col]:
                    height = BOARD_DATA.height - row
                    if height > bumps[col]:
                        bumps[col] = height
        return tuple(bumps)

    def get_contours(self):
        bumps = self.get_bumpyness()
        wells = [(bumps[i], bumps[i+1], bumps[i+2], bumps[i+3], bumps[i+4]) for i in range(BOARD_DATA.width - 4)]
        contour = []
        for subwell in wells:
            temp = [0] * 4
            for idx in range(len(subwell)-1):
                diff = subwell[idx+1] - subwell[idx]
                if diff > 3:
                    diff = 3
                if diff < -3:
                    diff = -3
                temp[idx] = diff + 3
            contour.append(tuple(temp))
        return tuple(contour)

    def calculate_index(self, contour, shape, x0, d0):
        index = 0
        print('Contour: ', contour)
        index += (contour[0] + 7*contour[1] + 49*contour[2] + 343 * contour[3])
        return index, shape, x0, d0

    def get_holes(self):
        holes = [0] * BOARD_DATA.width
        for col in range(BOARD_DATA.width):
            for row in range(BOARD_DATA.height - 1, BOARD_DATA.height - 1 - self.bumps[col], -1):
                if not self.board[row, col]:
                    holes[col] += 1
        return tuple(holes)

    def get_legal_moves(self):
        if self.currentShape.shape in (Shape.shapeI, Shape.shapeZ, Shape.shapeS):
            directions = [0, 1]
        elif self.currentShape.shape == Shape.shapeO:
            directions = [0]
        else:
            directions = [0, 1, 2, 3]

        legalMoves = []
        for d in directions:
            minX, maxX, minY, maxY = self.currentShape.getBoundingOffsets(d)
            # validX = list(range(-minX, BOARD_DATA.width - maxX))
            validX = list(range(-minX, 5 - maxX))
            for x in validX:
                legalMoves.append((d, x))
        return legalMoves


class TetrisAI(object):
    def __init__(self):
        pass

    def score(self, state):
        pass

    def nextMove(self, gameState):
        if gameState.nextShape == Shape.shapeNone:
            return None
        legalMoves = gameState.get_legal_moves()
        random.shuffle(legalMoves)

        # heightDiffs = gameState.heightDiffs
        # print('heightDiffs: ', heightDiffs)
        # subwells = gameState.subwells
        print('subwells: ', gameState.newSubwells)
        # gameState.create_subwells()
        # print(BOARD_DATA.backBoard)
        print(gameState.get_contour())
        # mirror = gameState.mirror
        # print('mirror', mirror)

        d, x = legalMoves[0]
        return (d, x, 0)


class QLearner(TetrisAI):
    def __init__(self):
        super().__init__()
        self.qvs = {}  # May need to use a Counter instead
        self.epsilon = 0.05
        self.alpha = 0.2
        self.discount = 0.8
        self.episodeRewards = 0
        self.e = {}
        self.chosen = 0

    def incrementE(self, stateKey):
        if stateKey in self.e.keys():
            self.e[stateKey] += 1
        else:
            self.e[stateKey] = 1

    def getLegalActions(self, state):
        shape = Shape(state[1])
        if shape.shape in (Shape.shapeI, Shape.shapeZ, Shape.shapeS):
            directions = [0, 1]
        elif shape.shape == Shape.shapeO:
            directions = [0]
        else:
            directions = [0, 1, 2, 3]

        legalMoves = []
        for d in directions:
            minX, maxX, minY, maxY = shape.getBoundingOffsets(d)
            validX = list(range(-minX, BOARD_DATA.width - maxX))
            for x in validX:
                legalMoves.append((d, x))
        return legalMoves

    def observeTransition(self, state, action, nextState, deltaReward):
        self.episodeRewards += deltaReward
        self.update(state, action, nextState, deltaReward)

    def weights(self):
        return self.weights

    def getAction(self, state):
        legalActions = self.getLegalActions(state)
        if len(legalActions) == 0:
            return None
        randInt = random.random()
        if randInt < self.epsilon:
            return random.choice(legalActions)
        else:
            return self.move_from_qvs(state)

    def get_qv(self, stateKey):
        if stateKey in self.qvs:
            return self.qvs[stateKey]
        else:
            return 0.0

    def val_from_qvs(self, state):
        legal = state.get_legal_moves()
        return max([self.get_qv(state, move) for move in legal])

    def move_from_qvs(self, state):
        best_action = None
        maxQ = float('-inf')
        legal_actions = self.getLegalActions(state)
        unseen = False
        positiveOrZero = []
        if len(legal_actions) == 0:
            return None
        for action in legal_actions:
            stateKey = self.calculate_index(state[0][0], state[1], action[0], action[1])
            qValue = self.get_qv(stateKey)
            if qValue >= 0:
                if qValue == 0:
                    unseen = True
                positiveOrZero.append(action)
            if maxQ < qValue:
                maxQ = qValue
                best_action = action
        if unseen:
            return random.choice(positiveOrZero)
        self.chosen += 1
        return best_action
        # moves = {}
        # for move in state.get_legal_moves():
        #     moves[move] = self.get_qv(state, move)
        # return max(moves, key=moves.get) # This should get argmax(qvs)

    def get_move(self, state):
        legal = state.get_legal_moves()
        if not len(legal):
            return None
        randy = random.random()
        if randy > self.epsilon:
            return random.choice(legal)
        else:
            return self.get_policy(state)

    def update(self, state, move, nextState, reward):
        # How do we get the next state?
        print('Move in update: ', move)
        stateKey = self.calculate_index(state[0][0], state[1], move[0], move[1])
        q1 = self.get_qv(stateKey)
        legalActions = self.getLegalActions(nextState)
        if len(legalActions) == 0:
            nextQValue = 0
        else:
            nextQValue = float('-inf')
            # print(legalActions)
            for action in legalActions:
                nextStateKey = self.calculate_index(nextState[0][0], state[1], action[0], action[1])
                q2 = self.get_qv(nextStateKey)
                if nextQValue < q2:
                    nextQValue = q2
            # delta = reward + self.discount * nextQValue - q1
            # for stateKey in self.e.keys():

            # self.incrementE(stateKey)
        samp = reward + self.discount * nextQValue

        stateKey = self.calculate_index(state[0][0], state[1], move[0], move[1])
        qval = (1 - self.alpha) * q1 + self.alpha * samp
        # print(stateKey[0], stateKey[1], stateKey[2], stateKey[3], qval)
        print('Contour: {}\nShape: {}\nDirection: {}\nXValue: {}\nQVal: {}'.format(stateKey[0], stateKey[1], stateKey[2], stateKey[3], qval))
        self.qvs[stateKey] = (1 - self.alpha) * q1 + self.alpha * samp
        # value = self.get_value(nextState)
        # new_q = (1-self.alpha) * q + self.alpha * (score + self.discount*value)
        # self.qvs[(state, move)] = new_q

    def get_policy(self, state):
        return self.move_from_qvs(state)

    def get_value(self, state):
        return self.val_from_qvs(state)

    def calculate_index(self, contour, shape, d0, x0):
        index = 0
        # print('Contour: ', contour)
        index += (contour[0] + 7*contour[1] + 49*contour[2] + 343 * contour[3])
        return index, shape, d0, x0


class SimpleTetrisAI(object):
    def nextMove(self, gameState):
        if gameState.nextShape == Shape.shapeNone:
            print("NEXT SHAPE IS NONE")
            return None
        # print('Bumps: ', gameState.bumps)
        # print(gameState.get_contour())
        legalMoves = gameState.get_legal_moves()
        minScore = float('inf')
        bestAction = None
        for action in legalMoves:
            nextState = self.nextState(gameState, action)
            nextScore = sum(nextState.holes) - min(nextState.bumps)
            if nextScore < minScore or bestAction is None:
                minScore = nextScore
                bestAction = action

        return bestAction

    def nextState(self, gameState, action):
        nextBoard = np.array(BOARD_DATA.getData()).reshape((BOARD_DATA.height, BOARD_DATA.width))
        shape = gameState.currentShape
        direction, x = action
        self.dropShape(nextBoard, shape, direction, x)
        return GameState(nextBoard, gameState.nextShape)

    def dropShape(self, board, shape, direction, x0):
        ydist = BOARD_DATA.height - 1
        for x, y in shape.getCoords(direction, x0, 0):
            changeY = 0
            while changeY + y < BOARD_DATA.height and (changeY + y < 0 or board[(y + changeY), x] == Shape.shapeNone):
                changeY += 1
            changeY -= 1
            if changeY < ydist:
                ydist = changeY
        # print("dropDown: shape {0}, direction {1}, x0 {2}, dy {3}".format(shape.shape, direction, x0, dy))
        self.dropShapeByDistance(board, shape, direction, x0, ydist)

    def dropShapeByDistance(self, data, shape, direction, x0, dist):
        for x, y in shape.getCoords(direction, x0, 0):
            data[y + dist, x] = shape.shape



# TETRIS_AI = TetrisAI()
# TETRIS_AI = SimpleTetrisAI()
TETRIS_AI = QLearner()