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
        self.color = WHITE

    def make_start(self):
        self.color = GREEN

    # Change the colors
    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = ORANGE

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = PURPLE

    def make_path(self):
        self.color = TURQUOISE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # Moving Down a row
            self.neighbors.append(grid[self.row + 1][self.col])
        
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # Moving Up a row
            self.neighbors.append(grid[self.row - 1][self.col])
        
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # Moving Right a row
            self.neighbors.append(grid[self.row][self.col + 1])
        
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # Moving Left a row
            self.neighbors.append(grid[self.row][self.col - 1])
    # Less than that handles Spot comparisons
    def __lt__(self, other):
        return False

# Heuristic Function / Figure the distance between point 1 and point 2 using Manhattan Distance
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    # Use distance formula
    return abs(x1 - x2) + abs(y1 - y2)

# Traverse from the current node all the way back to the start Node.
def construct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start)) # Adds to Priority Queue / Keeps track [takes two nodes that have the same fValue and takes the first that was inserted]
    came_from = {} # Where did this Node come from - Keeps track
    g_score = {spot: float("inf") for row in grid for spot in row} # List comprehension - Keeps track of the current shortest distance from start to this node
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row} # List comprehension - Keeps track of our predicted distance to the end
    f_score[start] = h(start.get_pos(), end.get_pos()) # Estimate the distance from start to end 

    open_set_hash = {start} # PriorityQueue can't tell us what's in the queue, so we have a hash to do that. 

    while not open_set.empty(): # Run until empty - Considers all nodes for possible path
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Exit while loop case
                pygame.quit()
        
        current = open_set.get()[2] # start 2 because we want the node[start] not the fscore or the count thats stored
        open_set_hash.remove(current) # Remove start from the hash. 

        if current == end: # We finished
            construct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1 # Take the distance of the current node and add 1

            if temp_g_score < g_score[neighbor]: # If we find a better path - Update
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor)) # Add
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()

        if current != start: # Make it closed(RED) if the node we got is not start
            current.make_closed()

    return False


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

# Draws the lines
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
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset() # Delete spot
                if spot == start:
                    start = None
                elif spot == end:
                    end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end: # Upadating the neighbors
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid) 
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end) # Creates anonymous function
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)        
                
    pygame.quit()

main(WIN, WIDTH)