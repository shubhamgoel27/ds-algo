from typing import List
from collections import deque
import copy

class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        """
        Find the maximum area of an island in the given grid.

        An island is a group of 1's (representing land) connected 4-directionally (horizontal or vertical).
        The grid is represented by a 2D array of 0's (water) and 1's (land).

        Args:
            grid (List[List[int]]): The 2D grid representing the map.

        Returns:
            int: The maximum area of an island in the grid.
        """
        m, n = len(grid), len(grid[0])
        max_area = 0

        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    # Start DFS when we find a land cell
                    self.curr_area = 0
                    self.dfs(grid, i, j)
                    max_area = max(max_area, self.curr_area)
        return max_area
    
    def dfs(self, grid: List[List[int]], i: int, j: int) -> None:
        """
        Perform Depth-First Search to explore and mark connected land cells.

        Args:
            grid (List[List[int]]): The 2D grid representing the map.
            i (int): Current row index.
            j (int): Current column index.
        """
        m, n = len(grid), len(grid[0])
        
        # Check if current cell is out of bounds or not land
        if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] != 1:
            return
        
        # Mark current cell as visited and increment area
        grid[i][j] = "#"
        self.curr_area += 1
        
        # Explore in all four directions
        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dy, dx in dirs:
            self.dfs(grid, i + dy, j + dx)

    def bfs(self, grid: List[List[int]], start_i: int, start_j: int) -> int:
        """
        Perform Breadth-First Search to explore and mark connected land cells.

        Args:
            grid (List[List[int]]): The 2D grid representing the map.
            start_i (int): Starting row index.
            start_j (int): Starting column index.

        Returns:
            int: The area of the island starting from the given cell.
        """
        m, n = len(grid), len(grid[0])
        queue = deque([(start_i, start_j)])
        grid[start_i][start_j] = "#"  # Mark as visited
        area = 1

        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        while queue:
            i, j = queue.popleft()
            for dy, dx in dirs:
                ni, nj = i + dy, j + dx
                if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == 1:
                    grid[ni][nj] = "#"  # Mark as visited
                    queue.append((ni, nj))
                    area += 1

        return area

    def maxAreaOfIslandBFS(self, grid: List[List[int]]) -> int:
        """
        Find the maximum area of an island in the given grid using BFS.

        Args:
            grid (List[List[int]]): The 2D grid representing the map.

        Returns:
            int: The maximum area of an island in the grid.
        """
        m, n = len(grid), len(grid[0])
        max_area = 0

        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    max_area = max(max_area, self.bfs(grid, i, j))

        return max_area

# Test cases
def test_maxAreaOfIsland():
    solution = Solution()
    
    # Test case 1: Grid with multiple islands
    grid1 = [
        [0,0,1,0,0,0,0,1,0,0,0,0,0],
        [0,0,0,0,0,0,0,1,1,1,0,0,0],
        [0,1,1,0,1,0,0,0,0,0,0,0,0],
        [0,1,0,0,1,1,0,0,1,0,1,0,0],
        [0,1,0,0,1,1,0,0,1,1,1,0,0],
        [0,0,0,0,0,0,0,0,0,0,1,0,0],
        [0,0,0,0,0,0,0,1,1,1,0,0,0],
        [0,0,0,0,0,0,0,1,1,0,0,0,0]
    ]
    assert solution.maxAreaOfIsland(copy.deepcopy(grid1)) == 6
    assert solution.maxAreaOfIslandBFS(copy.deepcopy(grid1)) == 6

    # Test case 2: Grid with no islands
    grid2 = [[0,0,0,0,0,0,0,0]]
    assert solution.maxAreaOfIsland(copy.deepcopy(grid2)) == 0
    assert solution.maxAreaOfIslandBFS(copy.deepcopy(grid2)) == 0

    # Test case 3: Grid with one large island
    grid3 = [
        [1,1,1],
        [1,1,1],
        [1,1,1]
    ]
    assert solution.maxAreaOfIsland(copy.deepcopy(grid3)) == 9
    assert solution.maxAreaOfIslandBFS(copy.deepcopy(grid3)) == 9

    print("All test cases passed!")

# Run the test cases
test_maxAreaOfIsland()

# Hints for solving this problem:
# 1. Use Depth-First Search (DFS) or Breadth-First Search (BFS) to explore connected land cells.
# 2. Keep track of visited cells to avoid counting them multiple times.
# 3. Implement helper functions for DFS and BFS to make the code more modular and flexible.
# 4. Use a direction array to simplify exploring adjacent cells.
# 5. Remember to handle edge cases, such as empty grids or grids with no islands.
# 6. Consider the trade-offs between DFS and BFS:
#    - DFS is often simpler to implement recursively and uses less memory for narrow, deep graphs.
#    - BFS is better for finding the shortest path and uses less memory for wide, shallow graphs.
# 7. Practice similar problems like "Number of Islands" to reinforce your understanding.
