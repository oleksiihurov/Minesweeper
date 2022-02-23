# -----------------------------------------------------------------------------
# "Minesweeper" tribute to original online variations of the game:
# https://minesweeperonline.com
# https://minesweeper.online
# Copyright (c) Feb 2022 Oleksii Hurov
# -----------------------------------------------------------------------------

"""
(II) Input level abstraction.
Predefined parameters and constants.
"""


# System imports
from typing import Optional
from dataclasses import dataclass
from os import path
from json import load as json_load
from configparser import ConfigParser

# External imports
from numpy.random import randint, seed

# Project imports
from structures import START_RULE


# --- Config Parser -----------------------------------------------------------

config: Optional[ConfigParser] = None


def config_parser():
    """Parsing configuration file for initialization."""

    global config
    config = ConfigParser()
    config.read(path.join('assets', 'config.ini'))


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

    if config.has_option('Minefield', 'bombs percentage'):
        if config.getfloat('Minefield', 'bombs percentage') < 0.1 \
                or config.getfloat('Minefield', 'bombs percentage') > 99.9:
            raise ValueError("bombs percentage values have to be floating/"
                             "integer value in range from 0.1 to 99.9")


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
            BOMBS = round(_bombs_percentage / 100 * (ROWS * COLS))
            BOMBS = min(max(BOMBS, 1), (ROWS * COLS - 1))

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

    SPRITES_IMAGE = path.join(
        'assets', config.get('User Interface', 'graphics name') + '.png'
    )
    SPRITES_STENCIL = path.join(
        'assets', config.get('User Interface', 'graphics name') + '.json'
    )

    NIGHT_MODE = \
        config.getboolean('User Interface', 'night mode', fallback=False)

    FPS = config.getint('User Interface', 'frames per second', fallback=60)

    INDICATE_HOVER = \
        config.getboolean('User Interface', 'indicate hovering', fallback=True)

    # reading stencil for retrieving dimensions of the sprites
    with open(SPRITES_STENCIL, 'r') as json_file:
        _obj = json_load(json_file)
    _stencil = {k: v for k, v in _obj.items()}

    # dimensions
    SCALE = config.getint('User Interface', 'graphics scale', fallback=1)
    BASE_CELL_SIZE = max(
        _stencil['cell_empty'][2],
        _stencil['cell_empty'][3]
    )
    CELL_SIZE = BASE_CELL_SIZE * SCALE
    BORDER = SCALE * max(
        _stencil['frame_panel_top_left_corner'][2],
        _stencil['frame_panel_top_left_corner'][3]
    )

    if GAME.COLS >= 8:
        PADDING = 0
    else:
        PADDING = int((8 - GAME.COLS) / 2 * CELL_SIZE)

    DIGIT_WIDTH = SCALE * _stencil['digit_0'][2]

    PANEL_HEIGHT = SCALE * _stencil['frame_panel_interior'][3]
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
