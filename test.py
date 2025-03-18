import os
import time
import random

def initialize_grid(rows, cols, density=0.3):
    """Initializes the grid with a given density of live cells."""
    return [[random.random() < density for _ in range(cols)] for _ in range(rows)]

def get_neighbors(grid, row, col):
    """Counts the live neighbors of a cell."""
    rows = len(grid)
    cols = len(grid[0])
    neighbors = 0
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col) and grid[i][j]:
                neighbors += 1
    return neighbors

def update_grid(grid):
    """Updates the grid based on the Game of Life rules."""
    rows = len(grid)
    cols = len(grid[0])
    new_grid = [[False for _ in range(cols)] for _ in range(rows)]

    for row in range(rows):
        for col in range(cols):
            neighbors = get_neighbors(grid, row, col)
            if grid[row][col]:  # Cell is alive
                if neighbors < 2 or neighbors > 3:
                    new_grid[row][col] = False  # Dies of under/over-population
                else:
                    new_grid[row][col] = True   # Survives
            else:  # Cell is dead
                if neighbors == 3:
                    new_grid[row][col] = True   # Becomes alive through reproduction
    return new_grid

def print_grid(grid):
    """Prints the grid to the terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
    for row in grid:
        print(''.join(['#' if cell else ' ' for cell in row]))

def game_of_life(rows=20, cols=40, generations=100, delay=0.1):
    """Runs the Game of Life simulation."""
    grid = initialize_grid(rows, cols)
    for _ in range(generations):
        print_grid(grid)
        grid = update_grid(grid)
        time.sleep(delay)

if __name__ == "__main__":
    game_of_life()
