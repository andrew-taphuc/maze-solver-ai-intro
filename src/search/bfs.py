from collections import deque

def solve_maze_bfs(maze, start, end):
    """
    Giải mê cung sử dụng thuật toán bfs
    
    Args:
        maze: Ma trận mê cung (0: đường đi, 1: tường)
        start: Vị trí bắt đầu (x, y)
        end: Vị trí kết thúc (x, y)
    
    Returns:
        List các vị trí tạo thành đường đi từ start đến end
    """
    rows, cols = len(maze), len(maze[0])
    queue = deque()
    queue.append(start)
    visited = set()
    visited.add(start)
    parent = {}  # Lưu cha của mỗi ô

    directions = [(-1,0), (1,0), (0,-1), (0,1)]  # lên, xuống, trái, phải

    while queue:
        x, y = queue.popleft()
        if (x, y) == end:
            # Truy vết đường đi từ end về start
            path = []
            cur = end
            while cur != start:
                path.append(cur)
                cur = parent[cur]
            path.append(start)
            path.reverse()
            return path
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)
            if (0 <= nx < rows and 0 <= ny < cols and
                maze[nx][ny] == 0 and neighbor not in visited):
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = (x, y)
    return None  # Không tìm thấy đường đi