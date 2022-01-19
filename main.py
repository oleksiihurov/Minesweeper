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
from config import GAME
from logic import Logic


# --- Main Program ------------------------------------------------------------

def main():
    logic = Logic(GAME)
    logic.new_game()
    logic.print_matrix()


if __name__ == '__main__':
    main()
