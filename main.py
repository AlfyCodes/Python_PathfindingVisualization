import pygame
import math
from queue import PriorityQueue

# Create a screen
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Finding Algorithm")

# Give color to the scrren
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0 , 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# Keeping track of the nodes in the grid (The spots on the grid)
class Spot: 
    def __init__(self, row, col, width, total_rows) # 
    self.row = row 
    self.col = col
    self.x = row * width 
    self.y = col * width 
    self.color = WHITE # All cubes will be white at start / Also indicates areas not yet looked at
    self.neighbors = [] 
    self.width = width 
    self.total_rows 

# Gets the position
def get_pos(self):
    return self.row, self.col 

# The red squares will indicate that we already looked at this position 
def is_closed(self):
    return self.color == RED

# Open Set
 def is_open(self):
    return self.colo == ORANGE

# Barrier
def is_barrier(self):
    return self.color == BLACK

# Starting Location
def is_start(self):
    return self.color == GREEN

# Ending Location
def is_end(self):
    return self.color == PURPLE

# Resets the Grid
def reset(self):
    self.color == WHITE

# Change the colors
def make_closed(self):
    self.color = RED

def make_open(self):
    self.color = GREEN

def make_barrier(self):
    self.color = BLACK

def make_end(self):
    self.color = PURPLE

def make_path(self):
    self.color = TURQUOISE

def draw(self, win):
    pygame.draw.rect(win, self.color, ())

def update_neighbors(self, grid):
    pass

# Less than that handles Spot comparisons 
def __lt__(self, other):
    return False
