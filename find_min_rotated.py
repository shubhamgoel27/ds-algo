from typing import List


class Solution:
    def findMin(self, nums: List[int]) -> int:
        """Minimum of a rotated sorted array of distinct ints. O(log n).

        Boundary binary search (the keep-mid convention): find the first index
        in the "tail run" that contains the minimum. Predicate per index i:
        P(i) = nums[i] <= nums[high] (i.e. i is in the tail). The array reads
        F...F T...T and the first True is the minimum.

          - `while low < high`, converging to one element.
          - `nums[mid] > nums[high]` -> mid is in the upper run (False) -> go right.
          - else mid is in the tail (True), it might BE the min -> keep it: high = mid.

        Anchor on nums[high] because the tail (and thus the min) always ends at
        high, so high is guaranteed to be on the side we are hunting.
        """
        low, high = 0, len(nums) - 1
        while low < high:
            mid = (low + high) // 2
            if nums[mid] > nums[high]:
                low = mid + 1
            else:
                high = mid
        return nums[low]


if __name__ == "__main__":
    solution = Solution()
    test_cases = [
        ([3, 4, 5, 1, 2], 1),
        ([4, 5, 6, 7, 0, 1, 2], 0),
        ([11, 13, 15, 17], 11),     # not rotated
        ([1], 1),
        ([2, 1], 1),
        ([5, 1, 2, 3, 4], 1),
    ]
    for nums, expected in test_cases:
        result = solution.findMin(nums)
        assert result == expected, f"findMin({nums}) = {result}, expected {expected}"
    print("All tests passed.")
