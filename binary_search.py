from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        """Index of target in a sorted distinct array, else -1. O(log n).

        Closed-interval [low, high] convention, used consistently:
          - `while low <= high`  : [low, high] non-empty while low <= high, so
            the one-element window (low == high) still gets checked.
          - `low = mid + 1` / `high = mid - 1` : mid was already checked and is
            not the target, so exclude it (and guarantee progress, no infinite loop).
          - return -1 once the interval goes empty.
        Pick ONE interval convention and never mix it; that is what kills off-by-ones.
        """
        low, high = 0, len(nums) - 1
        while low <= high:
            mid = (low + high) // 2
            if nums[mid] == target:
                return mid
            if nums[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        return -1


if __name__ == "__main__":
    solution = Solution()
    test_cases = [
        ([-1, 0, 3, 5, 9, 12], 9, 4),
        ([-1, 0, 3, 5, 9, 12], 2, -1),
        ([], 5, -1),
        ([5], 5, 0),
        ([5], 3, -1),
        ([1, 2], 1, 0),
        ([1, 2], 2, 1),
        ([1, 3, 5, 7], 7, 3),
    ]
    for nums, target, expected in test_cases:
        result = solution.search(nums, target)
        assert result == expected, f"search({nums}, {target}) = {result}, expected {expected}"
    print("All tests passed.")
