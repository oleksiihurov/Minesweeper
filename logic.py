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

# project imports
from config import START, CLICK


# --- Logic class -------------------------------------------------------------

class Logic:
    """All the Minesweeper game logic is here."""

    def __init__(self, game):
        # retrieving provided game parameters
        self.cols = game.COLS
        self.rows = game.ROWS
        self.rule = game.RULE
        self.bombs = game.BOMBS

        # boolean matrix layer of the present bombs on the minefield
        self.mined = np.empty(
            shape = (self.rows, self.cols),
            dtype = np.bool
        )
        # boolean matrix layer of the revealed/covered minefield cells
        self.opened = np.empty(
            shape = (self.rows, self.cols),
            dtype = np.bool
        )
        # boolean matrix layer of the flagged/non-flagged cells by player
        self.flagged = np.empty(
            shape = (self.rows, self.cols),
            dtype = np.bool
        )
        # matrix layer which represents number of bombs nearby for each cell
        self.nearby = np.empty(
            shape = (self.rows, self.cols),
            dtype = np.uint8
        )

        # flags
        self.is_started = False
        self.is_detonated = False

        # click position in format: (row, column)
        self.click_position: tuple[int, int] = (0, 0)

    # --- Matrix initialization methods ---------------------------------------

    def clear_matrices(self):
        # self.mined = np.zeros((self.rows, self.cols), np.bool)
        self.mined = np.zeros_like(self.mined)
        self.opened = np.zeros_like(self.opened)
        self.flagged = np.zeros_like(self.flagged)
        self.nearby = np.zeros_like(self.nearby)

    def generate_bombs(self):
        tmp = np.zeros(self.rows * self.cols, self.mined.dtype)
        tmp[:self.bombs] = True
        np.random.shuffle(tmp)
        self.mined = tmp.reshape((self.rows, self.cols))

    def calculate_nearby(self):
        # creating temporary matrix with empty borders around mined field
        m = np.zeros((self.rows + 2, self.cols + 2), self.mined.dtype)
        m[1:self.rows+1, 1:self.cols+1] = self.mined
        # calculating number of nearby bombs, excluding self cell bomb
        for row in range(self.rows):
            for col in range(self.cols):
                self.nearby[row, col] = \
                    np.sum(m[row:row+3, col:col+3]) - m[row+1, col+1]

    def new_game(self):
        self.clear_matrices()
        self.generate_bombs()
        self.calculate_nearby()

    # -------------------------------------------------------------------------

    def find_neighbours(self, position: tuple[int, int]):
        neighbour_positions = list()

        row, col = position
        top = (row - 1 >= 0)
        bottom = (row + 1 < self.rows)
        left = (col - 1 >= 0)
        right = (col + 1 < self.cols)

        if top:
            neighbour_positions.append((row - 1, col))
        if bottom:
            neighbour_positions.append((row + 1, col))
        if left:
            neighbour_positions.append((row, col - 1))
        if right:
            neighbour_positions.append((row, col + 1))
        if top and left:
            neighbour_positions.append((row - 1, col - 1))
        if top and right:
            neighbour_positions.append((row - 1, col + 1))
        if bottom and left:
            neighbour_positions.append((row + 1, col - 1))
        if bottom and right:
            neighbour_positions.append((row + 1, col + 1))

        return neighbour_positions

    def expand(self, position: tuple[int, int]):

        # Step 1: forming list of positions of adjacent empty cells
        expanding_cells = {position: False}
        while False in expanding_cells.values():
            for cell_position, was_processed in expanding_cells.items():
                if not was_processed:
                    expanding_cells[cell_position] = True
                    for neighbour in self.find_neighbours(cell_position):
                        if self.nearby[neighbour] == 0:
                            if expanding_cells.get(neighbour) is None:
                                expanding_cells[neighbour] = False

        # Step 2: opening all the neighbour cells to the list from Step 1
        # TODO

    # --- Click methods -------------------------------------------------------

    def _before_first_click_left_button(self):
        """
        Rearranging bombs under position of the first open click
        according to current game rule.
        """

        if self.flagged[self.click_position]:
            return

        if self.rule == START.AS_IS:
            pass

        elif self.rule == START.NO_BOMB:
            if self.mined[self.click_position]:
                while self.mined[(
                        new_bomb_position := (
                                np.random.randint(self.rows),
                                np.random.randint(self.cols)
                        )
                )]:
                    pass
                self.mined[new_bomb_position] = True
                self.mined[self.click_position] = False
                self.calculate_nearby()

        else:  # self.rule == START.EMPTY_CELL
            click_row, click_col = self.click_position

            covered_cells = 9
            # first click position is at the corner of the minefield:
            if self.click_position == (self.rows - 1, self.cols - 1) \
                    or self.click_position == (0, self.cols - 1) \
                    or self.click_position == (self.rows - 1, 0) \
                    or self.click_position == (0, 0):
                covered_cells = 4
            else:
                # first click position is at the edge of the minefield:
                if click_row == 0 or click_row == self.rows - 1 \
                        or click_col == 0 or click_col == self.cols - 1:
                    covered_cells = 6

            # validation by exceeding number of bombs
            if self.bombs + covered_cells >= (self.rows * self.cols):
                raise ValueError(
                    "Too many bombs on the minefield "
                    "to meet the rule of empty cell "
                    "for the first open click."
                )

            while self.nearby[self.click_position] != 0:
                for i in range(self.nearby[self.click_position]):
                    while self.mined[(
                            new_bomb_position := (
                                    np.random.randint(self.rows),
                                    np.random.randint(self.cols)
                            )
                    )]:
                        pass
                    self.mined[new_bomb_position] = True
                self.mined[
                    max(click_row - 1, 0):min(click_row + 2, self.rows + 1),
                    max(click_col - 1, 0):min(click_col + 2, self.cols + 1)
                ] = False
                self.calculate_nearby()

    def _click_left_button(self):
        if not self.opened[self.click_position]:
            if not self.flagged[self.click_position]:
                if not self.mined[self.click_position]:
                    self.opened[self.click_position] = True
                    if self.nearby[self.click_position] == 0:
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
                self._before_first_click_left_button()
                self.is_started = True
            self._click_left_button()
        elif click == CLICK.RIGHT:
            self._click_right_button()
        else:  # click == CLICK.MIDDLE
            self._click_middle_button()

    # --- Checking game state methods -----------------------------------------

    def is_game_won(self) -> bool:
        """
        Checking if the current state of the game is won.
        """
        pass
        # TODO

    def game_won_postprocedure(self):
        """
        Presumably: self.is_game_won() == True
        Marking all the remaining closed cells by flags.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if self.mined[row, col]:
                    self.flagged[row, col] = True

    def is_game_lost(self) -> bool:
        """
        Checking if the current state of the game is lost.
        """
        return True if self.is_detonated else False

    # -------------------------------------------------------------------------

    def print_matrix(self):
        print()
        lines = '┌─' + '──' * self.cols + '┐' + '\n'
        for row in range(self.rows):
            line = '│ '
            for col in range(self.cols):
                if self.mined[row, col]:
                    line += '█'
                else:
                    if self.nearby[row, col]:
                        line += str(self.nearby[row, col])
                    else:
                        line += '·'
                line += ' '
            lines += line + '│' + '\n'
        lines += '└─' + '──' * self.cols + '┘'
        print(lines)

    def matrix_to_draw(self) -> np.ndarray:
        """
        Exporting minefield matrix with the following definitions:
        (suitable for drawing current state using separate graphics module)

        0   : empty open cell, 0 nearby bombs
        1-8 : open cell with 1-8 nearby bombs
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
                    matrix[row, col] = self.nearby[row, col]
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

        return matrix
