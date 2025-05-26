from collections import deque

def solve_maze_bfs(maze, start, end):
    rows = len(maze)
    cols = len(maze[0])
    
    # Các hướng di chuyển: lên, phải, xuống, trái
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    # Khởi tạo queue và visited
    queue = deque([(start, [start])])
    visited = set([start])
    
    while queue:
        (x, y), path = queue.popleft()
        
        # Kiểm tra đã đến đích chưa
        if (x, y) == end:
            return path
            
        # Thử các hướng di chuyển
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            
            # Kiểm tra vị trí mới có hợp lệ không
            if (0 <= new_x < rows and 0 <= new_y < cols and 
                maze[new_x][new_y] == 0 and 
                (new_x, new_y) not in visited):
                
                # Thêm vào queue và đánh dấu đã thăm
                queue.append(((new_x, new_y), path + [(new_x, new_y)]))
                visited.add((new_x, new_y))
    
    return None  # Không tìm thấy đường đi
