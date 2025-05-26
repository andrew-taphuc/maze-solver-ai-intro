import random

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