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


# Project imports
from config import CLICK, GAME
from logic import Logic


# --- Main Program ------------------------------------------------------------

def main():
    logic = Logic(GAME)
    logic.new_game()

    logic.click(CLICK.RIGHT, (1, 1))
    logic.click(CLICK.LEFT, (1, 2))

    logic.click(CLICK.LEFT, (6, 8))

    logic.click(CLICK.RIGHT, (6, 26))
    logic.click(CLICK.RIGHT, (8, 23))
    logic.click(CLICK.LEFT, (9, 24))

    logic.print_revealed_minefield()
    logic.print_covered_minefield()


if __name__ == '__main__':
    main()
