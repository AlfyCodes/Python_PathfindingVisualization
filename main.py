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
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# Keeping track of the nodes in the grid (The spots on the grid)


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        # All cubes will be white at start / Also indicates areas not yet looked at
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

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

    def make_start(self):
        self.color = GREEN

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
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        pass

    # Less than that handles Spot comparisons
    def __lt__(self, other):
        return False

# Heuristic Function / Figure the distance between point 1 and point 2 using Manhattan Distance
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    # Use distance formula
    return abs(x1 - x2) + abs(y1 - y2)

# Makes the grid
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid

# Draw Lines
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))  # Horiztanl
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))  # Vertical

    # Draws the linens


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()

    # Handles mouse clicks - drawing cubes


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos  # take the position and divide by the width of the cubes

    row = y // gap
    col = x // gap

    return row, col

# The Main Loop


def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:  # Left Mouse Click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:  # If start is not on the grid - make it on next click
                    start = spot
                    start.make_start()
                elif not end and spot != start:  # Else if end is not on grid - make it on next click
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:  # Else if make a barrier
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # Right Mouse Click
                pass

    pygame.quit()

main(WIN, WIDTH)