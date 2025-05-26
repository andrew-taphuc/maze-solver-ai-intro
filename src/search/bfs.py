import pygame
from config import *
from typing import List
from cell import Cell
from utils import draw_text_of_running_alg, reconstruct_path, draw_button

def solve_maze_BFS(grid_cells: List[Cell], sc: pygame.Surface):
    """
    Giải mê cung sử dụng thuật toán bfs
    
    Args:
        maze: Ma trận mê cung (0: đường đi, 1: tường)
        start: Vị trí bắt đầu (x, y)
        end: Vị trí kết thúc (x, y)
    
    Returns:
        List các vị trí tạo thành đường đi từ start đến end
    """
    # Xác định ô bắt đầu và ô kết thúc
    start_cell = grid_cells[0]
    destination_cell = grid_cells[-1]

    # Khởi tạo các cấu trúc cần thiết cho BFS và truy vết đường đi
    queue = []
    parent = {}
    queue.append(start_cell)
    parent[start_cell] = None

    # Biến đếm số ô đã duyệt
    visited_cells_count = 0

    # Vòng lặp chính của BFS
    while queue:
        # Lấy ô đầu tiên ra khỏi hàng đợi và đánh dấu là đã duyệt
        current_cell = queue.pop(0)
        current_cell.visited = True
        visited_cells_count += 1

        # Tạm dừng để trực quan hóa thuật toán
        pygame.time.delay(60) 
        pygame.display.flip()

        # Vẽ lại toàn bộ mê cung ở mỗi vòng lặp để giữ các ô luôn hiển thị
        for cell in grid_cells:
            cell.draw(sc)

        # Hiển thị trạng thái hiện tại của thuật toán
        draw_text_of_running_alg(sc, "RUNNING: BFS", FONT, 17, 20, 200, "#FFFFFF")
        draw_text_of_running_alg(sc, "CELLS EXPLORED: " + str(visited_cells_count), FONT, 17, 20, 230, "#FFFFFF")

        # Hiển thị các nút chức năng
        draw_button(sc, "GENERATE MAZE", 20, 300, BUTTON_COLOR)
        draw_button(sc, "BFS", 20, 400, BUTTON_COLOR)
        draw_button(sc, "DFS", 20, 350, BUTTON_COLOR)
        draw_button(sc, "BIDIRECTIONAL BFS", 20, 450, BUTTON_COLOR)
        draw_button(sc, "A STAR", 20, 500, BUTTON_COLOR)
        draw_button(sc, "GBFS", 20, 550, BUTTON_COLOR)

        # Vẽ ô vừa được duyệt
        current_cell.draw(sc)

        # Kiểm tra nếu ô hiện tại là ô kết thúc
        if current_cell == destination_cell:
            # Nếu đã đến đích, truy vết và trả về đường đi
            path = reconstruct_path(sc, parent, start_cell, destination_cell)
            return path, visited_cells_count

        # Kiểm tra các ô hàng xóm và mở rộng tìm kiếm BFS
        neighbors = current_cell.check_neighbors_for_search(grid_cells)
        for neighbor in neighbors:
            if not neighbor.visited:
                # Thêm ô hàng xóm vào hàng đợi để duyệt sau
                queue.append(neighbor)
                # Gán ô hiện tại là cha của ô hàng xóm này
                parent[neighbor] = current_cell 
    
    return None, visited_cells_count
