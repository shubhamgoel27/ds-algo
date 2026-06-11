from typing import List
from collections import deque
import copy


class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        """Largest 4-directionally connected island (cell count). O(m*n).

        Return-value flood fill: dfs(i, j) returns the area of the blob reachable
        from (i, j). A guard clause at the top makes every call safe (off-grid,
        water, or already-sunk land all return 0), so the four recursive calls
        need no pre-checks. Sinking a visited cell to 0 is the visited marker.
        """
        m, n = len(grid), len(grid[0])

        def dfs(i, j):
            if not (0 <= i < m and 0 <= j < n) or grid[i][j] != 1:
                return 0
            grid[i][j] = 0                       # mark visited by sinking the cell
            return 1 + dfs(i + 1, j) + dfs(i - 1, j) + dfs(i, j + 1) + dfs(i, j - 1)

        max_area = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:              # a fresh, unvisited island start
                    max_area = max(max_area, dfs(i, j))
        return max_area

    def maxAreaOfIslandBFS(self, grid: List[List[int]]) -> int:
        """Iterative alternative (safe for huge grids that would overflow recursion).

        Mark each cell visited the moment it is enqueued, never when dequeued, so
        no cell is queued twice.
        """
        m, n = len(grid), len(grid[0])
        DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))
        max_area = 0

        for i in range(m):
            for j in range(n):
                if grid[i][j] != 1:
                    continue
                grid[i][j] = 0
                area = 0
                q = deque([(i, j)])
                while q:
                    r, c = q.popleft()
                    area += 1
                    for dr, dc in DIRS:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                            grid[nr][nc] = 0      # mark on enqueue
                            q.append((nr, nc))
                max_area = max(max_area, area)
        return max_area


def test_maxAreaOfIsland():
    solution = Solution()

    grid1 = [
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    ]
    assert solution.maxAreaOfIsland(copy.deepcopy(grid1)) == 6
    assert solution.maxAreaOfIslandBFS(copy.deepcopy(grid1)) == 6

    grid2 = [[0, 0, 0, 0, 0, 0, 0, 0]]
    assert solution.maxAreaOfIsland(copy.deepcopy(grid2)) == 0
    assert solution.maxAreaOfIslandBFS(copy.deepcopy(grid2)) == 0

    grid3 = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    assert solution.maxAreaOfIsland(copy.deepcopy(grid3)) == 9
    assert solution.maxAreaOfIslandBFS(copy.deepcopy(grid3)) == 9

    print("All test cases passed!")


if __name__ == "__main__":
    test_maxAreaOfIsland()
