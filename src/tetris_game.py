#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor

from tetris_model import BOARD_DATA, Shape
from tetrisAgent import QLearner, GameState
import numpy as np

class Tetris(QMainWindow):
    def __init__(self):
        super().__init__()
        self.isStarted = False
        self.isPaused = False
        self.gameOver = False
        self.nextMove = None
        self.lastShape = Shape.shapeNone
        self.shapesPlaced = 0

        self.initUI()

    def initUI(self):
        self.gridSize = 30
        self.speed = 25

        self.timer = QBasicTimer()
        self.setFocusPolicy(Qt.StrongFocus)

        hLayout = QHBoxLayout()
        self.tboard = Board(self, self.gridSize)
        hLayout.addWidget(self.tboard)

        self.sidePanel = SidePanel(self, self.gridSize)
        hLayout.addWidget(self.sidePanel)

        self.statusbar = self.statusBar()
        self.tboard.msg2Statusbar[str].connect(self.statusbar.showMessage)

        self.start()

        self.center()
        self.setWindowTitle('Tetris')
        self.show()

        self.setFixedSize(self.tboard.width() + self.sidePanel.width(),
                          self.sidePanel.height() + self.statusbar.height())

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def start(self):
        if self.isPaused:
            return

        self.isStarted = True
        self.tboard.score = 0
        BOARD_DATA.clear()

        self.tboard.msg2Statusbar.emit(str(self.tboard.score))

        BOARD_DATA.createNewPiece()
        self.timer.start(self.speed, self)

    def pause(self):
        if not self.isStarted:
            return

        self.isPaused = not self.isPaused

        if self.isPaused:
            self.timer.stop()
            self.tboard.msg2Statusbar.emit("paused")
        else:
            self.timer.start(self.speed, self)

        self.updateWindow()

    def updateWindow(self):
        self.tboard.updateData()
        self.sidePanel.updateData()
        self.update()

    def train(self, gameState):
        state = agent.state_from_gamestate(gameState)
        if agent and not self.nextMove:
            self.nextMove = agent.get_action(state)
        if self.nextMove:
            # Put the shape into the correct orientation
            k = 0
            while BOARD_DATA.currentDirection != self.nextMove[0] and k < 4:
                BOARD_DATA.rotateRight()
                k += 1
            k = 0
            while BOARD_DATA.currentX != self.nextMove[1] and k < 5:
                if BOARD_DATA.currentX > self.nextMove[1]:
                    BOARD_DATA.moveLeft()
                elif BOARD_DATA.currentX < self.nextMove[1]:
                    BOARD_DATA.moveRight()
                k += 1
        lines, merged = BOARD_DATA.moveDown()  # Move to the next State

        if lines is not None:
            # Get next state and reward
            if merged:
                self.shapesPlaced += 1
                board = np.array(BOARD_DATA.getData()).reshape((BOARD_DATA.height, BOARD_DATA.width))
                shape1 = BOARD_DATA.currentShape
                shape2 = BOARD_DATA.nextShape
                nextGameState = GameState(board, shape1, shape2)
                nextState = agent.state_from_gamestate(nextGameState)
                reward = agent.get_reward(gameState, nextGameState, lines)
                agent.observe_transitions(state, self.nextMove, nextState, reward)
            self.tboard.score += lines
            if self.lastShape != BOARD_DATA.currentShape:
                self.nextMove = None
                self.lastShape = BOARD_DATA.currentShape

            self.updateWindow()
        else:
            self.gameOver = True

    def play(self, gameState):
        state = agent.state_from_gamestate(gameState)
        if agent and not self.nextMove:
            self.nextMove = agent.get_policy(state)
        if self.nextMove:
            # Put the shape into the correct orientation
            k = 0
            while BOARD_DATA.currentDirection != self.nextMove[0] and k < 4:
                BOARD_DATA.rotateRight()
                k += 1
            k = 0
            while BOARD_DATA.currentX != self.nextMove[1] and k < 5:
                if BOARD_DATA.currentX > self.nextMove[1]:
                    BOARD_DATA.moveLeft()
                elif BOARD_DATA.currentX < self.nextMove[1]:
                    BOARD_DATA.moveRight()
                k += 1
        lines, merged = BOARD_DATA.moveDown()  # Move to the next State

        if lines is not None:
            if merged:
                self.shapesPlaced += 1
            self.tboard.score += lines
            if self.lastShape != BOARD_DATA.currentShape:
                self.nextMove = None
                self.lastShape = BOARD_DATA.currentShape

            self.updateWindow()
        else:
            self.gameOver = True

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            if self.gameOver:
                QApplication.quit()

            # Get the current state
            board = np.array(BOARD_DATA.getData()).reshape((BOARD_DATA.height, BOARD_DATA.width))
            shape1 = BOARD_DATA.currentShape
            shape2 = BOARD_DATA.nextShape
            gameState = GameState(board, shape1, shape2)

            if agent.train:
                self.train(gameState)
            else:
                self.play(gameState)

        else:
            super(Tetris, self).timerEvent(event)

    def keyPressEvent(self, event):
        if not self.isStarted or BOARD_DATA.currentShape == Shape.shapeNone:
            super(Tetris, self).keyPressEvent(event)
            return

        key = event.key()

        if key == Qt.Key_P:
            self.pause()
            return

        if self.isPaused:
            return
        elif key == Qt.Key_Left:
            BOARD_DATA.moveLeft()
        elif key == Qt.Key_Right:
            BOARD_DATA.moveRight()
        elif key == Qt.Key_Up:
            BOARD_DATA.rotateLeft()
        elif key == Qt.Key_Space:
            self.tboard.score += BOARD_DATA.dropDown()
        elif key == Qt.Key_Shift:
            tempShape = BOARD_DATA.currentShape
            BOARD_DATA.currentShape = BOARD_DATA.nextShape
            BOARD_DATA.nextShape = tempShape
        elif key == Qt.Key_C:
            BOARD_DATA.clear()
            self.tboard.score = 0
        elif key == Qt.Key_Escape:
            self.timer.stop()
            print('Exiting Game')
            global EXIT
            EXIT = True
            QApplication.quit()
        elif key == Qt.Key_S:
            self.speed -= 5
        elif key == Qt.Key_W:
            self.speed += 5
        else:
            super(Tetris, self).keyPressEvent(event)

        self.updateWindow()


def drawSquare(painter, x, y, val, s):
    colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                  0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

    if val == 0:
        return

    color = QColor(colorTable[val])
    x = int(x)
    y = int(y)
    s = int(s)

    painter.fillRect(x + 1, y + 1, s - 2, s - 2, color)

    painter.setPen(color.lighter())
    painter.drawLine(x, y + s - 1, x, y)
    painter.drawLine(x, y, x + s - 1, y)

    painter.setPen(color.darker())
    painter.drawLine(x + 1, y + s - 1, x + s - 1, y + s - 1)
    painter.drawLine(x + s - 1, y + s - 1, x + s - 1, y + 1)


class SidePanel(QFrame):
    def __init__(self, parent, gridSize):
        super().__init__(parent)
        self.setFixedSize(gridSize * 5, gridSize * BOARD_DATA.height)
        self.move(gridSize * BOARD_DATA.width, 0)
        self.gridSize = gridSize

    def updateData(self):
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        minX, maxX, minY, maxY = BOARD_DATA.nextShape.getBoundingOffsets(0)

        dy = 3 * self.gridSize
        dx = (self.width() - (maxX - minX) * self.gridSize) / 2

        val = BOARD_DATA.nextShape.shape
        for x, y in BOARD_DATA.nextShape.getCoords(0, 0, -minY):
            drawSquare(painter, x * self.gridSize + dx, y * self.gridSize + dy, val, self.gridSize)


class Board(QFrame):
    msg2Statusbar = pyqtSignal(str)
    speed = 1

    def __init__(self, parent, gridSize):
        super().__init__(parent)
        self.setFixedSize(gridSize * BOARD_DATA.width, gridSize * BOARD_DATA.height)
        self.gridSize = gridSize
        self.initBoard()

    def initBoard(self):
        self.score = 0
        BOARD_DATA.clear()

    def paintEvent(self, event):
        painter = QPainter(self)

        # Draw backboard
        for x in range(BOARD_DATA.width):
            for y in range(BOARD_DATA.height):
                val = BOARD_DATA.getValue(x, y)
                drawSquare(painter, x * self.gridSize, y * self.gridSize, val, self.gridSize)

        # Draw current shape
        for x, y in BOARD_DATA.getCurrentShapeCoord():
            val = BOARD_DATA.currentShape.shape
            drawSquare(painter, x * self.gridSize, y * self.gridSize, val, self.gridSize)

        # Draw a border
        painter.setPen(QColor(0x777777))
        painter.drawLine(self.width() - 1, 0, self.width() - 1, self.height())
        painter.setPen(QColor(0xCCCCCC))
        painter.drawLine(self.width(), 0, self.width(), self.height())

    def updateData(self):
        self.msg2Statusbar.emit(str(self.score))
        self.update()

def get_trained_values(path='qvaluesTrain1.pickle'):
    qvalues = None
    if os.path.getsize(path) > 0:
        f_myfile = open(path, 'rb')
        qvalues = pickle.load(f_myfile)  # variables come out in the order you put them in
        f_myfile.close()
    if qvalues:
        agent.qvs = qvalues
    else:
        sys.exit('FAILED TO READ TRAINING DATA')

def run_game():
    mean_shapes = 0
    max_score = []
    runs = 0
    for _ in range(20):
        runs += 1
        app = QApplication([])
        tetris = Tetris()
        app.exec_()
        if EXIT:
            break
        mean_shapes += tetris.shapesPlaced
        max_score.append(tetris.tboard.score)
        del app
    avg = sum(max_score) / len(max_score)
    print('Average Shapes: ', mean_shapes / runs)
    print('Max Score: ', max(max_score))
    print('Min Score: ', min(max_score))
    print('Average Score: ', avg)
    print('States in Q: ', len(agent.qvs))

def train_ai(episodes):
    run = 0
    mean_shapes = 0
    max_score = []
    for _ in range(episodes):
        run += 1
        app = QApplication([])
        tetris = Tetris()
        app.exec_()
        if EXIT:
            break
        mean_shapes += tetris.shapesPlaced
        max_score.append(tetris.tboard.score)
        del app
    avg = sum(max_score) / len(max_score)
    print('{} Runs'.format(run))
    print('Average Shapes: ', mean_shapes / run)
    print('Max Score: ', max(max_score))
    print('Average Score: ', avg)

EXIT = False
if __name__ == '__main__':
    # random.seed(32)
    import pickle
    import os
    episodes = 1000
    if len(sys.argv) <= 1:
        train = False
    elif len(sys.argv) == 2 and sys.argv[1] == 'train':
        train = True
    elif len(sys.argv) == 3 and sys.argv[1] == 'train':
        train = True
        episodes = int(sys.argv[2])
    else:
        train = False
    agent = QLearner(train=train)

    if agent.train:
        train_ai(episodes)
    else:
        # can use any pickle file
        get_trained_values()
        run_game()


    sys.exit()

