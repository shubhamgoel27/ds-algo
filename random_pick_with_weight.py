import random
from typing import List
import math

class Solution:
    """
    A class that implements weighted random picking.

    This class allows you to initialize with a list of weights and then
    randomly pick an index based on those weights.
    """

    def __init__(self, w: List[int]):
        """
        Initialize the Solution with a list of weights.

        Args:
            w (List[int]): A list of non-negative integers representing weights.
        """
        self.w = w
        self.cumsum = []
        self.total = 0
        # Calculate cumulative sum for efficient picking
        for weight in self.w:
            self.total += weight
            self.cumsum.append(self.total)

    def pickIndex(self) -> int:
        """
        Randomly pick an index based on the weights.

        Returns:
            int: The randomly picked index.
        """
        n = len(self.cumsum)
        l, r = 0, n - 1
        # Generate a random number between 1 and total weight
        random_num = random.randint(1, self.total)
        
        # Binary search to find the index
        while l < r:
            mid = (l + r) // 2
            if random_num <= self.cumsum[mid]:
                r = mid
            else:
                l = mid + 1
        return l

def test_solution():
    def run_test(weights, num_picks=100000):
        sol = Solution(weights)
        picks = [sol.pickIndex() for _ in range(num_picks)]
        observed = [picks.count(i) for i in range(len(weights))]
        expected = [num_picks * w / sum(weights) for w in weights]
        
        print(f"Weights: {weights}")
        print(f"Observed: {observed}")
        print(f"Expected: {[round(e) for e in expected]}")
        
        # Calculate percentage difference
        diff = [abs(o - e) / e * 100 for o, e in zip(observed, expected)]
        avg_diff = sum(diff) / len(diff)
        
        print(f"Average percentage difference: {avg_diff:.2f}%")
        print(f"Test {'passed' if avg_diff < 5 else 'failed'}")
        print()

    # Test case 1: Equal weights
    run_test([1, 1, 1, 1])

    # Test case 2: Unequal weights
    run_test([1, 3, 2, 4])

    # Test case 3: Extreme weights
    run_test([1, 99])

    # Test case 4: Many weights
    run_test([i for i in range(1, 11)])  # weights from 1 to 10

    # Test case 5: Single weight
    run_test([42])

if __name__ == "__main__":
    test_solution()

# Hints for future self:
# 1. The key idea is to use cumulative sum and binary search.
# 2. Think of the weights as ranges on a number line.
# 3. The cumulative sum helps in quickly determining which range a random number falls into.
# 4. Binary search is used for efficient lookup in the cumulative sum array.
# 5. Time complexity: O(n) for initialization, O(log n) for each pick.
# 6. Space complexity: O(n) for storing the cumulative sum array.