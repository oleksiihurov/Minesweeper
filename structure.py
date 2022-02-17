# -----------------------------------------------------------------------------
# "Minesweeper" tribute to original online variations of the game:
# https://minesweeperonline.com
# https://minesweeper.online
# Copyright (c) Feb 2022 Oleksii Hurov
# -----------------------------------------------------------------------------

"""
(II) Data level abstraction.
Data structures, types and interfaces.
"""


# System imports
from enum import Enum, auto


# --- Enums -------------------------------------------------------------------

class START_RULE(Enum):
    AS_IS = auto()  # As minefield generated - no changes
    NO_BOMB = auto()  # Once bomb appear under 1st click - it moved elsewhere
    EMPTY_CELL = auto()  # Under 1st click - entire 3*3 area cleared from bombs


class EVENT(Enum):
    MOUSE_MOTION = auto()
    LEFT_MOUSE_BUTTON_DOWN = auto()
    LEFT_MOUSE_BUTTON_UP = auto()
    RIGHT_MOUSE_BUTTON_DOWN = auto()
    RIGHT_MOUSE_BUTTON_UP = auto()
    SPACE_BAR_DOWN = auto()
    RIGHT_ARROW_KEY_DOWN = auto()
    LEFT_ARROW_KEY_DOWN = auto()
    UP_ARROW_KEY_DOWN = auto()
    DOWN_ARROW_KEY_DOWN = auto()


class ACTION(Enum):
    TO_HOVER = auto()  # focus the clickable element under mouse cursor
    TO_OPEN_PRESS = auto()  # highlight cells on pressing for opening
    TO_LABEL_PRESS = auto()  # highlight cells on pressing for labeling
    TO_OPEN = auto()  # to open cell
    TO_LABEL = auto()  # to flag or mark cell
    TO_REVEAL = auto()  # to label it or reveal its adjacent cells


class GAME_STATE(Enum):
    NEW = auto()  # game just created but not started
    GO = auto()  # game is started already and continues
    WON = auto()  # game is won and finished
    LOST = auto()  # # game is lost and finished


class FACE_STATE(Enum):
    READY = auto()  # regular smiley face button
    ACTIVE = auto()  # face while opening cell
    WON = auto()  # boss face on won game
    LOST = auto()  # sad face on lost game
    PRESSED = auto()  # pressed state of the button


# --- Other -------------------------------------------------------------------

CODE_TO_CELL = [
    'empty',
    'nearby_1',
    'nearby_2',
    'nearby_3',
    'nearby_4',
    'nearby_5',
    'nearby_6',
    'nearby_7',
    'nearby_8',
    'closed',
    'flagged',
    'marked',
    'marked_pressed',
    'mined',
    'not_mined',
    'detonated',
    'pressed'
]

CELL_TO_CODE = {k: v for v, k in enumerate(CODE_TO_CELL)}
