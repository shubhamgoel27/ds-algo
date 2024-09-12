from typing import List

class Solution:
    def maximumProduct(self, nums: List[int]) -> int:
        """
        Find the maximum product of three numbers in the given list.

        This function finds the maximum product that can be formed by multiplying
        three numbers from the given list. It considers both positive and negative numbers.

        Args:
            nums (List[int]): A list of integers.

        Returns:
            int: The maximum product of three numbers from the list.

        Time complexity: O(n), where n is the length of the input list.
        Space complexity: O(1), as we only use a constant amount of extra space.
        """
        max1 = max2 = max3 = float('-inf')
        min1 = min2 = float('inf')
        
        # Traverse the array once to find the three largest and two smallest numbers
        for num in nums:
            # Update the three largest numbers
            if num > max1:
                max3, max2, max1 = max2, max1, num
            elif num > max2:
                max3, max2 = max2, num
            elif num > max3:
                max3 = num
            
            # Update the two smallest numbers
            if num < min1:
                min2, min1 = min1, num
            elif num < min2:
                min2 = num
        
        # The maximum product is either from three largest numbers
        # or two smallest numbers (which could be negative) and the largest number
        return max(max1 * max2 * max3, min1 * min2 * max1)

# Test cases
def test_maximum_product():
    solution = Solution()
    
    # Test case 1: All positive numbers
    assert solution.maximumProduct([1, 2, 3, 4]) == 24
    
    # Test case 2: Mix of positive and negative numbers
    assert solution.maximumProduct([-1, -2, -3, 4, 5]) == 30
    
    # Test case 3: All negative numbers
    assert solution.maximumProduct([-5, -2, -1, -1]) == -2
    
    # Test case 4: Array with zeros
    assert solution.maximumProduct([-4, -3, 0, 2, 5]) == 60
    
    # Test case 5: Array with duplicate numbers
    assert solution.maximumProduct([3, 3, 3, 3]) == 27
    
    print("All test cases passed!")

# Run the test cases
test_maximum_product()

"""
Hints for solving this problem:

1. Consider both positive and negative numbers: The largest product might come from
   two large negative numbers multiplied by the largest positive number.

2. You don't need to sort the entire array: Focus on finding the three largest
   numbers and the two smallest numbers in a single pass.

3. Use variables to keep track of the largest and smallest numbers as you iterate
   through the list. This allows you to solve the problem in O(n) time complexity.

4. Remember to handle edge cases, such as when all numbers are negative or when
   there are zeros in the array.

5. The final step is to compare two possible products: the product of the three
   largest numbers, and the product of the two smallest numbers (which could be
   negative) multiplied by the largest number.

6. This problem can be solved in a single pass through the array, making it very
   efficient for large inputs.
"""