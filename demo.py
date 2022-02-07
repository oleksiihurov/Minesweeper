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
from config import EVENT, ACTION, FACE, GAME, GUI
from logic import Logic
from graphics import Graphics


# --- Demo --------------------------------------------------------------------

class Demo:

    def __init__(self):

        # Setup process
        self.is_running = True  # running main program flag
        self.is_mousemotion = False  # flag of the mouse pointer movement event
        self.mouse_position = None  # current mouse position
        self.event = None  # current occurred event from mouse or keys
        self.action = None  # current action performed based on event
        self.face_button_status = FACE.READY
        self.interaction_object = None

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
        self.event = None
        self.action = None
        return self.is_running

    def events_handler(self):
        """Reacting to the events from mouse/keyboard or window manipulation."""

        # Tracking both kinds of events: on press and release of mouse buttons.
        # Tracking only pressing events for keyboard keys.

        for event in pg.event.get():

            # events from main window
            if event.type == pg.QUIT:
                self.is_running = False
                break

            # events from mouse
            if event.type == pg.MOUSEMOTION:
                self.is_mousemotion = True
                self.mouse_position = pg.mouse.get_pos()

            left_button, middle_button, right_button = pg.mouse.get_pressed()
            if left_button:
                self.event = EVENT.LEFT_MOUSE_BUTTON_DOWN
                print(f'{self.event.name} at {self.mouse_position}')
            if right_button:
                self.event = EVENT.RIGHT_MOUSE_BUTTON_DOWN
                print(f'{self.event.name} at {self.mouse_position}')

            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:  # Left button click release
                    self.event = EVENT.LEFT_MOUSE_BUTTON_UP
                    print(f'{self.event.name} at {self.mouse_position}')
                if event.button == 3:  # Right button click release
                    self.event = EVENT.RIGHT_MOUSE_BUTTON_UP
                    print(f'{self.event.name} at {self.mouse_position}')

            # events from keyboard
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:  # Esc key
                    self.is_running = False
                if event.key == pg.K_SPACE:  # Space bar key press
                    self.event = EVENT.SPACE_BAR_DOWN
                    print(f'{self.event.name} at {self.mouse_position}')

    def actions_handler(self):
        """Program actions in the main loop."""

        # On pressing events we determining interaction (clickable) objects.
        # On releasing events we calling actions underneath objects.
        # That is done to give users ability to change their minds,
        # once performing the mouse click acton.

        # order is matter of the inner if's
        if self.event is not None:

            if self.graphics.face_button.collidepoint(self.mouse_position):
                self.interaction_object = self.graphics.face_button
                self.action = ACTION.TO_HOVER

                if self.event == EVENT.LEFT_MOUSE_BUTTON_DOWN:
                    self.face_button_status = FACE.PRESSED
                    self.action = ACTION.TO_PRESS
                if self.event == EVENT.LEFT_MOUSE_BUTTON_UP:
                    self.face_button_status = FACE.PRESSED
                    self.action = ACTION.TO_OPEN

            else:
                self.face_button_status = FACE.READY

            if self.graphics.minefield.collidepoint(self.mouse_position):
                self.interaction_object = self.graphics.minefield
                self.action = ACTION.TO_HOVER

                if self.event == EVENT.LEFT_MOUSE_BUTTON_DOWN:
                    self.action = ACTION.TO_PRESS
                if self.event == EVENT.RIGHT_MOUSE_BUTTON_DOWN:
                    pass

                if self.event == EVENT.LEFT_MOUSE_BUTTON_UP:
                    self.action = ACTION.TO_OPEN
                if self.event == EVENT.RIGHT_MOUSE_BUTTON_UP:
                    self.action = ACTION.TO_LABEL

                if self.event == EVENT.SPACE_BAR_DOWN:
                    if self.interaction_object == self.graphics.minefield:
                        self.action = ACTION.TO_REVEAL

        else:  # self.event is None
            self.interaction_object = None

    def reactions_handler(self):
        """Program reactions in the main loop."""

        # Performing actual reactions.

        # self.face_button_status = FACE.READY

        if self.action is not None:

            if self.interaction_object == self.graphics.face_button:
                if self.action == ACTION.TO_PRESS:
                    self.face_button_status = FACE.PRESSED
                if self.action == ACTION.TO_OPEN:
                    self.face_button_status = FACE.PRESSED
                    self.logic.new_game()
                    self.face_button_status = FACE.READY
                    print('new game')

            if self.interaction_object == self.graphics.minefield:
                if self.action == ACTION.TO_HOVER:
                    pass
                    # TODO
                if self.action == ACTION.TO_PRESS:
                    pass
                    # TODO
                if self.action == ACTION.TO_OPEN \
                        or self.action == ACTION.TO_LABEL \
                        or self.action == ACTION.TO_REVEAL:
                    print(f'Action to the cell: {self.graphics.convert_coords(self.mouse_position)}')
                    self.logic.perform_action(
                        self.action,
                        self.graphics.convert_coords(self.mouse_position)
                    )

    def graphics_handler(self):
        """Redrawing the screen."""
        self.graphics.draw_bombs_score(self.logic.get_bombs_score())
        self.graphics.draw_time_score(0)
        self.graphics.draw_face_button(self.face_button_status)
        self.graphics.draw_minefield(self.logic.matrix_to_draw())

        self.graphics.show()
