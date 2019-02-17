import pygame as pg
from os import path
# Settings for the game

# Window settings
TITLE = "Computing Project Platformer"
FONT = pg.font.match_font('arial')
WIDTH = 960
HEIGHT = 640
FPS = 60
GRID_SIZE = 32

DIR = path.dirname(__file__)  # Get file directory
IMAGES_DIR = path.join(DIR, 'images')  # Path to img file

# Player settings
MAX_HEARTS = 3

# Levels
MAX_LEVELS = 2

# Controls
LEFT = pg.K_LEFT
RIGHT = pg.K_RIGHT
JUMP = pg.K_UP

# Colour constants
TRANSPARENT = (0, 0, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (66, 212, 244)
