import heapq
import math

def solve_maze_gbfs(maze, start, end):
    """
    Giải mê cung sử dụng thuật toán Greedy Best-First Search
    
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
    
    #Check vị trí hợp lệ
    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols and maze[x][y] == 0
    
    if not is_valid(start[0], start[1]) or not is_valid(end[0], end[1]):
        return []
    
    if start == end:
        return [start]
    
    #khoảng cách Manhattan
    def heuristic(pos):
        return abs(pos[0] - end[0]) + abs(pos[1] - end[1])
    
    #khoảng cách Euclidean 
    def heuristic_euclidean(pos):
        return math.sqrt((pos[0] - end[0])**2 + (pos[1] - end[1])**2)
    
    #hướng di chuyển
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    #Priority queue: (heuristic_value, position)
    pq = [(heuristic(start), start)]
    
    #Dict lưu trữ parent để trace lại đường đi
    parent = {start: None}
    
    #Set các điểm đã thăm
    visited = set()
    
    def reconstruct_path():
        """Tái tạo đường đi từ end về start"""
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = parent.get(current)
        path.reverse()
        return path
    
    while pq:
        #Lấy node có heuristic value nhỏ nhất
        current_h, current_pos = heapq.heappop(pq)
        
        #Bỏ qua nếu đã thăm
        if current_pos in visited:
            continue
        
        #Đánh dấu đã thăm
        visited.add(current_pos)
        
        #Kiểm tra đã đến đích
        if current_pos == end:
            return reconstruct_path()
        
        #Mở rộng các node lân cận
        for dx, dy in directions:
            new_x, new_y = current_pos[0] + dx, current_pos[1] + dy
            new_pos = (new_x, new_y)
            
            #Kiểm tra vị trí hợp lệ và chưa thăm
            if is_valid(new_x, new_y) and new_pos not in visited:
                if new_pos not in parent:  
                    parent[new_pos] = current_pos
                    h_value = heuristic(new_pos)
                    heapq.heappush(pq, (h_value, new_pos))
    
    #Không tìm thấy đường đi
    return []

def solve_maze_gbfs_with_stats(maze, start, end):
    """
    Phiên bản GBFS có thống kê số node đã thăm
    """
    if not maze or not maze[0]:
        return [], 0
    
    rows, cols = len(maze), len(maze[0])
    nodes_explored = 0
    
    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols and maze[x][y] == 0
    
    if not is_valid(start[0], start[1]) or not is_valid(end[0], end[1]):
        return [], nodes_explored
    
    if start == end:
        return [start], 1
    
    def heuristic(pos):
        return abs(pos[0] - end[0]) + abs(pos[1] - end[1])
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    pq = [(heuristic(start), start)]
    parent = {start: None}
    visited = set()
    
    def reconstruct_path():
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = parent.get(current)
        path.reverse()
        return path
    
    while pq:
        current_h, current_pos = heapq.heappop(pq)
        
        if current_pos in visited:
            continue
        
        visited.add(current_pos)
        nodes_explored += 1
        
        if current_pos == end:
            return reconstruct_path(), nodes_explored
        
        for dx, dy in directions:
            new_x, new_y = current_pos[0] + dx, current_pos[1] + dy
            new_pos = (new_x, new_y)
            
            if is_valid(new_x, new_y) and new_pos not in visited:
                if new_pos not in parent:
                    parent[new_pos] = current_pos
                    h_value = heuristic(new_pos)
                    heapq.heappush(pq, (h_value, new_pos))
    
    return [], nodes_explored


if __name__ == "__main__":
    #Mê cung mẫu
    maze = [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 0, 1, 0]
    ]
    
    start = (0, 0)
    end = (4, 4)
    
    #Sử dụng GBFS thường
    path = solve_maze_gbfs(maze, start, end)
    print("Đường đi tìm được:", path)
    print("Độ dài đường đi:", len(path) if path else 0)
    
    #Sử dụng GBFS với thống kê
    path_stats, nodes_explored = solve_maze_gbfs_with_stats(maze, start, end)
    print("Số node đã khám phá:", nodes_explored)
    
    #In mê cung với đường đi
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
    else:
        print("\nKhông tìm thấy đường đi!")