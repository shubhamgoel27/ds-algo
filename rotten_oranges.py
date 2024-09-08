from collections import deque
from typing import List

class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        """
        Determine the minimum number of minutes until no cell has a fresh orange.
        
        Args:
        grid (List[List[int]]): A grid where 0 represents an empty cell,
                                1 represents a fresh orange, and
                                2 represents a rotten orange.
        
        Returns:
        int: The minimum number of minutes until no cell has a fresh orange.
             Returns -1 if it's impossible to rot all oranges.
        """
        total_fresh = 0
        rotten_oranges = []
        m, n = len(grid), len(grid[0])
        
        # Count fresh oranges and find initial rotten oranges
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    total_fresh += 1
                elif grid[i][j] == 2:
                    rotten_oranges.append((i, j))
        
        # Edge cases
        if not rotten_oranges and not total_fresh:
            return 0  # No oranges at all
        if not rotten_oranges:
            return -1  # Only fresh oranges, impossible to rot all
        
        t = 0  # Time counter
        new_rotten = 0  # Counter for newly rotten oranges
        
        # BFS to rot oranges
        q = deque([(r, c, 0) for r, c in rotten_oranges])  # (row, col, time)
        while q:
            r, c, curr_t = q.popleft()
            dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]  # 4 directions: up, down, right, left
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                    grid[nr][nc] = 2  # Rot the orange
                    new_rotten += 1
                    q.append((nr, nc, curr_t + 1))
                    t = curr_t + 1  # Update the time
        
        # Check if all fresh oranges were rotten
        return t if new_rotten == total_fresh else -1

# Test cases
def test_oranges_rotting():
    sol = Solution()
    
    # Test case 1: All oranges can be rotten
    grid1 = [[2,1,1],[1,1,0],[0,1,1]]
    assert sol.orangesRotting(grid1) == 4
    
    # Test case 2: Impossible to rot all oranges
    grid2 = [[2,1,1],[0,1,1],[1,0,1]]
    assert sol.orangesRotting(grid2) == -1
    
    # Test case 3: No fresh oranges initially
    grid3 = [[0,2]]
    assert sol.orangesRotting(grid3) == 0
    
    # Test case 4: Empty grid
    grid4 = [[]]
    assert sol.orangesRotting(grid4) == 0
    
    print("All test cases passed!")

# Run the tests
test_oranges_rotting()

# Broad hints for solving this problem:
# 1. Use a breadth-first search (BFS) approach to simulate the rotting process.
# 2. Keep track of the time and the number of fresh oranges that become rotten.
# 3. Use a queue to store the positions of rotten oranges and their "rotting time".
# 4. Process the grid layer by layer, rotting adjacent fresh oranges.
# 5. Pay attention to edge cases: no oranges, only fresh oranges, etc.
# 6. The time taken is the time when the last fresh orange becomes rotten.
# 7. Compare the number of newly rotten oranges with the initial count of fresh oranges.
