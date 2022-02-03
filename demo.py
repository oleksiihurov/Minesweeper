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
from config import ACTION, FACE, GAME, GUI
from logic import Logic
from graphics import Graphics


# --- Demo --------------------------------------------------------------------

class Demo:

    def __init__(self):

        # Setup process
        self.is_running = True  # running main program flag
        self.is_mousemotion = False  # flag of the mouse pointer movement event
        self.mouse_position = None  # current mouse position
        self.action = None  # current action performed on grabbing events stage

        # Setup graphics
        self.logic = Logic(GAME)
        self.graphics = Graphics(GUI.RESOLUTION)

        # TODO Debug
        self.logic.perform_action(ACTION.TO_LABEL, (1, 1))
        self.logic.perform_action(ACTION.TO_OPEN, (1, 2))

        self.logic.perform_action(ACTION.TO_OPEN, (6, 8))

        self.logic.perform_action(ACTION.TO_LABEL, (6, 26))
        self.logic.perform_action(ACTION.TO_LABEL, (8, 23))
        self.logic.perform_action(ACTION.TO_OPEN, (9, 24))

        self.logic.print_revealed_minefield()
        self.logic.print_covered_minefield()

    # --- Handle methods ------------------------------------------------------

    def loop_handler(self):
        """Resetting flags."""
        self.graphics.clock_tick()
        self.is_mousemotion = False
        self.action = None
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
                self.mouse_position = pg.mouse.get_pos()

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left button click press
                    self.action = ACTION.PRESSED
                    print(f'{self.action.name} at {self.mouse_position}')
                if event.button == 3:  # Right button click press
                    self.action = ACTION.TO_LABEL
                    print(f'{self.action.name} at {self.mouse_position}')

            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:  # Left button click release
                    self.action = ACTION.TO_OPEN
                    print(f'{self.action.name} at {self.mouse_position}')

            # events from keyboard
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:  # Esc key
                    self.is_running = False
                if event.key == pg.K_SPACE:  # Space bar key
                    self.action = ACTION.TO_REVEAL
                    print(f'{self.action.name} at {self.mouse_position}')

    def actions_handler(self):
        """Program actions in the main loop."""

        face_status = FACE.READY

        if self.action is not None:

            if self.graphics.face_button.collidepoint(self.mouse_position):
                face_status = FACE.PRESSED
                if self.action == ACTION.TO_OPEN:
                    self.logic.new_game()
                    print('new game')

            if self.graphics.minefield.collidepoint(self.mouse_position):
                print(f'cell: {self.graphics.convert_coords(self.mouse_position)}')
                self.logic.perform_action(
                    self.action,
                    self.graphics.convert_coords(self.mouse_position)
                )

        self.graphics.draw_bombs_score(self.logic.get_bombs_score())
        self.graphics.draw_time_score(0)
        self.graphics.draw_face_button(face_status)
        self.graphics.draw_minefield(self.logic.matrix_to_draw())

    def graphics_handler(self):
        """Redrawing the screen."""
        self.graphics.show()
