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
    heapq.heappush(open_set, (heuristic(start, end), 0, start))
    came_from = {}  # Lưu cha của mỗi ô
    g_score = {start: 0}  # Chi phí ngắn nhất từ start đến ô hiện tại

    directions = [(-1,0), (1,0), (0,-1), (0,1)]  # lên, xuống, trái, phải

    while open_set:
        f, g, current = heapq.heappop(open_set)
        if current == end:
            # Truy vết đường đi từ end về start
            path = []
            cur = end
            while cur != start:
                path.append(cur)
                cur = came_from[cur]
            path.append(start)
            path.reverse()
            return path
        x, y = current
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0:
                tentative_g = g + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score, tentative_g, neighbor))
    return None  # Không tìm thấy đường đi