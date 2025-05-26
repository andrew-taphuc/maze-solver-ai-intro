from collections import deque

def solve_maze_bfs(maze, start, end):
    """
    Giải mê cung bằng cách sử dụng BFS.

    Hàm thực hiện BFS để khám phá tất cả các đường dẫn có thể từ ô bắt đầu (phần tử đầu tiên trong
    grid_cells) đến ô đích (phần tử cuối cùng trong grid_cells). Trực quan hóa quá trình tìm kiếm
    bằng cách cập nhật màn hình (sử dụng pygame) khi quá trình tìm kiếm diễn ra và khi đến đích,
    hàm sẽ tái tạo và trả về đường dẫn từ điểm bắt đầu đến đích.

    Args:
    - grid_cells (List[Cell]): Danh sách tất cả các ô trong mê cung, mỗi ô là một đối tượng có các thuộc tính
    như các ô lân cận, trạng thái đã ghé thăm và các phương thức để kiểm tra các ô lân cận và tự vẽ chính nó.
    - sc (pygame.Surface): Bề mặt màn hình pygame được sử dụng để vẽ mê cung và trực quan hóa quá trình tìm kiếm

    Return:
    - path (List[Cell]): đường dẫn từ điểm bắt đầu của mê cung đến ô đích nếu không thì Không có
    - visited_cells_count (int): Tổng số ô đã ghé thăm trong quá trình tìm kiếm.
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