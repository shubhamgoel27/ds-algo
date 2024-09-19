from typing import List

class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        """
        Find the minimum capacity of the ship that can ship all packages within the given number of days.

        Args:
        weights (List[int]): A list of package weights.
        days (int): The number of days to ship all packages.

        Returns:
        int: The minimum capacity of the ship.

        Time complexity: O(n * log(sum(weights)))
        Space complexity: O(1)
        """
        def can_ship(capacity: int) -> bool:
            """Check if all packages can be shipped within the given days using the specified capacity."""
            ships = 1
            curr_load = 0
            for weight in weights:
                if curr_load + weight > capacity:
                    ships += 1
                    curr_load = 0
                curr_load += weight
            return ships <= days

        # Binary search boundaries
        left, right = max(weights), sum(weights)

        while left < right:
            mid = (left + right) // 2
            if can_ship(mid):
                right = mid  # Try a smaller capacity
            else:
                left = mid + 1  # Need a larger capacity

        return left

# Test cases
def test_solution():
    sol = Solution()
    assert sol.shipWithinDays([1,2,3,4,5,6,7,8,9,10], 5) == 15
    assert sol.shipWithinDays([3,2,2,4,1,4], 3) == 6
    assert sol.shipWithinDays([1,2,3,1,1], 4) == 3
    print("All test cases passed!")

test_solution()

"""
Hints for solving this problem:

1. Think about the range of possible ship capacities:
   - Minimum: the weight of the heaviest package
   - Maximum: the sum of all package weights

2. Use binary search to find the minimum capacity:
   - For each capacity, check if it's possible to ship all packages within the given days
   - If possible, try a smaller capacity; if not, try a larger capacity

3. To check if a capacity is feasible:
   - Simulate the shipping process
   - Keep track of the current ship's load and the number of ships used
   - If the number of ships exceeds the given days, the capacity is too small

4. The binary search will converge to the minimum feasible capacity

5. Time complexity analysis:
   - Binary search takes O(log(sum(weights))) iterations
   - Each iteration checks all weights, which is O(n)
   - Total: O(n * log(sum(weights)))

6. Practice similar problems involving binary search on a range of values
"""
