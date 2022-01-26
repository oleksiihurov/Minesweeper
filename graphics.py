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
from config import GUI


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

        self.sprites = dict()
        self.load_sprites()

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
            surface = pg.Surface(rect.size)
            surface.blit(image, (0, 0), rect)
            # rescaling if needed
            if GUI.SCALE != 1:
                w, h = rect.size
                surface = pg.transform.scale(
                    surface,
                    (w * GUI.SCALE, h * GUI.SCALE)
                )
            self.sprites[name] = surface

        # TODO DEBUG
        x = 0
        y = 0
        for i, sprite in enumerate(self.sprites.values()):
            rect: pg.Rect = sprite.get_rect()
            rect.move_ip(x, y)
            x += rect.width
            if i == 14:
                x = 0
                y = 100
            if i == 30:
                x = 0
                y = 200
            self.screen.blit(sprite, rect)

    @staticmethod
    def show():
        """Reflecting all the drawings on the display."""
        pg.display.flip()
