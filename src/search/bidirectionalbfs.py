from collections import deque

def solve_maze_bidirectional_bfs(maze, start, end):
    """
    Giải mê cung sử dụng thuật toán Bidirectional BFS
    
    Args:
        maze: Ma trận mê cung (0: đường đi, 1: tường)
        start: Vị trí bắt đầu (x, y)
        end: Vị trí kết thúc (x, y)
    
    Returns:
        List các vị trí tạo thành đường đi từ start đến end
    """
    if not maze or not maze[0]:
        return []
    
    rows, cols = len(maze), len(maze[0])
    
    #Kiểm tra vị trí hợp lệ
    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols and maze[x][y] == 0
    
    if not is_valid(start[0], start[1]) or not is_valid(end[0], end[1]):
        return []
    
    if start == end:
        return [start]
    
    #Các hướng di chuyển
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Queue cho tìm kiếm từ điểm bắt đầu và điểm kết thúc
    queue_start = deque([start])
    queue_end = deque([end])
    
    # Dict lưu trữ parent để trace lại đường đi
    parent_start = {start: None}
    parent_end = {end: None}
    
    # Set các điểm đã thăm
    visited_start = {start}
    visited_end = {end}
    
    def reconstruct_path(meeting_point):
        """Tái tạo đường đi từ điểm gặp nhau"""
        path = []
        
        # Trace từ meeting_point về start
        current = meeting_point
        while current is not None:
            path.append(current)
            current = parent_start.get(current)
        path.reverse()
        
        # Trace từ meeting_point về end 
        current = parent_end.get(meeting_point)
        while current is not None:
            path.append(current)
            current = parent_end.get(current)
        
        return path
    
    # Tìm kiếm bidirectional
    while queue_start and queue_end:
        # Mở rộng từ điểm bắt đầu
        if queue_start:
            current_start = queue_start.popleft()
            
            for dx, dy in directions:
                new_x, new_y = current_start[0] + dx, current_start[1] + dy
                new_pos = (new_x, new_y)
                
                if is_valid(new_x, new_y) and new_pos not in visited_start:
                    parent_start[new_pos] = current_start
                    visited_start.add(new_pos)
                    queue_start.append(new_pos)
                    
                    # Kiểm tra gặp nhau
                    if new_pos in visited_end:
                        return reconstruct_path(new_pos)
        
        # Mở rộng từ điểm kết thúc
        if queue_end:
            current_end = queue_end.popleft()
            
            for dx, dy in directions:
                new_x, new_y = current_end[0] + dx, current_end[1] + dy
                new_pos = (new_x, new_y)
                
                if is_valid(new_x, new_y) and new_pos not in visited_end:
                    parent_end[new_pos] = current_end
                    visited_end.add(new_pos)
                    queue_end.append(new_pos)
                    
                    # Kiểm tra gặp nhau
                    if new_pos in visited_start:
                        return reconstruct_path(new_pos)
    
    # Không tìm thấy đường đi
    return []


if __name__ == "__main__":
    maze = [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 0, 1, 0]
    ]
    start = (0, 0)
    end = (4, 4)
    
    path = solve_maze_bidirectional_bfs(maze, start, end)
    print("Đường đi tìm được:", path)
    
    # In mê cung với đường đi
    if path:
        maze_copy = [row[:] for row in maze]
        for x, y in path:
            if (x, y) != start and (x, y) != end:
                maze_copy[x][y] = 2  
        
        print("\nMê cung với đường đi (2: đường đi, S: start, E: end):")
        for i, row in enumerate(maze_copy):
            for j, cell in enumerate(row):
                if (i, j) == start:
                    print('S', end=' ')
                elif (i, j) == end:
                    print('E', end=' ')
                elif cell == 0:
                    print('.', end=' ')
                elif cell == 1:
                    print('#', end=' ')
                elif cell == 2:
                    print('*', end=' ')
            print()