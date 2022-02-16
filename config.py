# -----------------------------------------------------------------------------
# "Minesweeper" tribute to original online variations of the game:
# https://minesweeperonline.com
# https://minesweeper.online
# Copyright (c) Feb 2022 Oleksii Hurov
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

class START_RULE(Enum):
    AS_IS = auto()  # As minefield generated - no changes
    NO_BOMB = auto()  # Once bomb appear under 1st click - it moved elsewhere
    EMPTY_CELL = auto()  # Under 1st click - entire 3*3 area cleared from bombs


class PRESET(Enum):
    CUSTOM = auto()  # custom size and bombs
    BEGINNER = auto()  # size: 9x9, bombs: 10
    INTERMEDIATE = auto()  # size: 16x16, bombs: 40
    EXPERT = auto()  # size: 30x16, bombs: 99


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


class FACE(Enum):
    READY = auto()  # regular smiley face button
    ACTIVE = auto()  # face while opening cell
    WON = auto()  # boss face on won game
    LOST = auto()  # sad face on lost game
    PRESSED = auto()  # pressed state of the button


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


# --- Dataclasses -------------------------------------------------------------

@dataclass
class GAME:
    """Set of constants for Game."""

    # matrix size
    ROWS = 16  # 1 <= ROWS <= 256
    COLS = 30  # 1 <= COLS <= 256

    START_RULE = START_RULE.EMPTY_CELL
    MARKS_PRESENT = True

    # BOMBS_PERCENTAGE = 0.150  # 0.001 <= PERCENTAGE <= 0.999
    # BOMBS = \
    #     min(
    #         max(
    #             round(BOMBS_PERCENTAGE * (ROWS * COLS)),
    #             1
    #         ),
    #         (ROWS * COLS - 1)
    #     )
    BOMBS = 99  # 1 <= BOMBS <= (ROWS * COLS - 1)

    # random seed for minefield generation
    # None - pure random. 42 - certain random seed for reproducible results.
    SEED = None
    if SEED is None:
        # generating random seed and preserving it
        SEED = randint(2_147_483_648)
    seed(SEED)


@dataclass
class GUI:
    """Set of constants for Graphics User Interface."""

    # Actual display fullscreen resolution
    # do not considering OS scale and layout:
    # (thanks to solution by)
    # https://gamedev.stackexchange.com/questions/105750/pygame-fullsreen-display-issue
    import ctypes
    ctypes.windll.user32.SetProcessDPIAware()

    # dimensions
    SCALE = 2  # 1 == 100%; 2 == 200%; etc. Must be integer and positive
    BASE_CELL_SIZE = 16  # 16x16 px
    CELL_SIZE = BASE_CELL_SIZE * SCALE
    BORDER = 10 * SCALE  # px

    if GAME.COLS >= 8:
        PADDING = 0
    else:
        PADDING = int((8 - GAME.COLS) / 2 * CELL_SIZE)

    PANEL_HEIGHT = 32 * SCALE  # px
    FIELD_HEIGHT = CELL_SIZE * GAME.ROWS
    SCREEN_HEIGHT = PANEL_HEIGHT + FIELD_HEIGHT + 3 * BORDER

    PANEL_WIDTH = CELL_SIZE * max(GAME.COLS, 8)
    FIELD_WIDTH = PANEL_WIDTH
    SCREEN_WIDTH = PANEL_WIDTH + 2 * BORDER

    PANEL_X_CENTER = SCREEN_WIDTH // 2
    PANEL_Y_CENTER = PANEL_HEIGHT // 2 + BORDER

    PANEL_X_TOP_LEFT = BORDER
    PANEL_Y_TOP_LEFT = BORDER

    FIELD_X_TOP_LEFT = BORDER
    FIELD_Y_TOP_LEFT = PANEL_HEIGHT + 2 * BORDER

    RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)

    DRAW_HOVERS = True
    FPS = 60


# --- Config Validation -------------------------------------------------------

def config_validation():

    if GAME.ROWS == 1 and GAME.COLS == 1:
        raise ValueError("Minefield size is too small.")
    if GAME.ROWS > 256 or GAME.COLS > 256:
        raise ValueError("Minefield size is too big.")
    if GAME.BOMBS < 1:
        raise ValueError("Too few bombs set for the minefield.")
    if GAME.BOMBS > GAME.ROWS * GAME.COLS + 1:
        raise ValueError("Too many bombs set for the minefield.")


config_validation()
