import heapq

def heuristic(a, b):
    # Hàm heuristic: khoảng cách Manhattan
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def solve_maze_astar(maze, start, end):
    """
    Giải mê cung sử dụng thuật toán A* (A-star)
    
    Args:
        maze: Ma trận mê cung (0: đường đi, 1: tường)
        start: Vị trí bắt đầu (x, y)
        end: Vị trí kết thúc (x, y)
    
    Returns:
        List các vị trí tạo thành đường đi từ start đến end
    """
    rows, cols = len(maze), len(maze[0])
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, end), 0, start, [start]))
    visited = set()

    directions = [(-1,0), (1,0), (0,-1), (0,1)]  # lên, xuống, trái, phải

    while open_set:
        f, g, current, path = heapq.heappop(open_set)
        if current == end:
            return path
        if current in visited:
            continue
        visited.add(current)
        x, y = current
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)
            if (0 <= nx < rows and 0 <= ny < cols and
                maze[nx][ny] == 0 and neighbor not in visited):
                heapq.heappush(open_set, (
                    g + 1 + heuristic(neighbor, end),  # f = g + h
                    g + 1,
                    neighbor,
                    path + [neighbor]
                ))
    return None  # Không tìm thấy đường đi