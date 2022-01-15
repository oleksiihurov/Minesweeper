# -----------------------------------------------------------------------------
# "Minesweeper" tribute to original online variations of the game:
# https://minesweeperonline.com
# https://minesweeper.online
# Copyright (c) Jan 2022 Oleksii Hurov
# -----------------------------------------------------------------------------

"""
(III) Logic level abstraction.
Logic, primary purpose and calculations.
"""


# External imports
import numpy as np


class Logic:

    def __init__(self, game):
        self.cols = game.COLS
        self.rows = game.ROWS
        self.bombs = game.BOMBS

        self.mined = np.empty(
            shape = (self.rows, self.cols),
            dtype = np.bool
        )
        self.opened = np.empty(
            shape = (self.rows, self.cols),
            dtype = np.bool
        )
        self.flagged = np.empty(
            shape = (self.rows, self.cols),
            dtype = np.bool
        )
        self.neighbours = np.empty(
            shape = (self.rows, self.cols),
            dtype = np.uint8
        )

    # --- Matrix initialization methods ---------------------------------------

    def clear_matrices(self):
        # self.mined = np.zeros((self.rows, self.cols), np.bool)
        self.mined = np.zeros_like(self.mined)
        self.opened = np.zeros_like(self.opened)
        self.flagged = np.zeros_like(self.flagged)
        self.neighbours = np.zeros_like(self.neighbours)

    def generate_bombs(self):
        tmp = np.zeros(self.rows * self.cols, self.mined.dtype)
        tmp[:self.bombs] = True
        np.random.shuffle(tmp)
        self.mined = tmp.reshape((self.rows, self.cols))

    def calculate_neighbours(self):
        # creating temporary matrix with empty borders around mined field
        m = np.zeros((self.rows + 2, self.cols + 2), self.mined.dtype)
        m[1:self.rows+1, 1:self.cols+1] = self.mined
        # calculating number of neighbour bombs, excluding self cell bomb
        for row in range(self.rows):
            for col in range(self.cols):
                self.neighbours[row, col] = \
                    np.sum(m[row:row+3, col:col+3]) - m[row+1, col+1]

    def new_game(self):
        self.clear_matrices()
        self.generate_bombs()
        self.calculate_neighbours()

        print(self.mined)
        print(self.neighbours)
