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
        self.linesCleared = 0
        #self.heightDifferences = self.get_relation()
        self.subwells = self.get_subwells()
        self.isMirror = self.mirror()

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

    def get_relation(self):
        bumps = self.get_bumpyness()
        relationalBumps = list(range(BOARD_DATA.width))
        heightDifferences = [0] * BOARD_DATA.width
        for col in range(len(relationalBumps)):
            if col == 0:
                relationalBumps[0] = (0, bumps[col + 1] - bumps[col])
            elif col == BOARD_DATA.width - 1:
                relationalBumps[BOARD_DATA.width-1] = (bumps[col] - bumps[col-1], 0)
            else:
                relationalBumps[col] = (bumps[col] - bumps[col - 1], bumps[col + 1] - bumps[col])
        return relationalBumps

    def get_subwells(self):
        subwells = []
        bumps = self.get_relation()
        for b in range(BOARD_DATA.width -4):
            subwells.append((0, (bumps[b][1]), bumps[b + 1], bumps[b + 2], bumps[b + 3]))
        return subwells



    def mirror(self):
        subwells = self.get_subwells()
        same = False
        mirror = False
        for i, sub in enumerate(subwells):
            for i, sub2 in enumerate(subwells):
                if sub == sub2:
                    same = True
        return same, mirror


    def get_normalized_bumpyness(self):
        bumps = self.get_bumpyness()
        minLevel = min(bumps)
        return (b - minLevel for b in bumps)

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
        pass

    def score(self, state):
        pass

    def nextMove(self, gameState):
        if gameState.nextShape == Shape.shapeNone:
            return None
        legalMoves = gameState.get_legal_moves()
        random.shuffle(legalMoves)

        print('diff: ', gameState.heightDifferences)
        print('subwells: ', gameState.subwells)
        print('mirror: ', gameState.isMirror)

        d, x = legalMoves[0]
        return (d, x, 0)


class QLearner(TetrisAI):
    def __init__(self):
        super().__init__()
        self.qvs = {}  # May need to use a Counter instead
        self.epsilon = 0.6
        self.alpha = 0.8
        self.discount = 0.9
        self.episodeRewards = 0
        self.seen = 0
        self.transitions = []

    def get_state(self, gameState):
        board = np.array(BOARD_DATA.getData()).reshape((BOARD_DATA.height, BOARD_DATA.width))
        shape1 = BOARD_DATA.currentShape
        shape2 = BOARD_DATA.nextShape
        gameState = GameState(board, shape1, shape2)
        state = (gameState.get_relation(), gameState.currentShape.shape)
        transitions.append(state)
        return state



    def getLegalActions(self, state):
        shape = Shape(state[2])
        if shape.shape in (Shape.shapeI, Shape.shapeZ, Shape.shapeS):
            directions = [0, 1]
        elif shape.shape == Shape.shapeO:
            directions = [0, ]
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

    def getAction(self, state):
        legalActions = self.getLegalActions(state)
        if len(legalActions) == 0:
            return None
        randInt = random.random()
        if randInt < self.epsilon:
            return random.choice(legalActions)
        else:
            return self.move_from_qvs(state)

    def get_qv(self, state, move):
        if (state, move) in self.qvs:
            self.seen += 1
            return self.qvs[(state, move)]
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
            qValue = self.get_qv(state, action)
            if qValue >= 0:
                if qValue == 0:
                    unseen = True
                positiveOrZero.append(action)
            if maxQ < qValue:
                maxQ = qValue
                best_action = action
        if unseen:
            return random.choice(positiveOrZero)
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
            return self.policy(state)


    def reward(self, state, transitions):
        reward = 0
        for state in transitions:
            nextState = self.nextState
            preHeight = max(state)
            postHeight = max(nextState.bumps)
            preHoles = gameState.get_holes
            postHoles = nextState.holes
            if postHeight > preHeight:
                reward -= 100
            if postholes > preHoles:
                reward -= 40
        return reward


    def update(self, state, move, nextState, reward):
        # How do we get the next state?
        q = self.get_qv(state, move)
        legalActions = self.getLegalActions(nextState)
        if len(legalActions) == 0:
            nextQValue = 0
        else:
            nextQValue = float('-inf')
            for move in legalActions:
                q = self.get_qv(nextState, move)
                if nextQValue < q:
                    nextQValue = q
        samp = reward + self.discount * nextQValue
        self.qvs[(state, move)] = (1 - self.alpha) * q + self.alpha * samp
        # value = self.get_value(nextState)
        # new_q = (1-self.alpha) * q + self.alpha * (score + self.discount*value)
        # self.qvs[(state, move)] = new_q

    def get_policy(self, state):
        return self.move_from_qvs(state)

    def get_value(self, state):
        return self.val_from_qvs(state)


class SimpleTetrisAI(object):
    def nextMove(self, gameState):
        if gameState.nextShape == Shape.shapeNone:
            print("NEXT SHAPE IS NONE")
            return None
        # print('Bumps: ', gameState.bumps)

        legalMoves = gameState.get_legal_moves()
        minScore = float('inf')
        bestAction = None
        for action in legalMoves:
            nextState = self.nextState(gameState, action)
            nextScore = sum(nextState.holes) - min(nextState.bumps)
            if nextScore < minScore or bestAction is None:
                minScore = nextScore
                bestAction = action
        print("bumps", gameState.bumps)
        print("rbumps", gameState.get_relation())
        print('subwells: ', gameState.get_subwells())
        print('mirror: ', gameState.isMirror)
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