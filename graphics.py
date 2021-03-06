# -----------------------------------------------------------------------------
# "Minesweeper" tribute to original online variations of the game:
# https://minesweeperonline.com
# https://minesweeper.online
# Copyright (c) Feb 2022 Oleksii Hurov
# -----------------------------------------------------------------------------

"""
(IV) Output level abstraction.
Presentation, graphics & UI, provided by pygame external module.
"""


# System imports
from os import environ, path
from json import load as json_load
from typing import Optional

# External imports
from numpy import ndarray
import pygame as pg

# Project imports
from config import GAME, GUI
from structures import ACTION, FACE_STATE, CODE_TO_CELL


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
        if GUI.INDICATE_HOVER:
            self.make_hover_sprites()
        if GAME.COLS < 8:
            self.make_grid_line_sprite()

        # Preparing and drawing frame
        self.frame = pg.Surface((GUI.SCREEN_WIDTH, GUI.SCREEN_HEIGHT))
        self.build_frame()
        self.draw_frame()

        # Defining clickable objects
        self.face_button = self.define_face_button_rect()
        self.minefield = self.define_minefield_rect()

    # --- Sprites methods -----------------------------------------------------

    def load_sprites(self):
        """
        Compiling dictionary of separate sprite images from the file.
        """

        # Step 1: reading sprites from files
        image = pg.image.load(GUI.SPRITES_IMAGE).convert()

        with open(GUI.SPRITES_STENCIL, 'r') as json_file:
            obj = json_load(json_file)
        stencil = {k: v for k, v in obj.items()}

        # Step 2: clipping separate sprites
        for name, clip in stencil.items():

            # making separate sprite surface
            rect = pg.Rect(clip)
            sprite = pg.Surface(rect.size)
            sprite.blit(image, (0, 0), rect)

            # applying night mode for all sprites
            if GUI.NIGHT_MODE:
                darken = 140
                sprite.fill(
                    (darken, darken, darken),
                    special_flags = pg.BLEND_RGB_MULT
                )

            # rescaling if needed
            if GUI.SCALE != 1:
                w, h = rect.size
                sprite = pg.transform.scale(
                    sprite,
                    (w * GUI.SCALE, h * GUI.SCALE)
                )

            self.sprites[name] = sprite

    def make_grid_line_sprite(self):
        """
        Making additional sprite for vertical grid line
        in case of narrow minefield used (GAME.COLS < 8).
        """

        cell_empty = self.sprites['cell_empty']
        cell_empty_rect = cell_empty.get_rect()
        cell_empty_rect.width = 1 * GUI.SCALE

        sprite = pg.Surface(cell_empty_rect.size)
        sprite.blit(cell_empty, (0, 0), cell_empty_rect)
        self.sprites['cell_grid_line'] = sprite

    def make_hover_sprites(self):
        """
        Making additional sprites from existing for clickable UI elements.
        """

        brighten = 20
        sprites_to_be_hovered = [
            'face_button_ready',
            'face_button_lost',
            'face_button_won',

            'cell_empty',
            'cell_nearby_1',
            'cell_nearby_2',
            'cell_nearby_3',
            'cell_nearby_4',
            'cell_nearby_5',
            'cell_nearby_6',
            'cell_nearby_7',
            'cell_nearby_8',
            'cell_closed',
            'cell_flagged',
            'cell_marked'
        ]
        name_suffix = '_hovered'

        for name in sprites_to_be_hovered:
            self.sprites[name + name_suffix] = self.sprites[name].copy()
            self.sprites[name + name_suffix].fill(
                (brighten, brighten, brighten),
                special_flags = pg.BLEND_RGB_ADD
            )

    def put_sprite_using_anchor(
            self, surface: pg.Surface,
            name: str,
            anchor: str,
            x: int, y: int
    ):
        """
        Drawing sprite by its name on coordinates (x, y) of the surface,
        using anchor point for the rect.
        """

        sprite = self.sprites[name]
        rect = sprite.get_rect()
        if anchor == 'topleft':
            rect.topleft = (x, y)
        elif anchor == 'topright':
            rect.topright = (x, y)
        elif anchor == 'center':
            rect.center = (x, y)
        surface.blit(sprite, rect)

    def put_line_of_sprites(self, surface: pg.Surface, name: str, y: int):
        """
        Drawing line of sprites according to the number of minefield's columns
        by name on coordinates (x, y) of the surface.
        """

        for col in range(max(GAME.COLS, 8)):
            self.put_sprite_using_anchor(
                surface, name, 'topleft',
                GUI.BORDER + col * GUI.CELL_SIZE, y
            )

    def build_frame(self):
        """
        Building full frame surface according to the minefield size.
        """

        # frame line #1
        self.put_sprite_using_anchor(
            self.frame, 'frame_panel_top_left_corner', 'topleft',
            0, 0
        )
        self.put_line_of_sprites(
            self.frame, 'frame_panel_top_edge',
            0
        )
        self.put_sprite_using_anchor(
            self.frame, 'frame_panel_top_right_corner', 'topright',
            GUI.SCREEN_WIDTH, 0
        )

        # frame line #2
        self.put_sprite_using_anchor(
            self.frame, 'frame_panel_left_edge', 'topleft',
            0, GUI.BORDER
        )
        self.put_line_of_sprites(
            self.frame, 'frame_panel_interior',
            GUI.BORDER
        )
        self.put_sprite_using_anchor(
            self.frame, 'frame_panel_right_edge', 'topright',
            GUI.SCREEN_WIDTH, GUI.BORDER
        )

        # interior for digits on the panel
        self.put_sprite_using_anchor(
            self.frame, 'digit_panel_interior', 'center',
            GUI.PANEL_X_TOP_LEFT + 2 * GUI.DIGIT_WIDTH,
            GUI.PANEL_Y_CENTER
        )
        self.put_sprite_using_anchor(
            self.frame, 'digit_panel_interior', 'center',
            GUI.PANEL_X_TOP_LEFT + GUI.PANEL_WIDTH
            - 2 * GUI.DIGIT_WIDTH,
            GUI.PANEL_Y_CENTER
        )

        # frame line #3
        self.put_sprite_using_anchor(
            self.frame, 'frame_field_top_left_corner', 'topleft',
            0, GUI.BORDER + GUI.PANEL_HEIGHT
        )
        self.put_line_of_sprites(
            self.frame, 'frame_field_top_edge',
            GUI.BORDER + GUI.PANEL_HEIGHT
        )
        self.put_sprite_using_anchor(
            self.frame, 'frame_field_top_right_corner', 'topright',
            GUI.SCREEN_WIDTH, GUI.BORDER + GUI.PANEL_HEIGHT
        )

        # frame line #4
        for row in range(GAME.ROWS):
            self.put_sprite_using_anchor(
                self.frame, 'frame_field_left_edge', 'topleft',
                0, 2 * GUI.BORDER + GUI.PANEL_HEIGHT + row * GUI.CELL_SIZE
            )
            self.put_line_of_sprites(
                self.frame, 'frame_field_interior',
                2 * GUI.BORDER + GUI.PANEL_HEIGHT + row * GUI.CELL_SIZE
            )
            self.put_sprite_using_anchor(
                self.frame, 'frame_field_right_edge', 'topright',
                GUI.SCREEN_WIDTH,
                2 * GUI.BORDER + GUI.PANEL_HEIGHT + row * GUI.CELL_SIZE
            )

            # separate vertical grid line in case of narrow minefield
            if GAME.COLS < 8:
                self.put_sprite_using_anchor(
                    self.frame, 'cell_grid_line', 'topleft',
                    GUI.FIELD_X_TOP_LEFT + GUI.PADDING
                    + GAME.COLS * GUI.CELL_SIZE,
                    2 * GUI.BORDER + GUI.PANEL_HEIGHT + row * GUI.CELL_SIZE
                )

        # frame line #5
        self.put_sprite_using_anchor(
            self.frame, 'frame_field_bottom_left_corner', 'topleft',
            0, 2 * GUI.BORDER + GUI.PANEL_HEIGHT + GAME.ROWS * GUI.CELL_SIZE
        )
        self.put_line_of_sprites(
            self.frame, 'frame_field_bottom_edge',
            2 * GUI.BORDER + GUI.PANEL_HEIGHT + GAME.ROWS * GUI.CELL_SIZE
        )
        self.put_sprite_using_anchor(
            self.frame, 'frame_field_bottom_right_corner', 'topright',
            GUI.SCREEN_WIDTH,
            2 * GUI.BORDER + GUI.PANEL_HEIGHT + GAME.ROWS * GUI.CELL_SIZE
        )

    # --- Coords / Position methods -------------------------------------------

    @staticmethod
    def convert_coords(mouse_coords: tuple[int, int]) -> tuple[int, int]:
        """
        Converting mouse coords (x, y) - to minefield cell position (row, col).
        Presumably mouse cursor is inside minefield rect.
        """

        x, y = mouse_coords
        col = (x - GUI.FIELD_X_TOP_LEFT - GUI.PADDING) // GUI.CELL_SIZE
        row = (y - GUI.FIELD_Y_TOP_LEFT) // GUI.CELL_SIZE
        return row, col

    @staticmethod
    def convert_position(position: tuple[int, int]) -> tuple[int, int]:
        """
        Converting minefield cell position (row, col) - to pixel coords (x, y).
        """

        row, col = position
        x = GUI.FIELD_X_TOP_LEFT + GUI.PADDING + col * GUI.CELL_SIZE
        y = GUI.FIELD_Y_TOP_LEFT + row * GUI.CELL_SIZE
        return x, y

    def new_mouse_coords(
            self,
            mouse_coords: tuple[int, int],
            direction: str
    ) -> tuple[int, int]:
        """
        Defining new mouse cursor coords according to the direction
        over the center of appropriate minefield cell.
        """

        if direction is not None:
            row, col = self.convert_coords(mouse_coords)

            if direction == 'right':
                col = min(col + 1, GAME.COLS - 1)
            elif direction == 'left':
                col = max(col - 1, 0)
            elif direction == 'up':
                row = max(row - 1, 0)
            elif direction == 'down':
                row = min(row + 1, GAME.ROWS - 1)

            x, y = self.convert_position((row, col))
            x += GUI.CELL_SIZE // 2
            y += GUI.CELL_SIZE // 2
            return x, y
        else:
            return mouse_coords

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
            GUI.FIELD_X_TOP_LEFT + GUI.PADDING,
            GUI.FIELD_Y_TOP_LEFT,
            GAME.COLS * GUI.CELL_SIZE,
            GAME.ROWS * GUI.CELL_SIZE
        )

    # --- Drawing methods -----------------------------------------------------

    def draw_frame(self):
        """
        Reflecting frame on the screen for the indication and minefield.
        """

        self.screen.blit(self.frame, self.frame.get_rect())

    def draw_face_button(self, face_state: FACE_STATE):
        """
        Reflecting current state of the face button.
        """

        self.put_sprite_using_anchor(
            self.screen, 'face_button_' + face_state.name.lower(), 'center',
            GUI.PANEL_X_CENTER, GUI.PANEL_Y_CENTER
        )

    def draw_minefield(self, matrix: ndarray):
        """
        Reflecting current state of the minefield.
        """

        for row in range(GAME.ROWS):
            for col in range(GAME.COLS):
                self.put_sprite_using_anchor(
                    self.screen, 'cell_' + CODE_TO_CELL[matrix[row, col]],
                    'topleft', *self.convert_position((row, col))
                )

    def draw_hovered_cell(
            self,
            code_of_cell: int,
            cell: Optional[tuple[int, int]]
    ):
        """
        Reflecting hovered cell on the minefield.
        """

        hover_sprite_name = 'cell_' + CODE_TO_CELL[code_of_cell] + '_hovered'
        self.put_sprite_using_anchor(
            self.screen, hover_sprite_name, 'topleft',
            *self.convert_position(cell)
        )

    def draw_pressed_cells(
            self,
            cells: Optional[list[tuple[int, int]]],
            action: ACTION
    ):
        """
        Reflecting pressed cell/cells on the minefield.
        """

        if cells is not None:
            if action == ACTION.TO_OPEN_PRESS:
                for cell in cells:
                    self.put_sprite_using_anchor(
                        self.screen, 'cell_pressed', 'topleft',
                        *self.convert_position(cell)
                    )
            elif action == ACTION.TO_LABEL_PRESS:
                for cell in cells:
                    self.put_sprite_using_anchor(
                        self.screen, 'cell_marked_pressed', 'topleft',
                        *self.convert_position(cell)
                    )

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
            self.put_sprite_using_anchor(
                self.screen, 'digit_' + symbol, 'center',
                GUI.PANEL_X_TOP_LEFT + (index + 1) * GUI.DIGIT_WIDTH,
                GUI.PANEL_Y_CENTER
            )

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
        for index, symbol in enumerate(string_score[::-1]):
            self.put_sprite_using_anchor(
                self.screen, 'digit_' + symbol, 'center',
                GUI.PANEL_X_TOP_LEFT + GUI.PANEL_WIDTH
                - (index + 1) * GUI.DIGIT_WIDTH,
                GUI.PANEL_Y_CENTER
            )

    # --- Operational methods -------------------------------------------------

    def clock_tick(self):
        """Ticking clock."""
        self.time_delta = self.clock.tick(GUI.FPS)

    @staticmethod
    def show():
        """Reflecting all the drawings on the display."""
        pg.display.flip()
