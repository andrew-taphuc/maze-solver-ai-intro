def solve_maze_dfs_with_visualization(grid_cells, start, end, delay_callback=None):
    """
    Giải mê cung sử dụng thuật toán DFS với khả năng visualization
    
    Args:
        grid_cells: Danh sách các cell trong mê cung
        start: Cell bắt đầu  
        end: Cell kết thúc
        delay_callback: Hàm callback để tạo delay cho visualization
    
    Returns:
        List các cell tạo thành đường đi từ start đến end, hoặc None nếu không có đường đi
    """
    for cell in grid_cells:
        cell.visited = False
        cell.is_solution = False
    
    stack = []
    parent = {}
    
    stack.append(start)
    parent[start] = None
    start.visited = True
    
    while stack:
        current_cell = stack.pop()
        
        if delay_callback:
            delay_callback()
        
        if current_cell == end:
            path = []
            while current_cell is not None:
                path.append(current_cell)
                current_cell = parent[current_cell]
            
            path.reverse()
            
            for cell in path:
                cell.is_solution = True
            
            return path
        
        neighbors = current_cell.check_neighbors_for_search(grid_cells)
        
        for neighbor in neighbors:
            if not neighbor.visited:
                neighbor.visited = True
                parent[neighbor] = current_cell
                stack.append(neighbor)
    
    return None