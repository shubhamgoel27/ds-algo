from collections import deque
from typing import List
import copy

class Solution:
    """
    A class to solve the Number of Islands problem.
    """

    def numIslands(self, grid: List[List[str]]) -> int:
        """
        Count the number of islands in the given grid.

        An island is formed by connecting adjacent lands horizontally or vertically.

        Args:
            grid (List[List[str]]): A 2D grid where '1' represents land and '0' represents water.

        Returns:
            int: The number of islands in the grid.
        """
        if not grid or not grid[0]:
            return 0 
        count = 0
        m, n = len(grid), len(grid[0])
        for i in range(m):
            for j in range(n):
                if grid[i][j] == "1":
                    count += 1
                    self.bfs(grid, i, j)  # You can use either BFS or DFS here
        return count

    def bfs(self, grid: List[List[str]], i: int, j: int) -> None:
        """
        Perform Breadth-First Search to mark all connected land cells as visited.

        Args:
            grid (List[List[str]]): The 2D grid.
            i (int): Starting row index.
            j (int): Starting column index.
        """
        dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        grid[i][j] = "#"  # Mark as visited
        queue = deque([(i, j)])
        while queue:
            r, c = queue.popleft()
            for dx, dy in dirs:
                nr, nc = r + dx, c + dy
                if self.is_valid(grid, nr, nc) and grid[nr][nc] == "1":
                    grid[nr][nc] = "#"  # Mark as visited
                    queue.append((nr, nc))

    def dfs(self, grid: List[List[str]], i: int, j: int) -> None:
        """
        Perform Depth-First Search to mark all connected land cells as visited.

        Args:
            grid (List[List[str]]): The 2D grid.
            i (int): Starting row index.
            j (int): Starting column index.
        """
        dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        grid[i][j] = "#"  # Mark as visited
        for dx, dy in dirs:
            nr, nc = i + dx, j + dy
            if self.is_valid(grid, nr, nc) and grid[nr][nc] == "1":
                self.dfs(grid, nr, nc)

    def is_valid(self, grid: List[List[str]], r: int, c: int) -> bool:
        """
        Check if the given coordinates are valid within the grid.

        Args:
            grid (List[List[str]]): The 2D grid.
            r (int): Row index to check.
            c (int): Column index to check.

        Returns:
            bool: True if the coordinates are valid, False otherwise.
        """
        return 0 <= r < len(grid) and 0 <= c < len(grid[0])

    def numIslandsBFS(self, grid: List[List[str]]) -> int:
        """
        Count the number of islands using BFS.
        """
        if not grid or not grid[0]:
            return 0 
        count = 0
        m, n = len(grid), len(grid[0])
        for i in range(m):
            for j in range(n):
                if grid[i][j] == "1":
                    count += 1
                    self.bfs(grid, i, j)
        return count

    def numIslandsDFS(self, grid: List[List[str]]) -> int:
        """
        Count the number of islands using DFS.
        """
        if not grid or not grid[0]:
            return 0 
        count = 0
        m, n = len(grid), len(grid[0])
        for i in range(m):
            for j in range(n):
                if grid[i][j] == "1":
                    count += 1
                    self.dfs(grid, i, j)
        return count

# Test cases
def test_numIslandsBFS():
    solution = Solution()

    # Test case 1: Normal case
    grid1 = [
        ["1","1","1","1","0"],
        ["1","1","0","1","0"],
        ["1","1","0","0","0"],
        ["0","0","0","0","0"]
    ]
    assert solution.numIslandsBFS(copy.deepcopy(grid1)) == 1

    # Test case 2: Multiple islands
    grid2 = [
        ["1","1","0","0","0"],
        ["1","1","0","0","0"],
        ["0","0","1","0","0"],
        ["0","0","0","1","1"]
    ]
    assert solution.numIslandsBFS(copy.deepcopy(grid2)) == 3

    # Test case 3: Empty grid
    grid3 = []
    assert solution.numIslandsBFS(copy.deepcopy(grid3)) == 0

    # Test case 4: Single cell grid
    grid4 = [["1"]]
    assert solution.numIslandsBFS(copy.deepcopy(grid4)) == 1

    # Test case 5: All water
    grid5 = [
        ["0","0","0"],
        ["0","0","0"],
        ["0","0","0"]
    ]
    assert solution.numIslandsBFS(copy.deepcopy(grid5)) == 0

    print("All BFS test cases passed!")

def test_numIslandsDFS():
    solution = Solution()

    # Test case 1: Normal case
    grid1 = [
        ["1","1","1","1","0"],
        ["1","1","0","1","0"],
        ["1","1","0","0","0"],
        ["0","0","0","0","0"]
    ]
    assert solution.numIslandsDFS(copy.deepcopy(grid1)) == 1

    # Test case 2: Multiple islands
    grid2 = [
        ["1","1","0","0","0"],
        ["1","1","0","0","0"],
        ["0","0","1","0","0"],
        ["0","0","0","1","1"]
    ]
    assert solution.numIslandsDFS(copy.deepcopy(grid2)) == 3

    # Test case 3: Empty grid
    grid3 = []
    assert solution.numIslandsDFS(copy.deepcopy(grid3)) == 0

    # Test case 4: Single cell grid
    grid4 = [["1"]]
    assert solution.numIslandsDFS(copy.deepcopy(grid4)) == 1

    # Test case 5: All water
    grid5 = [
        ["0","0","0"],
        ["0","0","0"],
        ["0","0","0"]
    ]
    assert solution.numIslandsDFS(copy.deepcopy(grid5)) == 0

    print("All DFS test cases passed!")

# Run the tests
if __name__ == "__main__":
    test_numIslandsBFS()
    test_numIslandsDFS()