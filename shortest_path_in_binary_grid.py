from typing import List 
from collections import deque
class Solution:
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        n = len(grid)
        if grid[0][0] != 0 or grid[n-1][n-1] != 0:
            return -1

        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

        queue = deque([(0, 0, 1)])  # (row, col, path_length)
        visited = set((0, 0))

        while queue:
            row, col, path_length = queue.popleft()
            
            if (row, col) == (n-1, n-1):
                return path_length

            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc

                if 0 <= new_row < n and 0 <= new_col < n and (new_row, new_col) not in visited and grid[new_row][new_col] == 0:
                    queue.append((new_row, new_col, path_length + 1))
                    visited.add((new_row, new_col))

        return -1
    
def test_shortestPathBinaryMatrix():
    solution = Solution()

    # Test Case 1: Path is blocked at the start
    grid1 = [
        [1, 0],
        [0, 0]
    ]
    assert solution.shortestPathBinaryMatrix(grid1) == -1, "Test Case 1 Failed"

    # Test Case 2: Path is blocked at the end
    grid2 = [
        [0, 0],
        [0, 1]
    ]
    assert solution.shortestPathBinaryMatrix(grid2) == -1, "Test Case 2 Failed"

    # Test Case 3: Small grid with clear path
    grid3 = [
        [0, 1],
        [1, 0]
    ]
    assert solution.shortestPathBinaryMatrix(grid3) == 2, "Test Case 3 Failed"

    # Test Case 4: Larger grid with clear path
    grid4 = [
        [0, 0, 0],
        [1, 1, 0],
        [1, 1, 0]
    ]
    assert solution.shortestPathBinaryMatrix(grid4) == 4, "Test Case 4 Failed"

    # Test Case 5: Path is not possible
    grid5 = [
        [0, 1, 1],
        [1, 1, 1],
        [1, 1, 0]
    ]
    assert solution.shortestPathBinaryMatrix(grid5) == -1, "Test Case 5 Failed"

    # Test Case 6: Single cell grid
    grid6 = [
        [0]
    ]
    assert solution.shortestPathBinaryMatrix(grid6) == 1, "Test Case 6 Failed"

    # Test Case 7: Larger grid with multiple paths
    grid7 = [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ]
    assert solution.shortestPathBinaryMatrix(grid7) == 8, "Test Case 7 Failed"

    print("All test cases passed!")

if __name__ == "__main__":
    test_shortestPathBinaryMatrix()