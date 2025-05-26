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
    if start == end:
        return [start]
    
    for cell in grid_cells:
        cell.visited = False
    
    stack = [start]
    parent = {start: None}
    start.visited = True
    
    while stack:
        current = stack.pop()
        
        if current == end:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1]
        
        for neighbor in current.check_neighbors_for_search(grid_cells):
            if not neighbor.visited:
                neighbor.visited = True
                parent[neighbor] = current
                stack.append(neighbor)
    
    return None