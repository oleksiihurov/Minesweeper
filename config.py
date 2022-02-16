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
from typing import Optional
from enum import Enum, auto
from dataclasses import dataclass
from os import path
from configparser import ConfigParser

# External imports
from numpy.random import randint, seed


# --- Types -------------------------------------------------------------------

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


# --- Config Parser -----------------------------------------------------------

config: Optional[ConfigParser] = None


def config_parser():
    """Parsing configuration file for initialization."""

    global config
    config = ConfigParser()
    config.read(path.join('assets', 'config.ini'))


# --- Config Validation -------------------------------------------------------

def config_validation():
    """Validating parameters for correctness from configuration file."""

    global config

    if config.getint('Minefield', 'rows') < 1 \
            or config.getint('Minefield', 'columns') < 1:
        raise ValueError("Minefield dimensions could not be negative.")
    if config.getint('Minefield', 'rows') == 1 \
            and config.getint('Minefield', 'columns') == 1:
        raise ValueError("Minefield size is too small.")
    if config.getint('Minefield', 'rows') > 256 \
            and config.getint('Minefield', 'columns') > 256:
        raise ValueError("Minefield size is too big.")

    if config.getint('Minefield', 'bombs') < 1:
        raise ValueError("Too few bombs set for the minefield.")
    if config.getint('Minefield', 'bombs') > \
            config.getint('Minefield', 'rows') * \
            config.getint('Minefield', 'columns') - 1:
        raise ValueError("Too many bombs set for the minefield.")

    if config.getfloat('Minefield', 'bombs percentage') < 0.1 \
            or config.getfloat('Minefield', 'bombs percentage') > 99.9:
        raise ValueError("bombs percentage values have to be "
                         "floating/integer value in range from 0.1 to 99.9")


# --- Executing Config --------------------------------------------------------

config_parser()
config_validation()


# --- Dataclasses -------------------------------------------------------------

@dataclass
class GAME:
    """Set of constants for Game."""

    # minefield
    if config.has_option('Minefield', 'preset'):
        ROWS, COLS, BOMBS = {
            'beginner': [9, 9, 10],
            'intermediate': [16, 16, 40],
            'expert': [16, 30, 99]
        }.get(config.get('Minefield', 'preset'))

    else:
        ROWS = config.getint('Minefield', 'rows', fallback=8)
        COLS = config.getint('Minefield', 'columns', fallback=8)
        BOMBS = config.getint('Minefield', 'bombs', fallback=1)

        _bombs_percentage = \
            config.getfloat('Minefield', 'bombs percentage', fallback=None)
        if _bombs_percentage is not None:
            BOMBS = \
                min(
                    max(
                        round(_bombs_percentage / 100 * (ROWS * COLS)), 1
                    ), (ROWS * COLS - 1)
                )

    # game parameters
    START_RULE = {
        'as is': START_RULE.AS_IS,
        'no bomb': START_RULE.NO_BOMB,
        'empty cell': START_RULE.EMPTY_CELL
    }.get(config.get('Game Parameters', 'starting rule'))

    MARKS_PRESENT = \
        config.getboolean('Game Parameters', 'marks present', fallback=False)

    _seed = config.get('Game Parameters', 'random seed', fallback=None)
    if _seed in [None, '']:
        # generating random seed and preserving it
        _seed = randint(2_147_483_648)
    seed(int(_seed))


@dataclass
class GUI:
    """Set of constants for Graphics User Interface."""

    # Actual display fullscreen resolution
    # do not considering OS scale and layout:
    # (thanks to solution by)
    # https://gamedev.stackexchange.com/questions/105750/pygame-fullsreen-display-issue
    import ctypes
    ctypes.windll.user32.SetProcessDPIAware()

    FPS = config.getint('User Interface', 'frames per second', fallback=60)

    INDICATE_HOVER = \
        config.getboolean('User Interface', 'indicate hovering', fallback=True)

    # dimensions
    SCALE = config.getint('User Interface', 'scale', fallback=1)
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
