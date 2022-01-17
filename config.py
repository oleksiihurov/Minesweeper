# -----------------------------------------------------------------------------
# "Minesweeper" tribute to original online variations of the game:
# https://minesweeperonline.com
# https://minesweeper.online
# Copyright (c) Jan 2022 Oleksii Hurov
# -----------------------------------------------------------------------------

"""
(I) Input level abstraction.
Predefined parameters, constants and types.
"""


# System imports
from enum import Enum, auto
from dataclasses import dataclass


# --- Types -------------------------------------------------------------------

class START(Enum):
    AS_IS = auto()  # As minefield generated - no changes
    NO_BOMB = auto()  # Once bomb appear under 1st click - it moved elsewhere
    EMPTY_CELL = auto()  # Under 1st click - entire 3*3 area cleared from bombs


class CLICK(Enum):
    LEFT = auto()  # to open
    RIGHT = auto()  # to flag
    MIDDLE = auto()  # to flag it or reveal its adjacent cells


# --- Dataclasses -------------------------------------------------------------

@dataclass
class GAME:
    """Set of constants for Game."""

    # matrix size
    ROWS = 5  # 2 <= ROWS <= 32
    COLS = 7  # 2 <= COLS <= 32

    RULE = START.AS_IS

    BOMBS_PERCENTAGE = 0.200  # 0.001 <= PERCENTAGE <= 0.999
    BOMBS = int(BOMBS_PERCENTAGE * (ROWS * COLS))
    # BOMBS = 10


# -----------------------------------------------------------------------------

def config_validation():

    if GAME.ROWS < 2 or GAME.COLS < 2:
        raise ValueError("Minefield size is too narrow.")
    if GAME.ROWS > 32 or GAME.COLS > 32:
        raise ValueError("Minefield size is too wide.")
    if GAME.BOMBS + 1 >= GAME.ROWS * GAME.COLS:
        raise ValueError("Too many bombs set for the minefield.")


config_validation()
