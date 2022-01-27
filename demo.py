# -----------------------------------------------------------------------------
# "Minesweeper" tribute to original online variations of the game:
# https://minesweeperonline.com
# https://minesweeper.online
# Copyright (c) Jan 2022 Oleksii Hurov
# -----------------------------------------------------------------------------

"""
(V) Control level abstraction.
Main program. Entry point.
"""


# External imports
import pygame as pg

# Project imports
from config import CLICK, FACE, GAME, GUI
from logic import Logic
from graphics import Graphics


# --- Demo --------------------------------------------------------------------

class Demo:

    def __init__(self):

        # Setup process
        self.is_running = True  # running main program flag
        self.is_mousemotion = False  # flag of the mouse pointer movement event

        # Setup graphics
        self.logic = Logic(GAME)
        self.graphics = Graphics(GUI.RESOLUTION)

        # TODO Debug
        self.logic.click(CLICK.RIGHT, (1, 1))
        self.logic.click(CLICK.LEFT, (1, 2))

        self.logic.click(CLICK.LEFT, (6, 8))

        self.logic.click(CLICK.RIGHT, (6, 26))
        self.logic.click(CLICK.RIGHT, (8, 23))
        self.logic.click(CLICK.LEFT, (9, 24))

        self.logic.print_revealed_minefield()
        self.logic.print_covered_minefield()

    # --- Handle methods ------------------------------------------------------

    def loop_handler(self):
        """Resetting flags."""
        self.is_mousemotion = False
        return self.is_running

    def events_handler(self):
        """Reacting to the events from mouse/keyboard or window manipulation."""
        for event in pg.event.get():

            # events from main window
            if event.type == pg.QUIT:
                self.is_running = False
                break

            # events from mouse
            if event.type == pg.MOUSEMOTION:
                self.is_mousemotion = True

            # events from keyboard
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.is_running = False
                if event.key == pg.K_SPACE:
                    pass

    def actions_handler(self):
        """Program actions in the main loop."""
        self.graphics.draw_bombs_score(self.logic.get_bombs_score())
        self.graphics.draw_time_score(0)
        self.graphics.draw_face_button(FACE.READY)
        self.graphics.draw_minefield(self.logic.matrix_to_draw())

    def graphics_handler(self):
        """Redrawing the screen."""
        self.graphics.show()
