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
from dataclasses import dataclass


@dataclass
class GAME:
    """Set of constants for Game."""

    # matrix size
    ROWS = 5  # 2 <= ROWS <= 32
    COLS = 7  # 2 <= COLS <= 32

    # BOMBS = 10

    BOMBS_PERCENTAGE = 0.200  # 0.001 <= PERCENTAGE <= 0.999
    BOMBS = int(BOMBS_PERCENTAGE * (ROWS * COLS))
