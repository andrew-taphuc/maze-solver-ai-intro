from collections import deque
import time

def solve_maze_bidirectional_bfs(maze, start, end, allow_diagonal=False, show_progress=False):
    """
    Giải mê cung sử dụng thuật toán Bidirectional BFS với nhiều tính năng nâng cao
    
    Args:
        maze: Ma trận mê cung (0: đường đi, 1: tường)
        start: Vị trí bắt đầu (x, y)
        end: Vị trí kết thúc (x, y)
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
    
    # Các hướng di chuyển
    if allow_diagonal:
        # 8 hướng: lên, xuống, trái, phải, và 4 hướng chéo
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    else:
        # 4 hướng: lên, xuống, trái, phải
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Queue cho tìm kiếm từ điểm bắt đầu và điểm kết thúc
    queue_start = deque([start])
    queue_end = deque([end])
    
    # Dict lưu trữ parent để trace lại đường đi
    parent_start = {start: None}
    parent_end = {end: None}
    
    # Set các điểm đã thăm (để trả về thống kê)
    all_visited = set()
    visited_start = {start}
    visited_end = {end}
    all_visited.update([start, end])
    
    def reconstruct_path(meeting_point):
        """Tái tạo đường đi từ điểm gặp nhau"""
        path = []
        
        # Trace từ meeting_point về start
        current = meeting_point
        while current is not None:
            path.append(current)
            current = parent_start.get(current)
        path.reverse()
        
        # Trace từ meeting_point về end (bỏ qua meeting_point để tránh trùng)
        current = parent_end.get(meeting_point)
        while current is not None:
            path.append(current)
            current = parent_end.get(current)
        
        return path
    
    # Tìm kiếm bidirectional với cải tiến
    iteration = 0
    while queue_start and queue_end:
        iteration += 1
        if show_progress and iteration % 10 == 0:
            print(f"Iteration {iteration}: Queue sizes - Start: {len(queue_start)}, End: {len(queue_end)}")
        
        # Luôn mở rộng từ queue nhỏ hơn để cân bằng
        if len(queue_start) <= len(queue_end):
            # Mở rộng từ điểm bắt đầu
            if queue_start:
                current_start = queue_start.popleft()
                nodes_explored += 1
                
                for dx, dy in directions:
                    new_x, new_y = current_start[0] + dx, current_start[1] + dy
                    new_pos = (new_x, new_y)
                    
                    if is_valid(new_x, new_y) and new_pos not in visited_start:
                        parent_start[new_pos] = current_start
                        visited_start.add(new_pos)
                        all_visited.add(new_pos)
                        queue_start.append(new_pos)
                        
                        # Kiểm tra gặp nhau
                        if new_pos in visited_end:
                            end_time = time.time()
                            path = reconstruct_path(new_pos)
                            return {
                                "path": path,
                                "stats": {
                                    "nodes_explored": nodes_explored,
                                    "time_taken": end_time - start_time,
                                    "path_length": len(path),
                                    "iterations": iteration
                                },
                                "visited_cells": all_visited
                            }
        else:
            # Mở rộng từ điểm kết thúc
            if queue_end:
                current_end = queue_end.popleft()
                nodes_explored += 1
                
                for dx, dy in directions:
                    new_x, new_y = current_end[0] + dx, current_end[1] + dy
                    new_pos = (new_x, new_y)
                    
                    if is_valid(new_x, new_y) and new_pos not in visited_end:
                        parent_end[new_pos] = current_end
                        visited_end.add(new_pos)
                        all_visited.add(new_pos)
                        queue_end.append(new_pos)
                        
                        # Kiểm tra gặp nhau
                        if new_pos in visited_start:
                            end_time = time.time()
                            path = reconstruct_path(new_pos)
                            return {
                                "path": path,
                                "stats": {
                                    "nodes_explored": nodes_explored,
                                    "time_taken": end_time - start_time,
                                    "path_length": len(path),
                                    "iterations": iteration
                                },
                                "visited_cells": all_visited
                            }
    
    # Không tìm thấy đường đi
    end_time = time.time()
    return {
        "path": [],
        "stats": {
            "nodes_explored": nodes_explored,
            "time_taken": end_time - start_time,
            "path_length": 0,
            "iterations": iteration
        },
        "visited_cells": all_visited
    }

def visualize_maze_with_path(maze, result, start, end):
    """Hiển thị mê cung với đường đi và các ô đã thăm"""
    if not result["path"]:
        print("Không tìm thấy đường đi!")
        return
    
    maze_copy = [row[:] for row in maze]
    
    # Đánh dấu các ô đã thăm
    for x, y in result["visited_cells"]:
        if (x, y) != start and (x, y) != end and (x, y) not in result["path"]:
            maze_copy[x][y] = 3  # Ô đã thăm nhưng không nằm trên đường đi
    
    # Đánh dấu đường đi
    for x, y in result["path"]:
        if (x, y) != start and (x, y) != end:
            maze_copy[x][y] = 2  # Đường đi
    
    print("\nMê cung với kết quả:")
    print("S: Start, E: End, *: Đường đi, .: Ô trống, #: Tường, ~: Đã thăm")
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
            elif cell == 3:
                print('~', end=' ')
        print()

def compare_algorithms(maze, start, end):
    """So sánh hiệu suất giữa các chế độ khác nhau"""
    print("=== SO SÁNH HIỆU SUẤT ===")
    
    # Bidirectional BFS thường
    result1 = solve_maze_bidirectional_bfs(maze, start, end)
    print(f"BFS 2 chiều (4 hướng): {result1['stats']}")
    
    # Bidirectional BFS với đường chéo
    result2 = solve_maze_bidirectional_bfs(maze, start, end, allow_diagonal=True)
    print(f"BFS 2 chiều (8 hướng): {result2['stats']}")
    
    return result1, result2
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
    
    # Test cải thiện
    print("=== BIDIRECTIONAL BFS CẢI TIẾN ===")
    result = solve_maze_bidirectional_bfs(maze, start, end, show_progress=True)
    
    print(f"\nKết quả:")
    print(f"Đường đi: {result['path']}")
    print(f"Thống kê: {result['stats']}")
    
    # Hiển thị mê cung
    visualize_maze_with_path(maze, result, start, end)
    
    # So sánh các chế độ
    compare_algorithms(maze, start, end)