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


# System imports
from enum import Enum, auto

# External imports
import numpy as np


# -----------------------------------------------------------------------------

class START(Enum):
    AS_IS = auto()  # as minefield generated
    NO_BOMB = auto()  # Once bomb appear under 1st click - it moved elsewhere
    EMPTY_CELL = auto()  # Under 1st click - entire 3*3 area cleared from bombs


class CLICK(Enum):
    LEFT = auto()  # to open
    RIGHT = auto()  # to flag
    MIDDLE = auto()  # to flag it or reveal its adjacent cells


# --- Logic class -------------------------------------------------------------

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

        self.is_started = False
        self.is_detonated = False
        self.click_position = (None, None)

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

    # --- Click methods -------------------------------------------------------

    def _first_click_left_button(self):
        pass
        # TODO

    def _click_left_button(self):
        if not self.opened[self.click_position]:
            if not self.flagged[self.click_position]:
                if not self.mined[self.click_position]:
                    self.opened[self.click_position] = True
                    if self.neighbours[self.click_position] == 0:
                        pass
                        # TODO to expand
                else:
                    # Game over
                    self.is_detonated = True

    def _click_right_button(self):
        if not self.opened[self.click_position]:
            self.flagged[self.click_position] = \
                not self.flagged[self.click_position]

    def _click_middle_button(self):
        pass
        # TODO

    def click(self, click: CLICK, click_position):
        self.click_position = click_position

        if click == CLICK.LEFT:
            if not self.is_started:
                self._first_click_left_button()
                self.is_started = True
            else:  # self.is_started == True
                self._click_left_button()
        elif click == CLICK.RIGHT:
            self._click_right_button()
        else:  # click == CLICK.MIDDLE
            self._click_middle_button()

    # -------------------------------------------------------------------------

    def matrix_to_draw(self):
        """
        0   : empty open cell, 0 neighbours
        1-8 : open cell with 1-8 neighbours
        9   : covered cell
        10  : flagged cell
        11  : bomb cell
        12  : wrong bomb cell
        13  : detonated cell
        """
        matrix = np.zeros((self.rows, self.cols), np.uint8)
        for row in range(self.rows):
            for col in range(self.cols):
                if self.opened[row, col]:
                    matrix[row, col] = self.neighbours[row, col]
                else:
                    if not self.is_detonated:
                        if self.flagged[row, col]:
                            matrix[row, col] = 10
                        else:
                            matrix[row, col] = 9
                    else:
                        if self.click_position == (row, col) \
                                and self.mined[row, col] \
                                and not self.flagged[row, col]:
                            matrix[row, col] = 13
                            break
                        if self.flagged[row, col] \
                                and not self.mined[row, col]:
                            matrix[row, col] = 12
                            break
                        if self.mined[row, col] \
                                and not self.flagged[row, col]:
                            matrix[row, col] = 11
                            break
                        if self.mined[row, col] \
                                and self.flagged[row, col]:
                            matrix[row, col] = 10
                            break
                        matrix[row, col] = 9
