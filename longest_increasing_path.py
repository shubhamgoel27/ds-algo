from typing import List

class Solution:
    def longestIncreasingPath(self, grid: List[List[int]]) -> int:
        """
        Find the length of the longest increasing path in a grid.
        
        Args:
        grid (List[List[int]]): A 2D grid of integers.
        
        Returns:
        int: The length of the longest increasing path.
        
        Time complexity: O(rows * cols), where rows and cols are the dimensions of the grid.
        Space complexity: O(rows * cols) for the memoization array.
        """
        if not grid or not grid[0]:
            return 0
        
        rows, cols = len(grid), len(grid[0])
        cache = [[-1] * cols for _ in range(rows)]  # Memoization array

        def dfs(row: int, col: int) -> int:
            # If already computed, return cached result
            if cache[row][col] != -1:
                return cache[row][col]
            
            longest_path = 1  # At least the cell itself
            
            # Check all four directions
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for d_row, d_col in directions:
                next_row, next_col = row + d_row, col + d_col
                # If within bounds and next cell is greater, explore that path
                if (0 <= next_row < rows and 0 <= next_col < cols and 
                    grid[next_row][next_col] > grid[row][col]):
                    longest_path = max(longest_path, 1 + dfs(next_row, next_col))
            
            # Cache the result for current cell
            cache[row][col] = longest_path
            return longest_path

        # Find the maximum path starting from each cell
        max_path_length = 0
        for row in range(rows):
            for col in range(cols):
                max_path_length = max(max_path_length, dfs(row, col))
        return max_path_length

# Test cases
def test_longest_increasing_path():
    solution = Solution()
    
    # Test case 1: Simple 3x3 grid
    assert solution.longestIncreasingPath([[9,9,4],[6,6,8],[2,1,1]]) == 4
    
    # Test case 2: 3x3 grid with multiple paths
    assert solution.longestIncreasingPath([[3,4,5],[3,2,6],[2,2,1]]) == 4
    
    # Test case 3: 1x1 grid
    assert solution.longestIncreasingPath([[1]]) == 1
    
    # Test case 4: Empty grid
    assert solution.longestIncreasingPath([]) == 0
    
    print("All test cases passed!")

# Run the tests
test_longest_increasing_path()

"""
Hints for solving this problem:

1. This is a graph problem where each cell is a node, and edges exist between
   adjacent cells with increasing values.

2. Use depth-first search (DFS) to explore all possible paths from each cell.

3. Implement memoization to avoid redundant calculations, as many paths will
   overlap.

4. The base case for the DFS is when a cell has no valid neighbors (higher values).

5. The final answer is the maximum path length found starting from any cell.

6. Be careful with the grid boundaries when exploring neighbors.

7. Time complexity can be reduced from exponential to O(rows * cols) with memoization.

8. Consider edge cases like empty grids or single-cell grids.
"""