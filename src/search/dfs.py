def solve_maze_dfs(grid_cells, start, end):
    """
    Giải mê cung sử dụng thuật toán DFS (Depth-First Search)
    
    Args:
        grid_cells: Danh sách các cell trong mê cung
        start: Cell bắt đầu
        end: Cell kết thúc
    
    Returns:
        List các cell tạo thành đường đi từ start đến end, hoặc None nếu không có đường đi
    """
    stack = []
    parent = {}
    
    stack.append(start)
    parent[start] = None
    start.visited = True
    
    while stack:
        current_cell = stack.pop()
        
        if current_cell == end:
            path = []
            while current_cell is not None:
                path.append(current_cell)
                current_cell = parent[current_cell]
            path.reverse()
            return path
        
        neighbors = current_cell.check_neighbors_for_search(grid_cells)
        
        for neighbor in neighbors:
            if not neighbor.visited:
                neighbor.visited = True
                parent[neighbor] = current_cell
                stack.append(neighbor)
    
    return None