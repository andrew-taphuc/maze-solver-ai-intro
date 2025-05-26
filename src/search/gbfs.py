import heapq
import math
import time

def solve_maze_gbfs(maze, start, end, heuristic_type="manhattan", allow_diagonal=False, show_progress=False):
    """
    Giải mê cung sử dụng thuật toán Greedy Best-First Search với nhiều tính năng nâng cao
    
    Args:
        maze: Ma trận mê cung (0: đường đi, 1: tường)
        start: Vị trí bắt đầu (x, y)
        end: Vị trí kết thúc (x, y)
        heuristic_type: Loại heuristic ("manhattan", "euclidean", "chebyshev", "octile")
        allow_diagonal: Cho phép di chuyển chéo (8 hướng)
        show_progress: Hiển thị quá trình tìm kiếm
    
    Returns:
        Dict chứa: path (đường đi), stats (thống kê), visited_cells (các ô đã thăm)
    """
    start_time = time.time()
    
    if not maze or not maze[0]:
        return {"path": [], "stats": {"nodes_explored": 0, "time_taken": 0}, "visited_cells": set()}
    
    rows, cols = len(maze), len(maze[0])
    nodes_explored = 0
    
    # Kiểm tra vị trí hợp lệ
    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols and maze[x][y] == 0
    
    if not is_valid(start[0], start[1]) or not is_valid(end[0], end[1]):
        return {"path": [], "stats": {"nodes_explored": 0, "time_taken": time.time() - start_time}, "visited_cells": set()}
    
    if start == end:
        return {"path": [start], "stats": {"nodes_explored": 1, "time_taken": time.time() - start_time}, "visited_cells": {start}}
    
    # Các loại hàm heuristic
    def heuristic_manhattan(pos):
        return abs(pos[0] - end[0]) + abs(pos[1] - end[1])
    
    def heuristic_euclidean(pos):
        return math.sqrt((pos[0] - end[0])**2 + (pos[1] - end[1])**2)
    
    def heuristic_chebyshev(pos):
        return max(abs(pos[0] - end[0]), abs(pos[1] - end[1]))
    
    def heuristic_octile(pos):
        dx = abs(pos[0] - end[0])
        dy = abs(pos[1] - end[1])
        return max(dx, dy) + (math.sqrt(2) - 1) * min(dx, dy)
    
    # Chọn hàm heuristic
    heuristic_functions = {
        "manhattan": heuristic_manhattan,
        "euclidean": heuristic_euclidean,
        "chebyshev": heuristic_chebyshev,
        "octile": heuristic_octile
    }
    
    heuristic = heuristic_functions.get(heuristic_type, heuristic_manhattan)
    
    # Các hướng di chuyển
    if allow_diagonal:
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    else:
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Priority queue: (heuristic_value, position)
    pq = [(heuristic(start), start)]
    
    # Dict lưu trữ parent để trace lại đường đi
    parent = {start: None}
    
    # Set các điểm đã thăm (để trả về thống kê)
    visited = set()
    all_visited = set()
    
    def reconstruct_path():
        """Tái tạo đường đi từ end về start"""
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = parent.get(current)
        path.reverse()
        return path
    
    iteration = 0
    while pq:
        iteration += 1
        if show_progress and iteration % 50 == 0:
            print(f"Iteration {iteration}: Queue size: {len(pq)}, Nodes explored: {nodes_explored}")
        
        # Lấy node có heuristic value nhỏ nhất
        current_h, current_pos = heapq.heappop(pq)
        
        # Bỏ qua nếu đã thăm
        if current_pos in visited:
            continue
        
        # Đánh dấu đã thăm
        visited.add(current_pos)
        all_visited.add(current_pos)
        nodes_explored += 1
        
        # Kiểm tra đã đến đích
        if current_pos == end:
            end_time = time.time()
            path = reconstruct_path()
            return {
                "path": path,
                "stats": {
                    "nodes_explored": nodes_explored,
                    "time_taken": end_time - start_time,
                    "path_length": len(path),
                    "iterations": iteration,
                    "heuristic_used": heuristic_type
                },
                "visited_cells": all_visited
            }
        
        # Mở rộng các node lân cận
        for dx, dy in directions:
            new_x, new_y = current_pos[0] + dx, current_pos[1] + dy
            new_pos = (new_x, new_y)
            
            # Kiểm tra vị trí hợp lệ và chưa thăm
            if is_valid(new_x, new_y) and new_pos not in visited:
                if new_pos not in parent:  # Chưa được khám phá
                    parent[new_pos] = current_pos
                    h_value = heuristic(new_pos)
                    heapq.heappush(pq, (h_value, new_pos))
    
    # Không tìm thấy đường đi
    end_time = time.time()
    return {
        "path": [],
        "stats": {
            "nodes_explored": nodes_explored,
            "time_taken": end_time - start_time,
            "path_length": 0,
            "iterations": iteration,
            "heuristic_used": heuristic_type
        },
        "visited_cells": all_visited
    }

def compare_heuristics(maze, start, end):
    """So sánh các loại heuristic khác nhau"""
    print("\n=== SO SÁNH CÁC HEURISTIC ===")
    heuristics = ["manhattan", "euclidean", "chebyshev", "octile"]
    
    results = {}
    for h_type in heuristics:
        result = solve_maze_gbfs(maze, start, end, heuristic_type=h_type)
        results[h_type] = result
        print(f"Heuristic {h_type}: {result['stats']}")
    
    return results

def visualize_comparison(maze, start, end):
    """Hiển thị so sánh trực quan giữa các thuật toán"""
    print("\n=== SO SÁNH TRỰC QUAN ===")
    
    # GBFS với Manhattan
    gbfs_result = solve_maze_gbfs(maze, start, end, heuristic_type="manhattan")
    print(f"GBFS (Manhattan): Đường đi {len(gbfs_result['path'])} bước, thăm {len(gbfs_result['visited_cells'])} ô")
    
    # GBFS với Euclidean + diagonal
    gbfs_diag_result = solve_maze_gbfs(maze, start, end, heuristic_type="euclidean", allow_diagonal=True)
    print(f"GBFS (Euclidean + Diagonal): Đường đi {len(gbfs_diag_result['path'])} bước, thăm {len(gbfs_diag_result['visited_cells'])} ô")
    
    return gbfs_result, gbfs_diag_result
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

# Ví dụ sử dụng
if __name__ == "__main__":
    # Mê cung mẫu (0: đường đi, 1: tường)
    maze = [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 0, 1, 0]
    ]
    
    start = (0, 0)
    end = (4, 4)
    
    print("=== GREEDY BEST-FIRST SEARCH CẢI TIẾN ===")
    
    # Test với các heuristic khác nhau
    result_manhattan = solve_maze_gbfs(maze, start, end, heuristic_type="manhattan", show_progress=True)
    print(f"\nKết quả Manhattan:")
    print(f"Đường đi: {result_manhattan['path']}")
    print(f"Thống kê: {result_manhattan['stats']}")
    
    # Test với diagonal movement
    result_diagonal = solve_maze_gbfs(maze, start, end, heuristic_type="octile", allow_diagonal=True)
    print(f"\nKết quả với di chuyển chéo:")
    print(f"Đường đi: {result_diagonal['path']}")
    print(f"Thống kê: {result_diagonal['stats']}")
    
    # So sánh các heuristic
    compare_heuristics(maze, start, end)
    
    # So sánh trực quan
    visualize_comparison(maze, start, end)
    end = (4, 4)
    
    # Sử dụng GBFS thường
    path = solve_maze_gbfs(maze, start, end)
    print("Đường đi tìm được:", path)
    print("Độ dài đường đi:", len(path) if path else 0)
    
    # Sử dụng GBFS với thống kê
    path_stats, nodes_explored = solve_maze_gbfs_with_stats(maze, start, end)
    print("Số node đã khám phá:", nodes_explored)
    
    # In mê cung với đường đi
    if path:
        maze_copy = [row[:] for row in maze]
        for x, y in path:
            if (x, y) != start and (x, y) != end:
                maze_copy[x][y] = 2  # Đánh dấu đường đi
        
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