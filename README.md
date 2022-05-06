# Tetris Game

Python implementation of Tetris with a Q-Learning AI.

Need python3, PyQt5, Pickle, and NumPy to be installed.
Python 3 can be installed from https://www.python.org/downloads/
The necessary packages can be installed with pip:
  pip install pyqt5
  pip install pickle
  pip install numpy

* `tetris_game.py` is the main application.
* `tetris_model.py` is the data model.
* `tetrisAgent.py` contains the Q-Learning agent

tetris_game.py:
  
  The tetris_game file sets the basis for playing the game.
  It updates the window, shape placement, colors, external 
  controls, and all general data needed to play. In this file, 
  we provide ways to analyze the performance data ourselves, 
  which would require an additional installation of pandas 
  (pip install pandas).

tetris_agent.py:

  The tetris_agent file establishes the Tetris-playing agent, 
  that uses reinforcement learning. This file sets up the
  state space that the agent is playing in, methods to find
  block heights and their relational differences, holes,
  contours, and the necessary Q-Learning methods.
  
tetris_model.py:

  The tetris_model file is the foundation for how the game operates.
  It establishes the shapes and their coordinates, bounding offsets,
  the backboard description, and possible moves.

Run `tetris_game.py` to watch the AI play.
Press `P` to pause the game.
Pres `esc` to quit the game where it's at.

```shell
$ python3 tetris_game.py
```
