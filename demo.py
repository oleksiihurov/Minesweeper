# -----------------------------------------------------------------------------
# "Minesweeper" tribute to original online variations of the game:
# https://minesweeperonline.com
# https://minesweeper.online
# Copyright (c) Feb 2022 Oleksii Hurov
# -----------------------------------------------------------------------------

"""
(V) Control level abstraction.
Main program. Entry point.
"""


# External imports
import pygame as pg

# Project imports
from config import EVENT, ACTION, GAME_STATE, FACE, GAME, GUI
from logic import Logic
from graphics import Graphics


# --- Demo --------------------------------------------------------------------

class Demo:

    def __init__(self):

        # Setup process
        self.is_running = True  # running main program flag

        self.is_mousemotion = False  # flag of the mouse pointer movement event
        self.mouse_coords = None  # current mouse position

        self.event = None  # current occurred event from mouse or keys
        self.action = None  # current action performed based on event

        self.press_action = None
        self.face_button_status = FACE.READY
        self.interaction_object = None

        # Setup graphics
        self.logic = Logic(GAME)
        self.graphics = Graphics(GUI.RESOLUTION)

        # TODO Debug
        # self.logic.perform_action(ACTION.TO_LABEL, (1, 1))
        # self.logic.perform_action(ACTION.TO_OPEN, (1, 2))
        #
        # self.logic.perform_action(ACTION.TO_OPEN, (6, 8))
        #
        # self.logic.perform_action(ACTION.TO_LABEL, (6, 26))
        # self.logic.perform_action(ACTION.TO_LABEL, (6, 26))
        # self.logic.perform_action(ACTION.TO_LABEL, (8, 23))
        # self.logic.perform_action(ACTION.TO_OPEN, (9, 24))
        #
        # self.logic.print_revealed_minefield()
        # self.logic.print_covered_minefield()

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
                return

            # events from mouse
            if event.type == pg.MOUSEMOTION:
                self.is_mousemotion = True
                self.mouse_coords = pg.mouse.get_pos()

            left_button, middle_button, right_button = pg.mouse.get_pressed()
            if left_button:  # Left button click press
                self.event = EVENT.LEFT_MOUSE_BUTTON_DOWN
                print(f'Event {self.event.name} at coords: {self.mouse_coords}')
            if right_button:  # Right button click press
                self.event = EVENT.RIGHT_MOUSE_BUTTON_DOWN
                print(f'Event {self.event.name} at coords: {self.mouse_coords}')

            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:  # Left button click release
                    self.event = EVENT.LEFT_MOUSE_BUTTON_UP
                    print(f'Event {self.event.name} at coords: {self.mouse_coords}')
                if event.button == 3:  # Right button click release
                    self.event = EVENT.RIGHT_MOUSE_BUTTON_UP
                    print(f'Event {self.event.name} at coords: {self.mouse_coords}')

            # events from keyboard
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:  # Esc key
                    self.is_running = False
                    return

                # if event.key == pg.K_F2:  # 'F2' key
                #     self.event = None
                #     self.new_game()
                #     return

                if event.key == pg.K_RIGHT:  # 'right arrow' key
                    self.event = EVENT.RIGHT_ARROW_KEY_DOWN
                if event.key == pg.K_LEFT:  # 'left arrow' key
                    self.event = EVENT.LEFT_ARROW_KEY_DOWN
                if event.key == pg.K_UP:  # 'up arrow' key
                    self.event = EVENT.UP_ARROW_KEY_DOWN
                if event.key == pg.K_DOWN:  # 'down arrow' key
                    self.event = EVENT.DOWN_ARROW_KEY_DOWN

                if event.key == pg.K_z:  # 'z' key
                    self.event = EVENT.LEFT_MOUSE_BUTTON_UP
                if event.key == pg.K_x:  # 'x' key
                    self.event = EVENT.RIGHT_MOUSE_BUTTON_UP

                if event.key == pg.K_SPACE:  # Space bar key press
                    self.event = EVENT.SPACE_BAR_DOWN
                    print(f'Event {self.event.name} at coords: {self.mouse_coords}')

    def actions_handler(self):
        """Program actions in the main loop."""

        # On pressing events we determining interaction (clickable) objects.
        # On releasing events we calling actions underneath objects.
        # That is done to give users ability to change their minds,
        # once performing the mouse click acton.

        if self.event is not None:

            if self.graphics.face_button.collidepoint(self.mouse_coords):
                self.interaction_object = self.graphics.face_button
                self.action = ACTION.TO_HOVER

                if self.event == EVENT.LEFT_MOUSE_BUTTON_DOWN:
                    self.action = ACTION.TO_OPEN_PRESS
                if self.event == EVENT.LEFT_MOUSE_BUTTON_UP:
                    self.action = ACTION.TO_OPEN

            else:
                if self.logic.game_state == GAME_STATE.NEW \
                        or self.logic.game_state == GAME_STATE.GO:
                    self.face_button_status = FACE.READY
                elif self.logic.game_state == GAME_STATE.WON:
                    self.face_button_status = FACE.WON
                elif self.logic.game_state == GAME_STATE.LOST:
                    self.face_button_status = FACE.LOST

            if self.graphics.minefield.collidepoint(self.mouse_coords):
                self.interaction_object = self.graphics.minefield
                self.action = ACTION.TO_HOVER

                if self.event == EVENT.RIGHT_ARROW_KEY_DOWN \
                        or self.event == EVENT.LEFT_ARROW_KEY_DOWN \
                        or self.event == EVENT.UP_ARROW_KEY_DOWN \
                        or self.event == EVENT.DOWN_ARROW_KEY_DOWN:
                    self.move_mouse_cursor()

                if self.event == EVENT.LEFT_MOUSE_BUTTON_DOWN:
                    self.action = ACTION.TO_OPEN_PRESS
                if self.event == EVENT.RIGHT_MOUSE_BUTTON_DOWN:
                    self.action = ACTION.TO_LABEL_PRESS

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

        if self.action is not None:

            if self.interaction_object == self.graphics.face_button:
                if self.action == ACTION.TO_HOVER:
                    pass
                    # TODO
                elif self.action == ACTION.TO_OPEN_PRESS:
                    self.face_button_status = FACE.PRESSED
                elif self.action == ACTION.TO_OPEN:
                    self.new_game()

            if self.logic.game_state == GAME_STATE.NEW \
                    or self.logic.game_state == GAME_STATE.GO:
                if self.interaction_object == self.graphics.minefield:
                    if self.action == ACTION.TO_HOVER:
                        pass
                        # TODO
                    elif self.action == ACTION.TO_OPEN_PRESS \
                            or self.action == ACTION.TO_LABEL_PRESS:
                        self.reaction_on_press()
                    elif self.action == ACTION.TO_OPEN \
                            or self.action == ACTION.TO_LABEL \
                            or self.action == ACTION.TO_REVEAL:
                        self.reaction_on_release()

    def graphics_handler(self):
        """Redrawing the screen."""
        self.graphics.draw_face_button(self.face_button_status)
        self.graphics.draw_bombs_score(self.logic.get_bombs_score())
        self.graphics.draw_time_score(self.logic.get_time_score())
        self.graphics.draw_minefield(self.logic.get_matrix())
        self.graphics.draw_pressed_cells(
            self.logic.get_pressed_cells(),
            self.press_action
        )

        self.graphics.show()

    # --- Gaming methods ------------------------------------------------------

    def move_mouse_cursor(self):
        """
        Moving mouse cursor according
        to the direction of pressed arrow keys.
        """

        if self.event == EVENT.RIGHT_ARROW_KEY_DOWN:
            direction = 'right'
        elif self.event == EVENT.LEFT_ARROW_KEY_DOWN:
            direction = 'left'
        elif self.event == EVENT.UP_ARROW_KEY_DOWN:
            direction = 'up'
        elif self.event == EVENT.DOWN_ARROW_KEY_DOWN:
            direction = 'down'
        else:
            direction = None

        pg.mouse.set_pos(
            self.graphics.new_mouse_coords(self.mouse_coords, direction)
        )

    def new_game(self):
        """Procedure for the new game."""

        print('New Game')
        self.logic.new_game()
        self.face_button_status = FACE.READY

    def reaction_on_press(self):
        """Performing reaction on press input buttons/keys."""

        print(f'Action {self.action.name} to the cell at position: '
              f'{self.graphics.convert_coords(self.mouse_coords)}')
        self.face_button_status = FACE.ACTIVE
        self.press_action = self.action
        self.logic.find_pressed_cells(
            self.graphics.convert_coords(self.mouse_coords),
            self.press_action
        )

    def reaction_on_release(self):
        """Performing reaction on release input buttons/keys."""

        print(f'Action {self.action.name} to the cell at position: '
              f'{self.graphics.convert_coords(self.mouse_coords)}')
        self.press_action = None
        self.logic.perform_action(
            self.action,
            self.graphics.convert_coords(self.mouse_coords)
        )
        if self.logic.check_game_lost():
            self.face_button_status = FACE.LOST
        if self.logic.check_game_won():
            self.face_button_status = FACE.WON
