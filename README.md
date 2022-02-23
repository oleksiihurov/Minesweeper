# Minesweeper

Tribute to original online variations of the game:

https://minesweeperonline.com

https://minesweeper.online

Project is created by Oleksii Hurov in Feb 2022
for educational purpose as well as part of portfolio.


## Technologies and programming methods learned during development

### Methods:
- Correct separating project's codebase into distinct modules.
- Using external source of initial information from configs.
- Parsing various format config-files (json, ini) and image sprites (png).
- Distinct engine logic, which could be used separately.
- Division of project's modules to levels of abstraction:
    - (I) Data level abstraction - Data structures, types and interfaces;
    - (II) Input level abstraction - Predefined parameters and constants;
    - (III) Logic level abstraction - Logic, primary purpose and calculations;
    - (IV) Output level abstraction - Presentation, graphics & UI;
    - (V) Control level abstraction - Main program. Entry point.

### Technologies:
- Using scientific computing package "Numpy" for internal data storing.
- Applying external graphics module "Pygame" as an engine for output.
- Dealing with events stack from keyboard and mouse as a source input.
- Own custom GUI processing.

### Coding:
- Widely using of docstrings and comments for better readability of code.
- Using type hinting generics for better readability of code.
- Composing Python classes as dataclasses, enums, type definitions, etc.
- No hard-coding. All the constants defined in external configs.
- Mnemonic variables and functions names.
- Complete PEP 8 style compatibility.
- Main program entry point is not flooded with unnecessary code.


## Dependency on external modules and versions

* Python 3.9.5+
* numpy 1.21.4 (https://numpy.org)
* pygame 2.1.0 (https://www.pygame.org)


## How to Use the Program

1. Open the project in any convenient Python IDE.
2. Install the following packages using pip: "numpy" and "pygame"
3. To adjust configuration for the game - edit the file: "assets\config.ini"
4. Run the project's main.py


## How to Play

Minesweeper is a single-player puzzle video game.
The objective of the game is to clear a rectangular board
containing hidden "mines" or bombs without detonating any of them,
with help from clues about the number of neighbouring mines in each field.


## Controls to Play

- Left mouse button click (or '1' key) on the minefield:
    opens corresponding cell.
- Right mouse button click (or '3' key) on the minefield:
    labels corresponding cell.
- Middle mouse button click (or '2' key, or space bar key) on the minefield:
    reveals cells around.
- Arrow keys (up, down, left, right) move current cursor over the cells.
- Esc key closes the program.


## Several screenshots from the project

![screenshot1.png](/screenshots/screenshot1.png)

![screenshot2.png](/screenshots/screenshot2.png)

![screenshot3.png](/screenshots/screenshot3.png)