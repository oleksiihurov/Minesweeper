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


# Project imports
from demo import Demo


# --- Main Program ------------------------------------------------------------

def main():
    demo = Demo()
    while demo.loop_handler():
        demo.events_handler()
        demo.actions_handler()
        demo.reactions_handler()
        demo.graphics_handler()


if __name__ == '__main__':
    main()
