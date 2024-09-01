from typing import List

class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        """
        Count the number of subarrays that sum to k.

        Args:
            nums (List[int]): The input array of integers.
            k (int): The target sum.

        Returns:
            int: The number of subarrays that sum to k.

        Time complexity: O(n), where n is the length of nums.
        Space complexity: O(n) in the worst case.
        """
        from collections import defaultdict
        prefix_sum = defaultdict(int)
        prefix_sum[0] = 1
        count = 0
        currsum = 0 
        for i in range(len(nums)):
            currsum += nums[i]
            if currsum - k in prefix_sum:
                count += prefix_sum[currsum-k]
            prefix_sum[currsum] += 1 
        return count 

# Tests
import unittest

class TestSolution(unittest.TestCase):
    def setUp(self):
        self.solution = Solution()

    def test_example_1(self):
        self.assertEqual(self.solution.subarraySum([1,1,1], 2), 2)

    def test_example_2(self):
        self.assertEqual(self.solution.subarraySum([1,2,3], 3), 2)

    def test_empty_array(self):
        self.assertEqual(self.solution.subarraySum([], 0), 0)

    def test_single_element(self):
        self.assertEqual(self.solution.subarraySum([5], 5), 1)

    def test_negative_numbers(self):
        self.assertEqual(self.solution.subarraySum([-1,-1,1], 0), 1)

if __name__ == "__main__":
    unittest.main()
