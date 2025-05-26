import pygame
import sys
from config import *
import random

# Initialize Pygame
pygame.init()

# Constants
TILE_SIZE = 40
ROWS = 15
COLS = 15
WIDTH = COLS * TILE_SIZE
HEIGHT = ROWS * TILE_SIZE

def generate_maze(rows, cols):
    # Initialize maze with walls
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    
    def carve_path(x, y):
        maze[y][x] = 0
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < cols and 0 <= new_y < rows and 
                maze[new_y][new_x] == 1):
                # Carve path between current cell and new cell
                maze[y + dy//2][x + dx//2] = 0
                carve_path(new_x, new_y)
    
    # Start from a random even position
    start_x = random.randrange(0, cols, 2)
    start_y = random.randrange(0, rows, 2)
    carve_path(start_x, start_y)
    
    # Ensure start and end are accessible
    maze[0][0] = 0
    maze[rows-1][cols-1] = 0
    
    return maze

# Generate initial maze
MAZE = generate_maze(ROWS, COLS)

# Colors
WHITE = BACKGROUND_COLOR
BLACK = WALL_COLOR
BLUE = CELL_VISITED_COLOR
GREEN = START_END_CELL_COLOR

# Set up screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

# Player position
player_pos = [0, 0]
goal_pos = [ROWS - 1, COLS - 1]

clock = pygame.time.Clock()

# Draw the maze
def draw_maze():
    for row in range(ROWS):
        for col in range(COLS):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            if MAZE[row][col] == 1:
                pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE))
            else:
                pygame.draw.rect(screen, WHITE, (x, y, TILE_SIZE, TILE_SIZE))
    # Draw goal
    gx, gy = goal_pos[1] * TILE_SIZE, goal_pos[0] * TILE_SIZE
    pygame.draw.rect(screen, GREEN, (gx, gy, TILE_SIZE, TILE_SIZE))

# Draw the player
def draw_player():
    x = player_pos[1] * TILE_SIZE
    y = player_pos[0] * TILE_SIZE
    pygame.draw.rect(screen, BLUE, (x, y, TILE_SIZE, TILE_SIZE))

# Main game loop
running = True
while running:
    screen.fill(WHITE)
    draw_maze()
    draw_player()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Press R to regenerate maze
                MAZE = generate_maze(ROWS, COLS)
                player_pos = [0, 0]

    # Movement
    keys = pygame.key.get_pressed()
    row, col = player_pos
    if keys[pygame.K_UP] and row > 0 and MAZE[row - 1][col] == 0:
        player_pos[0] -= 1
    if keys[pygame.K_DOWN] and row < ROWS - 1 and MAZE[row + 1][col] == 0:
        player_pos[0] += 1
    if keys[pygame.K_LEFT] and col > 0 and MAZE[row][col - 1] == 0:
        player_pos[1] -= 1
    if keys[pygame.K_RIGHT] and col < COLS - 1 and MAZE[row][col + 1] == 0:
        player_pos[1] += 1

    # Check win
    if player_pos == goal_pos:
        print("🎉 You reached the goal!")
        pygame.time.wait(2000)
        running = False

    clock.tick(10)

pygame.quit()
sys.exit()
