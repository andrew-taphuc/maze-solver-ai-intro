from collections import deque

def solve_maze_astar(maze, start, end):
    """
    Giải mê cung sử dụng thuật toán Breadth-First Search (BFS)
    
    Args:
        maze: Ma trận mê cung (0: đường đi, 1: tường)
        start: Vị trí bắt đầu (x, y)
        end: Vị trí kết thúc (x, y)
    
    Returns:
        List các vị trí tạo thành đường đi từ start đến end
    """
    rows, cols = len(maze), len(maze[0])
    queue = deque()
    queue.append((start, [start]))
    visited = set()
    visited.add(start)

    directions = [(-1,0), (1,0), (0,-1), (0,1)]  # lên, xuống, trái, phải

    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == end:
            return path
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (0 <= nx < rows and 0 <= ny < cols and
                maze[nx][ny] == 0 and (nx, ny) not in visited):
                queue.append(((nx, ny), path + [(nx, ny)]))
                visited.add((nx, ny))
    return None  # Không tìm thấy đường đi