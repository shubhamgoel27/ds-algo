from typing import List

class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        """
        Find the length of the longest contiguous subarray with at most k zeros.

        Args:
        nums (List[int]): A binary array (containing only 0 and 1).
        k (int): The maximum number of zeros allowed to be flipped.

        Returns:
        int: The length of the longest contiguous subarray that contains only 1s after flipping at most k 0s.

        Example:
        >>> s = Solution()
        >>> s.longestOnes([1,1,1,0,0,0,1,1,1,1,0], 2)
        6
        >>> s.longestOnes([0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], 3)
        10
        """
        n = len(nums)
        l = 0
        zero_count = 0
        max_ones = 0
        
        for r in range(n):
            if nums[r] == 0:
                zero_count += 1
            
            # If zero_count exceeds k, adjust the left pointer `l`
            while zero_count > k:
                if nums[l] == 0:
                    zero_count -= 1
                l += 1
            
            # Update max_ones with the current window size
            max_ones = max(max_ones, r - l + 1)
        
        return max_ones

# Test cases
if __name__ == "__main__":
    s = Solution()
    
    # Test case 1
    assert s.longestOnes([1,1,1,0,0,0,1,1,1,1,0], 2) == 6
    
    # Test case 2
    assert s.longestOnes([0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], 3) == 10
    
    # Test case 3: All ones
    assert s.longestOnes([1,1,1,1,1], 0) == 5
    
    # Test case 4: All zeros
    assert s.longestOnes([0,0,0,0,0], 2) == 2
    
    # Test case 5: Empty array
    assert s.longestOnes([], 1) == 0
    
    print("All test cases passed!")