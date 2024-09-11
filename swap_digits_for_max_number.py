class Solution:
    def maximumSwap(self, num: int) -> int:
        """
        Swap two digits in the given number to create the maximum possible value.
        
        Args:
            num (int): The input number.
        
        Returns:
            int: The maximum number after at most one swap.
        
        Time complexity: O(n), where n is the number of digits in num.
        Space complexity: O(n) for the digit list and last occurrence dictionary.
        """
        # Convert number to a list of digits
        num_digits = list(map(int, str(num)))
        
        # Store the last occurrence of each digit
        last = {digit: i for i, digit in enumerate(num_digits)}

        for i, digit in enumerate(num_digits):
            # Check for larger digits from 9 down to current digit
            for d in range(9, digit, -1):
                if last.get(d, -1) > i:
                    # Swap the current digit with the larger digit found later
                    num_digits[i], num_digits[last[d]] = num_digits[last[d]], num_digits[i]
                    # Convert back to integer and return
                    return int(''.join(map(str, num_digits)))

        # If no swap is made, return the original number
        return num

# Test cases
def test_maximum_swap():
    solution = Solution()
    assert solution.maximumSwap(2736) == 7236
    assert solution.maximumSwap(9973) == 9973
    assert solution.maximumSwap(1993) == 9913
    assert solution.maximumSwap(98368) == 98863
    print("All test cases passed!")

test_maximum_swap()

"""
Hints for solving this problem:

1. Think about how to identify the best swap: 
   - Look for a larger digit that appears later in the number.

2. Efficiency considerations:
   - Instead of repeatedly searching for larger digits, consider pre-computing
     the last occurrence of each digit.

3. Iteration strategy:
   - Iterate through the number from left to right, as earlier swaps are more significant.

4. Early termination:
   - Once a valid swap is found, you can immediately return the result.

5. Edge cases:
   - Consider what happens if the number is already the maximum possible.

6. Data structure choice:
   - Using a list of digits allows for easy swapping and reconstruction.

Remember: The goal is to make at most one swap to maximize the number!
"""