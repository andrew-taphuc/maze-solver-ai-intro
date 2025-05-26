import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
TILE_SIZE = 40
MAZE = [
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 1, 0],
    [1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0]
]

ROWS = len(MAZE)
COLS = len(MAZE[0])
WIDTH = COLS * TILE_SIZE
HEIGHT = ROWS * TILE_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)

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
