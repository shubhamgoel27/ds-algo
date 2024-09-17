from typing import List

class Solution:
    def minSwaps(self, data: List[int]) -> int:
        """
        Calculate the minimum number of swaps required to group all 1's together in the binary array.

        Args:
        data (List[int]): A binary array containing only 0's and 1's.

        Returns:
        int: The minimum number of swaps needed to group all 1's together.

        Time complexity: O(n), where n is the length of the input array.
        Space complexity: O(1), as we use only a constant amount of extra space.
        """
        # Count total number of 1's in the array
        ones = sum(data)
        n = len(data)
        
        # Initialize variables for sliding window
        curr_zeros = 0
        min_zeros = float("inf")
        
        # Count zeros in the first window of size 'ones'
        for i in range(ones):
            if data[i] == 0:
                curr_zeros += 1
        
        # Initialize min_zeros with the first window
        min_zeros = curr_zeros
        
        # Slide the window and update min_zeros
        for i in range(ones, n):
            if data[i - ones] == 0:
                curr_zeros -= 1  # Remove the leftmost element from the window
            if data[i] == 0:
                curr_zeros += 1  # Add the rightmost element to the window
            min_zeros = min(min_zeros, curr_zeros)
        
        return min_zeros

# Test cases
def test_min_swaps():
    solution = Solution()
    
    # Test case 1: Already grouped
    assert solution.minSwaps([1,1,1,0,0]) == 0
    
    # Test case 2: Needs swaps
    assert solution.minSwaps([1,0,1,0,1]) == 1
    
    # Test case 3: All zeros
    assert solution.minSwaps([0,0,0,0,0]) == 0
    
    # Test case 4: All ones
    assert solution.minSwaps([1,1,1,1,1]) == 0
    
    # Test case 5: Alternating
    assert solution.minSwaps([1,0,1,0,1,0]) == 1
    
    print("All test cases passed!")

# Run the test cases
test_min_swaps()

"""
Broad hints for solving this problem:

1. Sliding Window Technique:
   - The key insight is to use a sliding window of size equal to the total number of 1's in the array.
   - This window represents the optimal position where all 1's should be grouped.

2. Counting Zeros:
   - Instead of counting 1's, focus on counting 0's within the window.
   - The number of 0's in the window represents the number of swaps needed.

3. Minimizing Swaps:
   - As you slide the window, keep track of the minimum number of 0's encountered.
   - This minimum will give you the minimum number of swaps required.

4. Efficient Counting:
   - Use a running count to efficiently update the number of 0's in the window as it slides.
   - Add 0's entering the window and subtract 0's leaving the window.

5. Edge Cases:
   - Consider arrays with all 0's, all 1's, or already grouped 1's.

6. Time and Space Complexity:
   - Aim for a single pass through the array (O(n) time complexity).
   - Try to use only a constant amount of extra space (O(1) space complexity).

Remember: The problem is essentially asking to find the window with the maximum number of 1's,
which is equivalent to finding the window with the minimum number of 0's.
"""
