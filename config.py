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

# External imports
from numpy.random import randint, seed


# --- Types -------------------------------------------------------------------

class START(Enum):
    AS_IS = auto()  # As minefield generated - no changes
    NO_BOMB = auto()  # Once bomb appear under 1st click - it moved elsewhere
    EMPTY_CELL = auto()  # Under 1st click - entire 3*3 area cleared from bombs


class PRESET(Enum):
    CUSTOM = auto()  # custom size and bombs
    BEGINNER = auto()  # size: 9x9, bombs: 10
    INTERMEDIATE = auto()  # size: 16x16, bombs: 40
    EXPERT = auto()  # size: 30x16, bombs: 99


class CLICK(Enum):
    LEFT = auto()  # to open
    RIGHT = auto()  # to flag
    MIDDLE = auto()  # to flag it or reveal its adjacent cells


# --- Dataclasses -------------------------------------------------------------

@dataclass
class GAME:
    """Set of constants for Game."""

    # matrix size
    ROWS = 16  # 2 <= ROWS <= 32
    COLS = 30  # 2 <= COLS <= 32

    RULE = START.AS_IS

    # BOMBS_PERCENTAGE = 0.150  # 0.001 <= PERCENTAGE <= 0.999
    # BOMBS = max(round(BOMBS_PERCENTAGE * (ROWS * COLS)), 1)
    BOMBS = 99

    # random seed for minefield generation
    # None - pure random. 42 - certain random seed for reproducible results.
    SEED = 42
    if SEED is None:
        # generating random seed and preserving it
        SEED = randint(2_147_483_648)
    seed(SEED)


# -----------------------------------------------------------------------------

def config_validation():

    if GAME.ROWS < 2 or GAME.COLS < 2:
        raise ValueError("Minefield size is too narrow.")
    if GAME.ROWS > 32 or GAME.COLS > 32:
        raise ValueError("Minefield size is too wide.")
    if GAME.BOMBS + 1 >= GAME.ROWS * GAME.COLS:
        raise ValueError("Too many bombs set for the minefield.")


config_validation()
