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
from config import GAME, GUI


# --- Graphics ----------------------------------------------------------------

class Graphics:
    """Setup of pygame graphics."""

    def __init__(self, resolution: tuple[int, int]):
        """Initializing pygame graphics."""

        # Initialization pygame display
        environ['SDL_VIDEO_CENTERED'] = '1'  # centering pygame window
        pg.init()
        self.screen = pg.display.set_mode(resolution)

        # Taskbar appearance
        pg.display.set_caption('Minesweeper')
        pg.display.set_icon(pg.image.load(path.join('assets', 'favicon.ico')))

        # Preparing sprites
        self.sprites: dict[str: pg.Surface] = dict()
        self.load_sprites()
        self.build_frame()

        # Initial drawing
        self.draw_bombs()
        self.draw_face_button()
        self.draw_time()

    # --- Sprites methods -----------------------------------------------------

    def load_sprites(self):
        """Compiling dictionary of separate sprite images from the file."""

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

        # TODO DEBUG
        # x = 0
        # y = 0
        # for i, sprite in enumerate(self.sprites.values()):
        #     rect: pg.Rect = sprite.get_rect()
        #     rect.move_ip(x, y)
        #     x += rect.width
        #     if i == 14:
        #         x = 0
        #         y = 100
        #     if i == 30:
        #         x = 0
        #         y = 200
        #     self.screen.blit(sprite, rect)

    def build_frame(self):
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

    # --- Drawing methods -----------------------------------------------------

    def draw_bombs(self):
        pass

    def draw_face_button(self):
        pass

    def draw_time(self):
        pass

    def draw_minefield(self, matrix: ndarray):
        pass

    # --- Operational methods -------------------------------------------------

    @staticmethod
    def show():
        """Reflecting all the drawings on the display."""
        pg.display.flip()
