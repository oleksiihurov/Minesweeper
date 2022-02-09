# -----------------------------------------------------------------------------
# "Minesweeper" tribute to original online variations of the game:
# https://minesweeperonline.com
# https://minesweeper.online
# Copyright (c) Feb 2022 Oleksii Hurov
# -----------------------------------------------------------------------------

"""
(III) Logic level abstraction.
Logic, primary purpose and calculations.
"""

# System imports
from typing import Optional
from time import time

# External imports
import numpy as np

# Project imports
from config import START_RULE, ACTION, GAME_STATE, CELL_TO_CODE


# --- Logic class -------------------------------------------------------------

class Logic:
    """All the Minesweeper game logic is here."""

    def __init__(self, game):
        # retrieving provided game parameters
        self.cols = game.COLS
        self.rows = game.ROWS
        self.start_rule = game.START_RULE
        self.marks_present = game.MARKS_PRESENT
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
        # boolean matrix layer of the marked/non-marked cells by player
        self.marked = np.empty(
            shape = (self.rows, self.cols),
            dtype = np.bool
        )
        # matrix layer which represents number of bombs nearby for each cell
        self.nearby = np.empty(
            shape = (self.rows, self.cols),
            dtype = np.uint8
        )

        # click position in format: (row, column)
        self.click_position: Optional[tuple[int, int]] = None
        self.cells_to_press: Optional[list[tuple[int, int]]] = None

        # game timer
        self.time_started = None
        self.time_score = None

        # creating new game
        self.game_state = GAME_STATE.NEW
        self.new_game()

    # --- Initialization methods ----------------------------------------------

    def clear_matrices(self):
        """Erasing all the matrix layers."""

        self.mined = np.zeros_like(self.mined)
        self.opened = np.zeros_like(self.opened)
        self.flagged = np.zeros_like(self.flagged)
        self.marked = np.zeros_like(self.marked)
        self.nearby = np.zeros_like(self.nearby)

    def reset_state(self):
        """Resetting state of the game to the initial."""

        self.click_position = None
        self.cells_to_press = None
        self.time_started = None
        self.time_score = None
        self.game_state = GAME_STATE.NEW

    def generate_bombs(self):
        """Filling up minefield by predefine number of bombs."""

        tmp = np.zeros(self.rows * self.cols, self.mined.dtype)
        tmp[:self.bombs] = True
        np.random.shuffle(tmp)
        self.mined = tmp.reshape((self.rows, self.cols))

    def calculate_nearby(self):
        """
        Calculating throughout the entire minefield
        number of neighbour bombs for each cell.
        """

        # creating temporary matrix with empty borders around mined field
        m = np.zeros((self.rows + 2, self.cols + 2), self.mined.dtype)
        m[1:self.rows+1, 1:self.cols+1] = self.mined

        # calculating number of nearby bombs, excluding self cell bomb
        for row in range(self.rows):
            for col in range(self.cols):
                self.nearby[row, col] = \
                    np.sum(m[row:row+3, col:col+3]) - m[row+1, col+1]

    def new_game(self):
        """New game with the same predefined conditions."""

        self.clear_matrices()
        self.reset_state()
        self.generate_bombs()
        self.calculate_nearby()

    # --- Operational methods -------------------------------------------------

    def find_neighbours(
            self,
            position: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """
        Compiling list of neighbour cells positions, taking into account
        possible edge and corner cases, where just part of cells exist.
        """

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

    def find_pressed_cells(self, position: tuple[int, int]):
        """
        Compiling list of cells positions to be reflected as pressed.
        In case of pressing nearby cell - compiling list of several cells.
        """

        if self.opened[position]:
            self.cells_to_press = []
            for neighbour in self.find_neighbours(position):
                if not self.opened[neighbour]:
                    if not self.flagged[neighbour]:
                        self.cells_to_press.append(neighbour)
        else:
            if self.flagged[position]:
                self.cells_to_press = []
            else:
                self.cells_to_press = [position]

    def count_nearby_closes(self, position: tuple[int, int]) -> int:
        """Return number of closed neighbour cells."""

        count = 0
        for neighbour in self.find_neighbours(position):
            if not self.opened[neighbour]:
                count += 1
        return count

    def count_nearby_flags(self, position: tuple[int, int]) -> int:
        """Return number of set flags on neighbour cells."""

        count = 0
        for neighbour in self.find_neighbours(position):
            if self.flagged[neighbour]:
                count += 1
        return count

    def to_open_neighbours(
            self,
            position: tuple[int, int],
            do_detonation_check = True,
            do_further_expansion = True
    ):
        """
        Opening the neighbour cells in case if set flags are correct.
        """

        # Step 1: checking for detonation due to wrong flags
        if do_detonation_check:
            for neighbour in self.find_neighbours(position):
                if self.flagged[neighbour] ^ self.mined[neighbour]:
                    # Game over
                    self.game_state = GAME_STATE.LOST
                    return

        # Step 2: than the actual opening of the neighbours
        for neighbour in self.find_neighbours(position):
            if not self.flagged[neighbour]:
                self.to_open_cell(neighbour)
                if do_further_expansion:
                    if self.nearby[neighbour] == 0:
                        self.expand(neighbour)

    def to_flag_neighbours(self, position: tuple[int, int]):
        """
        Flagging the neighbour cells in case if there are
        precise number of closed neighbours.
        """

        for neighbour in self.find_neighbours(position):
            if not self.opened[neighbour]:
                self.to_flag_cell(neighbour)

    def expand(self, position: tuple[int, int]):
        """
        Expending area in case opened cell has no bombs nearby.
        """

        # Step 1: forming list of positions of adjacent empty cells
        expanding_cells = {position: False}
        while False in expanding_cells.values():
            expanding_cells_to_add = dict()
            for cell_position, was_processed in expanding_cells.items():
                if not was_processed:
                    expanding_cells[cell_position] = True
                    for neighbour in self.find_neighbours(cell_position):
                        if self.nearby[neighbour] == 0:
                            if not self.flagged[neighbour]:
                                expanding_cells_to_add[neighbour] = False
            for empty_neighbour in expanding_cells_to_add:
                if expanding_cells.get(empty_neighbour) is None:
                    expanding_cells[empty_neighbour] = False

        # Step 2: opening all the neighbour cells to the list from Step 1
        for empty_cell in expanding_cells:
            if not self.flagged[empty_cell]:
                self.to_open_cell(empty_cell)
            self.to_open_neighbours(empty_cell, False, False)

    def to_open_cell(self, position: tuple[int, int]):
        """Opening cell."""
        self.opened[position] = True
        self.marked[position] = False

    def to_flag_cell(self, position: tuple[int, int]):
        """Flagging cell (even if there is mark)."""
        self.flagged[position] = True
        self.marked[position] = False

    def to_label_cell(self, position: tuple[int, int]):
        """Labeling cell by mark or flag."""
        if self.marks_present:
            if not self.flagged[position] and not self.marked[position]:
                self.flagged[position] = True
            elif self.flagged[position]:
                self.flagged[position] = False
                self.marked[position] = True
            elif self.marked[position]:
                self.marked[position] = False
        else:
            self.flagged[position] = not self.flagged[position]

    # --- Action methods ------------------------------------------------------

    def _before_first_action_to_open(self) -> bool:
        """
        Rearranging bombs under position of the first open click
        according to current start rule.
        Return True in case of successful performing - False otherwise.
        """

        if self.flagged[self.click_position]:
            return False

        if self.start_rule == START_RULE.AS_IS:
            pass

        elif self.start_rule == START_RULE.NO_BOMB:
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

        else:  # self.start_rule == START_RULE.EMPTY_CELL
            click_row, click_col = self.click_position

            # Step 1: validation of possibility to follow the rule
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
            # TODO consider case for 1x8 minefield

            # validation by exceeding number of bombs
            # TODO instead of exception - redirect to START.NO_BOMB case
            if self.bombs + covered_cells >= (self.rows * self.cols):
                raise ValueError(
                    "Too many bombs on the minefield "
                    "to meet the rule of empty cell "
                    "for the first open click."
                )

            # Step 2: performing the rule itself
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

        return True

    def action_to_open(self):
        """
        Action to open cell under click position.
        """

        if not self.opened[self.click_position]:
            if not self.flagged[self.click_position]:
                if not self.mined[self.click_position]:
                    self.to_open_cell(self.click_position)
                    if self.nearby[self.click_position] == 0:
                        self.expand(self.click_position)
                else:
                    # Game over
                    self.game_state = GAME_STATE.LOST
                    return
        else:
            self.action_to_reveal()

    def action_to_label(self):
        """
        Action to label cell by flag or mark under click position.
        """

        if not self.opened[self.click_position]:
            self.to_label_cell(self.click_position)
        else:
            if self.count_nearby_closes(self.click_position) == \
                    self.nearby[self.click_position]:
                self.to_flag_neighbours(self.click_position)

    def action_to_reveal(self):
        """
        Combined action to label cell or to reveal its adjacent cells
        under click position.
        """

        if not self.opened[self.click_position]:
            self.to_label_cell(self.click_position)
        else:
            if self.count_nearby_flags(self.click_position) == \
                    self.nearby[self.click_position]:
                self.to_open_neighbours(self.click_position)

    def perform_action(self, action: ACTION, click_position):
        """
        Method to call appropriate action by corresponding click.
        """

        self.click_position = click_position
        self.cells_to_press = None

        if action == ACTION.TO_OPEN:
            if self.game_state == GAME_STATE.NEW:
                if self._before_first_action_to_open():
                    self.game_state = GAME_STATE.GO
                    self.start_game_time()
            self.action_to_open()
        elif action == ACTION.TO_LABEL:
            self.action_to_label()
        elif action == ACTION.TO_REVEAL:
            self.action_to_reveal()

    # --- Checking game state methods -----------------------------------------

    def start_game_time(self):
        """Starting game timer."""
        self.time_started = time()
        self.time_score = 0

    def check_game_lost(self) -> bool:
        """Checking if the current state of the game is lost."""
        return True if self.game_state == GAME_STATE.LOST else False

    def check_game_won(self) -> bool:
        """Checking if the current state of the game is won."""

        # Counting closed cells - that's the only necessary criteria.
        # Set flags do not matter actually, they are optional
        # as soon as closed cells are the correct ones.
        # Otherwise player can't leave opened number of cells
        # by number of bombs without detonating.
        if self.rows * self.cols - np.sum(self.opened) == self.bombs:
            self.game_state = GAME_STATE.WON

            # game win postprocedure:
            # marking all the remaining closed cells by flags
            for row in range(self.rows):
                for col in range(self.cols):
                    if self.mined[row, col]:
                        self.flagged[row, col] = True

            return True
        else:
            return False

    # --- Export methods ------------------------------------------------------

    def print_revealed_minefield(self):
        """
        Debug print to console current state of revealed minefield.
        """

        print()
        lines = '┌─' + '──' * self.cols + '┐' + '\n'
        for row in range(self.rows):
            line = '│ '
            for col in range(self.cols):
                if self.mined[row, col]:
                    line += '*'
                else:
                    if self.nearby[row, col]:
                        line += str(self.nearby[row, col])
                    else:
                        line += ' '  # '·'
                line += ' '
            lines += line + '│' + '\n'
        lines += '└─' + '──' * self.cols + '┘'
        print(lines)

    def print_covered_minefield(self):
        """
        Debug print to console current state of covered minefield.
        """

        print()
        lines = '╔═' + '══' * self.cols + '╗' + '\n'
        for row in range(self.rows):
            line = '║ '
            for col in range(self.cols):
                if not self.opened[row, col]:
                    if self.flagged[row, col]:
                        line += '▒'
                    else:
                        line += '█'
                else:
                    if self.nearby[row, col]:
                        line += str(self.nearby[row, col])
                    else:
                        line += '·'
                line += ' '
            lines += line + '║' + '\n'
        lines += '╚═' + '══' * self.cols + '╝'
        print(lines)

    def get_pressed_cells(self) -> Optional[list[tuple[int, int]]]:
        """
        Return pressed cell/cells at the moment
        after calling method self.find_pressed_cells()
        """
        return self.cells_to_press

    def get_bombs_score(self) -> int:
        """Counting number of left bombs to flag on the minefield."""
        return int(self.bombs - np.sum(self.flagged))

    def get_time_score(self) -> int:
        """Proving time score of the current game."""

        if self.time_score is None:
            return 0
        else:
            if self.game_state == GAME_STATE.GO:
                self.time_score = time() - self.time_started
            return int(self.time_score)

    def get_matrix(self) -> np.ndarray:
        """
        Exporting minefield matrix with the definitions from CODE_TO_CELL.
        (suitable for drawing current state using separate graphics module)
        """

        matrix = np.zeros((self.rows, self.cols), np.uint8)

        for row in range(self.rows):
            for col in range(self.cols):
                if self.opened[row, col]:
                    matrix[row, col] = self.nearby[row, col]
                else:
                    matrix[row, col] = CELL_TO_CODE['closed']
                    if self.game_state != GAME_STATE.LOST:
                        if self.marked[row, col]:
                            matrix[row, col] = CELL_TO_CODE['marked']
                        if self.flagged[row, col]:
                            matrix[row, col] = CELL_TO_CODE['flagged']
                    else:
                        if self.mined[row, col]:
                            if self.flagged[row, col]:
                                matrix[row, col] = CELL_TO_CODE['flagged']
                            else:
                                matrix[row, col] = CELL_TO_CODE['mined']
                        else:
                            if self.marked[row, col]:
                                matrix[row, col] = CELL_TO_CODE['marked']
                            if self.flagged[row, col]:
                                matrix[row, col] = CELL_TO_CODE['not_mined']

                        if self.click_position == (row, col):
                            matrix[row, col] = CELL_TO_CODE['detonated']

        return matrix
