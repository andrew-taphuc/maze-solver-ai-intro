import pygame
import heapq  
from config import *
from typing import List
from cell import Cell
from utils import reconstruct_path, manhattan_distance, draw_text_of_running_alg, draw_button

def solve_maze_A_star(grid_cells: List[Cell], sc: pygame.Surface):
    """
    Giải mê cung sử dụng thuật toán A* (A-star)
    
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

    # Biến đếm số ô đã duyệt
    visited_cells_count = 0

    # Hàng đợi ưu tiên cho tập mở (chứa các ô sẽ được đánh giá), mỗi phần tử là (f_cost, id, cell)
    open_set = []
    heapq.heappush(open_set, (0, id(start_cell), start_cell))

    # G cost: khoảng cách thực tế từ ô bắt đầu đến ô hiện tại
    g_cost = {cell: float('inf') for cell in grid_cells}
    # Khởi tạo g_cost cho tất cả các ô là vô cùng
    g_cost[start_cell] = 0  # g_cost của ô bắt đầu là 0

    # F cost: G cost + heuristic (ước lượng khoảng cách đến đích)
    f_cost = {cell: float('inf') for cell in grid_cells}
    # Khởi tạo f_cost cho tất cả các ô là vô cùng
    f_cost[start_cell] = manhattan_distance(start_cell, destination_cell)  
    # f_cost của ô bắt đầu là heuristic đến ô đích

    # Khởi tạo parent để truy vết đường đi
    parent = {}
    parent[start_cell] = None

    # Vòng lặp chính của thuật toán A*
    while open_set:
        # Lấy ô có f_cost nhỏ nhất ra khỏi hàng đợi ưu tiên
        _, _, current_cell = heapq.heappop(open_set)
        # Đánh dấu ô hiện tại là đã duyệt
        current_cell.visited = True
        visited_cells_count += 1

        # Nếu đã đến đích, truy vết và trả về đường đi
        if current_cell == destination_cell:
            path = reconstruct_path(sc, parent, start_cell, destination_cell)
            return path, visited_cells_count

        # Vẽ lại toàn bộ mê cung ở mỗi vòng lặp để giữ các ô luôn hiển thị
        for cell in grid_cells:
            cell.draw(sc)

        # Vẽ ô vừa được duyệt
        current_cell.draw(sc)

        # Hiển thị trạng thái hiện tại của thuật toán
        draw_text_of_running_alg(sc, "RUNNING: A Star", FONT, 17, 20, 200, "#FFFFFF")
        draw_text_of_running_alg(sc, "CELLS EXPLORED: " + str(visited_cells_count), FONT, 17, 20, 230, "#FFFFFF")

        # Hiển thị các nút chức năng
        draw_button(sc, "GENERATE MAZE", 20, 300, BUTTON_COLOR)
        draw_button(sc, "BFS", 20, 400, BUTTON_COLOR)
        draw_button(sc, "DFS", 20, 350, BUTTON_COLOR)
        draw_button(sc, "BIDIRECTIONAL BFS", 20, 450, BUTTON_COLOR)
        draw_button(sc, "A STAR", 20, 500, BUTTON_COLOR)
        draw_button(sc, "GBFS", 20, 550, BUTTON_COLOR)
        
        # Tạm dừng để trực quan hóa thuật toán
        pygame.time.delay(60)
        pygame.display.flip()

        # Duyệt các ô hàng xóm của ô hiện tại
        neighbors = current_cell.check_neighbors_for_search(grid_cells)
        for neighbor in neighbors:
            # Bỏ qua các ô đã duyệt
            if neighbor.visited:
                continue

            # Tính g_cost tạm thời (khoảng cách từ start đến neighbor qua current_cell)
            tentative_g_cost = g_cost[current_cell] + 1  # Khoảng cách giữa hai ô kề nhau là 1
            # Nếu tìm được đường đi ngắn hơn đến neighbor
            if tentative_g_cost < g_cost[neighbor]:
                # Gán ô cha cho neighbor là current_cell
                parent[neighbor] = current_cell
                # Cập nhật g_cost cho neighbor
                g_cost[neighbor] = tentative_g_cost
                # Cập nhật f_cost với g_cost mới và heuristic (khoảng cách Manhattan)
                f_cost[neighbor] = g_cost[neighbor] + manhattan_distance(neighbor, destination_cell)

                # Thêm neighbor vào open_set nếu chưa có
                if neighbor not in [item[2] for item in open_set]:
                    heapq.heappush(open_set, (f_cost[neighbor], id(neighbor), neighbor))
    
    return None, visited_cells_count
