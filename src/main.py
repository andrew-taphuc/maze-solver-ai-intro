import pygame
import sys
import time
from config import *
from utils import generate_maze
from search.bfs import solve_maze_bfs
from search.dfs import solve_maze_dfs
from search.astar import solve_maze_astar
from search.gbfs import solve_maze_gbfs
from search.bidirectionalbfs import solve_maze_bidirectional_bfs

# Initialize Pygame
pygame.init()

# Constants
TILE_SIZE = 40
ROWS = 15
COLS = 15
WIDTH = COLS * TILE_SIZE
HEIGHT = ROWS * TILE_SIZE + 100  # Thêm không gian cho hướng dẫn

# Generate initial maze
MAZE = generate_maze(ROWS, COLS)

# Colors
WHITE = BACKGROUND_COLOR
BLACK = WALL_COLOR
BLUE = CELL_VISITED_COLOR
GREEN = START_END_CELL_COLOR
YELLOW = CELL_SOLUTION_COLOR

# Set up screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

# Font setup
pygame.font.init()
font = pygame.font.SysFont(FONT, 20)
small_font = pygame.font.SysFont(FONT, 16)

# Game stats
class GameStats:
    def __init__(self):
        self.steps = 0
        self.start_time = time.time()
        self.best_time = float('inf')
        self.mazes_solved = 0
        self.total_steps = 0
        self.reset()

    def reset(self):
        self.steps = 0
        self.start_time = time.time()
        self.current_path = set()

    def add_step(self, pos):
        if pos not in self.current_path:
            self.steps += 1
            self.current_path.add(pos)

    def get_time(self):
        return round(time.time() - self.start_time, 1)

    def update_best_time(self):
        current_time = self.get_time()
        if current_time < self.best_time:
            self.best_time = current_time

    def maze_solved(self):
        self.mazes_solved += 1
        self.total_steps += self.steps
        self.update_best_time()

stats = GameStats()

# Player position
player_pos = [0, 0]
goal_pos = [ROWS - 1, COLS - 1]

# Solution path
solution_path = None
current_solution_index = 0

clock = pygame.time.Clock()

def draw_instructions():
    # Vẽ nền cho phần hướng dẫn
    pygame.draw.rect(screen, WHITE, (0, HEIGHT - 100, WIDTH, 100))
    
    # Danh sách các hướng dẫn
    instructions = [
        "Hướng dẫn:",
        "↑↓←→: Di chuyển",
        "S: Hiển thị đường đi",
        "A: Tự động giải",
        "R: Tạo mê cung mới"
    ]
    
    # Vẽ từng dòng hướng dẫn
    for i, text in enumerate(instructions):
        text_surface = font.render(text, True, BLACK)
        screen.blit(text_surface, (10, HEIGHT - 90 + i * 20))

def draw_stats():
    # Thông tin thống kê
    stats_texts = [
        f"Thời gian: {stats.get_time()}s",
        f"Bước đi: {stats.steps}",
        f"Mê cung đã giải: {stats.mazes_solved}",
        f"Thời gian tốt nhất: {stats.best_time if stats.best_time != float('inf') else 'N/A'}s",
        f"Trung bình bước đi: {round(stats.total_steps/stats.mazes_solved, 1) if stats.mazes_solved > 0 else 0}"
    ]
    
    # Vẽ thống kê ở góc phải
    for i, text in enumerate(stats_texts):
        text_surface = small_font.render(text, True, BLACK)
        screen.blit(text_surface, (WIDTH - 250, HEIGHT - 90 + i * 20))

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

def draw_player():
    x = player_pos[1] * TILE_SIZE
    y = player_pos[0] * TILE_SIZE
    pygame.draw.rect(screen, BLUE, (x, y, TILE_SIZE, TILE_SIZE))

def draw_solution():
    if solution_path:
        for x, y in solution_path:
            pygame.draw.rect(screen, YELLOW, 
                           (y * TILE_SIZE, x * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def draw_status():
    status_text = "Chế độ: " + ("Tự động giải" if auto_solve else "Điều khiển thủ công")
    text_surface = font.render(status_text, True, BLACK)
    screen.blit(text_surface, (WIDTH - 200, HEIGHT - 90))

# Main game loop
running = True
auto_solve = False
while running:
    screen.fill(WHITE)
    draw_maze()
    draw_solution()
    draw_player()
    draw_instructions()
    draw_status()
    draw_stats()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Press R to regenerate maze
                MAZE = generate_maze(ROWS, COLS)
                player_pos = [0, 0]
                solution_path = None
                auto_solve = False
                stats.reset()
            elif event.key == pygame.K_s:  # Press S to show solution
                solution_path = solve_maze_bfs(MAZE, (0, 0), (ROWS-1, COLS-1))
            elif event.key == pygame.K_a:  # Press A to toggle auto solve
                auto_solve = not auto_solve
                if auto_solve:
                    solution_path = solve_maze_bfs(MAZE, (0, 0), (ROWS-1, COLS-1))
                    current_solution_index = 0

    if auto_solve and solution_path:
        if current_solution_index < len(solution_path):
            next_pos = solution_path[current_solution_index]
            player_pos = [next_pos[0], next_pos[1]]
            stats.add_step(tuple(player_pos))
            current_solution_index += 1
            pygame.time.wait(100)
    else:
        # Manual movement
        keys = pygame.key.get_pressed()
        row, col = player_pos
        old_pos = player_pos.copy()
        if keys[pygame.K_UP] and row > 0 and MAZE[row - 1][col] == 0:
            player_pos[0] -= 1
        if keys[pygame.K_DOWN] and row < ROWS - 1 and MAZE[row + 1][col] == 0:
            player_pos[0] += 1
        if keys[pygame.K_LEFT] and col > 0 and MAZE[row][col - 1] == 0:
            player_pos[1] -= 1
        if keys[pygame.K_RIGHT] and col < COLS - 1 and MAZE[row][col + 1] == 0:
            player_pos[1] += 1
        
        if player_pos != old_pos:
            stats.add_step(tuple(player_pos))

    # Check win
    if player_pos == goal_pos:
        stats.maze_solved()
        win_text = f"🎉 Chúc mừng! Bạn đã đến đích!\nThời gian: {stats.get_time()}s\nBước đi: {stats.steps}"
        lines = win_text.split('\n')
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, BLACK)
            screen.blit(text_surface, (WIDTH//2 - 150, HEIGHT - 60 + i * 25))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    clock.tick(10)

pygame.quit()
sys.exit()
