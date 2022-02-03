# -----------------------------------------------------------------------------
# "Minesweeper" tribute to original online variations of the game:
# https://minesweeperonline.com
# https://minesweeper.online
# Copyright (c) Jan 2022 Oleksii Hurov
# -----------------------------------------------------------------------------

"""
(IV) Output level abstraction.
Presentation, graphics & UI, provided by pygame external module.
"""


# System imports
from os import environ, path
import json

# External imports
from numpy import ndarray
import pygame as pg

# Project imports
from config import FACE, CODE_TO_CELL, GAME, GUI


# --- Graphics ----------------------------------------------------------------

class Graphics:
    """Setup of pygame graphics."""

    def __init__(self, resolution: tuple[int, int]):
        """Initializing pygame graphics."""

        # Initialization pygame display
        environ['SDL_VIDEO_CENTERED'] = '1'  # centering pygame window
        pg.init()
        self.screen = pg.display.set_mode(resolution)

        # Setup process
        self.clock = pg.time.Clock()
        self.time_delta = None

        # Taskbar appearance
        pg.display.set_caption('Minesweeper')
        pg.display.set_icon(pg.image.load(path.join('assets', 'favicon.ico')))

        # Preparing sprites
        self.sprites: dict[str, pg.Surface] = dict()
        self.load_sprites()
        self.build_frame()

        # Defining clickable objects
        self.face_button = self.define_face_button_rect()
        self.minefield = self.define_minefield_rect()

    # --- Sprites methods -----------------------------------------------------

    def load_sprites(self):
        """
        Compiling dictionary of separate sprite images from the file.
        """

        # Step 1: reading sprites from files
        image = pg.image.load(path.join('assets', 'sprites.png')).convert()

        with open(path.join('assets', 'sprites.json'), 'r') as json_file:
            obj = json.load(json_file)
        template = {k: v for k, v in obj.items()}

        # Step 2: clipping separate sprites
        for name, clip in template.items():
            # making separate sprite surface
            rect = pg.Rect(clip)
            sprite = pg.Surface(rect.size)
            sprite.blit(image, (0, 0), rect)
            # rescaling if needed
            if GUI.SCALE != 1:
                w, h = rect.size
                sprite = pg.transform.scale(
                    sprite,
                    (w * GUI.SCALE, h * GUI.SCALE)
                )
            self.sprites[name] = sprite

    def build_frame(self):
        """
        Building full frame surface according to the minefield size,
        and drawing it on the screen.
        """

        frame = pg.Surface((GUI.SCREEN_WIDTH, GUI.SCREEN_HEIGHT))

        # frame line #1
        sprite = self.sprites['frame_panel_top_left_corner']
        rect = sprite.get_rect()
        rect.topleft = (0, 0)
        frame.blit(sprite, rect)

        sprite = self.sprites['frame_panel_top_edge']
        rect = sprite.get_rect()
        for col in range(GAME.COLS):
            rect.topleft = (GUI.BORDER + col * GUI.CELL_SIZE, 0)
            frame.blit(sprite, rect)

        sprite = self.sprites['frame_panel_top_right_corner']
        rect = sprite.get_rect()
        rect.topright = (GUI.SCREEN_WIDTH, 0)
        frame.blit(sprite, rect)

        # frame line #2
        sprite = self.sprites['frame_panel_left_edge']
        rect = sprite.get_rect()
        rect.topleft = (0, GUI.BORDER)
        frame.blit(sprite, rect)

        sprite = self.sprites['frame_panel_interior']
        rect = sprite.get_rect()
        for col in range(GAME.COLS):
            rect.topleft = (GUI.BORDER + col * GUI.CELL_SIZE, GUI.BORDER)
            frame.blit(sprite, rect)

        sprite = self.sprites['frame_panel_right_edge']
        rect = sprite.get_rect()
        rect.topright = (GUI.SCREEN_WIDTH, GUI.BORDER)
        frame.blit(sprite, rect)

        # frame line #3
        sprite = self.sprites['frame_field_top_left_corner']
        rect = sprite.get_rect()
        rect.topleft = (0, GUI.BORDER + GUI.PANEL_HEIGHT)
        frame.blit(sprite, rect)

        sprite = self.sprites['frame_field_top_edge']
        rect = sprite.get_rect()
        for col in range(GAME.COLS):
            rect.topleft = (
                GUI.BORDER + col * GUI.CELL_SIZE,
                GUI.BORDER + GUI.PANEL_HEIGHT
            )
            frame.blit(sprite, rect)

        sprite = self.sprites['frame_field_top_right_corner']
        rect = sprite.get_rect()
        rect.topright = (GUI.SCREEN_WIDTH, GUI.BORDER + GUI.PANEL_HEIGHT)
        frame.blit(sprite, rect)

        # frame line #4
        for row in range(GAME.ROWS):
            sprite = self.sprites['frame_field_left_edge']
            rect = sprite.get_rect()
            rect.topleft = (
                0,
                2 * GUI.BORDER + GUI.PANEL_HEIGHT + row * GUI.CELL_SIZE
            )
            frame.blit(sprite, rect)

            sprite = self.sprites['frame_field_interior']
            rect = sprite.get_rect()
            for col in range(GAME.COLS):
                rect.topleft = (
                    GUI.BORDER + col * GUI.CELL_SIZE,
                    2 * GUI.BORDER + GUI.PANEL_HEIGHT + row * GUI.CELL_SIZE
                )
                frame.blit(sprite, rect)

            sprite = self.sprites['frame_field_right_edge']
            rect = sprite.get_rect()
            rect.topright = (
                GUI.SCREEN_WIDTH,
                2 * GUI.BORDER + GUI.PANEL_HEIGHT + row * GUI.CELL_SIZE
            )
            frame.blit(sprite, rect)

        # frame line #5
        sprite = self.sprites['frame_field_bottom_left_corner']
        rect = sprite.get_rect()
        rect.topleft = (
            0,
            2 * GUI.BORDER + GUI.PANEL_HEIGHT + GAME.ROWS * GUI.CELL_SIZE
        )
        frame.blit(sprite, rect)

        sprite = self.sprites['frame_field_bottom_edge']
        rect = sprite.get_rect()
        for col in range(GAME.COLS):
            rect.topleft = (
                GUI.BORDER + col * GUI.CELL_SIZE,
                2 * GUI.BORDER + GUI.PANEL_HEIGHT + GAME.ROWS * GUI.CELL_SIZE
            )
            frame.blit(sprite, rect)

        sprite = self.sprites['frame_field_bottom_right_corner']
        rect = sprite.get_rect()
        rect.topright = (
            GUI.SCREEN_WIDTH,
            2 * GUI.BORDER + GUI.PANEL_HEIGHT + GAME.ROWS * GUI.CELL_SIZE
        )
        frame.blit(sprite, rect)

        self.screen.blit(frame, frame.get_rect())

    @staticmethod
    def convert_coords(mouse_coords: tuple[int, int]) -> tuple[int, int]:
        """
        Converting mouse coords (x, y)
        to minefield cell position (row, col).
        Presumably mouse cursor is inside minefield rect.
        """

        x, y = mouse_coords
        col = (x - GUI.FIELD_X_TOP_LEFT) // GUI.CELL_SIZE
        row = (y - GUI.FIELD_Y_TOP_LEFT) // GUI.CELL_SIZE
        return row, col

    # --- Defining methods ----------------------------------------------------

    def define_face_button_rect(self) -> pg.Rect:
        """
        Defining face button rect for checking colliding event once clicked.
        """

        sprite = self.sprites['face_button_ready']
        rect = sprite.get_rect()
        rect.midtop = (
            GUI.PANEL_X_CENTER,
            GUI.PANEL_Y_TOP_LEFT + 3 * GUI.SCALE
        )
        return rect

    @staticmethod
    def define_minefield_rect() -> pg.Rect:
        """
        Defining minefield rect for checking colliding event once clicked.
        """

        return pg.Rect(
            GUI.FIELD_X_TOP_LEFT,
            GUI.FIELD_Y_TOP_LEFT,
            GAME.COLS * GUI.CELL_SIZE,
            GAME.ROWS * GUI.CELL_SIZE
        )

    # --- Drawing methods -----------------------------------------------------

    def draw_face_button(self, face: FACE):
        """
        Reflecting current state of the face button.
        """

        sprite = self.sprites['face_button_' + face.name.lower()]
        rect = sprite.get_rect()
        rect.midtop = (
            GUI.PANEL_X_CENTER,
            GUI.PANEL_Y_TOP_LEFT + 3 * GUI.SCALE
        )
        self.screen.blit(sprite, rect)

    def draw_minefield(self, matrix: ndarray):
        """
        Reflecting current state of the minefield.
        """

        for row in range(GAME.ROWS):
            for col in range(GAME.COLS):
                sprite = self.sprites['cell_' + CODE_TO_CELL[matrix[row, col]]]
                rect = sprite.get_rect()
                rect.topleft = (
                    GUI.FIELD_X_TOP_LEFT + col * GUI.CELL_SIZE,
                    GUI.FIELD_Y_TOP_LEFT + row * GUI.CELL_SIZE
                )
                self.screen.blit(sprite, rect)

    def draw_bombs_score(self, bombs_score: int):
        """
        Reflecting current bombs score on the panel.
        """

        # compiling 3-symbol score number as a string
        if bombs_score >= 0:
            string_score = format(bombs_score % 1000, '0>3')
        else:
            string_score = '-' + format(abs(bombs_score) % 100, '0>2')

        # drawing corresponding digits
        for index, symbol in enumerate(string_score):
            sprite = self.sprites['digit_' + symbol]
            rect = sprite.get_rect()
            rect.topleft = (
                GUI.PANEL_X_TOP_LEFT + (5 + index * 13) * GUI.SCALE,
                GUI.PANEL_Y_TOP_LEFT + 4 * GUI.SCALE
            )
            self.screen.blit(sprite, rect)

    def draw_time_score(self, time_score: int):
        """
        Reflecting current time score on the panel.
        """

        # compiling 3-symbol score number as a string
        if 0 <= time_score <= 999:
            string_score = format(time_score, '0>3')
        else:
            string_score = '999'

        # drawing corresponding digits
        for index, symbol in enumerate(string_score):
            sprite = self.sprites['digit_' + symbol]
            rect = sprite.get_rect()
            rect.topright = (
                GUI.PANEL_X_TOP_LEFT + GUI.PANEL_WIDTH
                - (5 + (2 - index) * 13) * GUI.SCALE,
                GUI.PANEL_Y_TOP_LEFT + 4 * GUI.SCALE
            )
            self.screen.blit(sprite, rect)

    # --- Operational methods -------------------------------------------------

    def clock_tick(self):
        """Ticking clock."""
        self.time_delta = self.clock.tick(GUI.FPS)

    @staticmethod
    def show():
        """Reflecting all the drawings on the display."""
        pg.display.flip()
