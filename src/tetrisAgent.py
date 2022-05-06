from tetris_model import BOARD_DATA, Shape
import random


class GameState:
    def __init__(self, board, shape, nextShape=None):
        self.currentShape = shape
        self.nextShape = nextShape
        self.board = board
        self.contour = self.get_contours()
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
        """Returns a tuple of integers ranged 0-6 representing the height diff between
        a column and subsequent columns."""
        bumps = self.get_bumpyness()
        wells = [(bumps[i], bumps[i + 1], bumps[i + 2], bumps[i + 3], bumps[i + 4]) for i in
                 range(BOARD_DATA.width - 4)]
        contour = []
        for subwell in wells:
            temp = [0] * 4
            for idx in range(len(subwell) - 1):
                diff = subwell[idx + 1] - subwell[idx]
                if diff > 3:
                    diff = 3
                if diff < -3:
                    diff = -3
                temp[idx] = diff + 3
            contour.append(tuple(temp))
        return tuple(contour)

    def get_holes(self):
        """Returns a tuple containing the amount of holes in each column."""
        holes = [0] * BOARD_DATA.width
        for col in range(BOARD_DATA.width):
            for row in range(BOARD_DATA.height - 1, BOARD_DATA.height - 1 - self.bumps[col], -1):
                if not self.board[row, col]:
                    holes[col] += 1
        return tuple(holes)


class QLearner():
    def __init__(self, **kwargs):
        self.qvs = {}
        self.epsilon = kwargs.get('epsilon', 0.05)
        self.alpha = kwargs.get('alpha', 0.2)
        self.discount = kwargs.get('discount', 0.7)
        self.train = kwargs.get('train', True)

    def state_from_gamestate(self, gamestate):
        return gamestate.contour, gamestate.currentShape.shape

    def get_reward(self, gameState, nextGameState, lines):
        maxHeight1 = max(gameState.get_bumpyness())
        maxHeight2 = max(nextGameState.get_bumpyness())
        sumHoles1 = sum(gameState.holes)
        sumHoles2 = sum(nextGameState.holes)
        reward = 0
        if maxHeight2 > maxHeight1:
            reward -= 100 * (maxHeight2 - maxHeight1)
        if sumHoles2 > sumHoles1:
            reward -= 40 * (sumHoles2 - sumHoles1)
        reward += lines ** 2
        return reward

    def get_legal_actions(self, state):
        shape = Shape(state[1])
        if shape.shape in (Shape.shapeI, Shape.shapeZ, Shape.shapeS):
            directions = [0, 1]
        elif shape.shape == Shape.shapeO:
            directions = [0]
        else:
            directions = [0, 1, 2, 3]

        legalMoves = []
        for d in directions:
            minX, maxX, _, _ = shape.getBoundingOffsets(d)
            validX = list(range(-minX, BOARD_DATA.width - maxX))
            for x in validX:
                legalMoves.append((d, x))
        return legalMoves

    def observe_transitions(self, state, action, nextState, deltaReward):
        self.update(state, action, nextState, deltaReward)

    def get_action(self, state):
        legalActions = self.get_legal_actions(state)
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

    def move_from_qvs(self, state):
        best_action = None
        maxQ = float('-inf')
        legal_actions = self.get_legal_actions(state)
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
        return best_action

    def update(self, state, move, nextState, reward):
        stateKey = self.calculate_index(state[0][0], state[1], move[0], move[1])
        q1 = self.get_qv(stateKey)
        legalActions = self.get_legal_actions(nextState)
        if len(legalActions) == 0:
            nextQValue = 0
        else:
            nextQValue = float('-inf')
            for action in legalActions:
                nextStateKey = self.calculate_index(nextState[0][0], state[1], action[0], action[1])
                q2 = self.get_qv(nextStateKey)
                if nextQValue < q2:
                    nextQValue = q2
        samp = reward + self.discount * nextQValue

        stateKey = self.calculate_index(state[0][0], state[1], move[0], move[1])
        self.qvs[stateKey] = (1 - self.alpha) * q1 + self.alpha * samp

    def get_policy(self, state):
        return self.move_from_qvs(state)

    def calculate_index(self, contour, shape, d0, x0):
        index = 0
        index += (contour[0] + 7 * contour[1] + 49 * contour[2] + 343 * contour[3])
        return index, shape, d0, x0


TETRIS_AI = QLearner()
