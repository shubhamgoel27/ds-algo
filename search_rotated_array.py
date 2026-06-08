from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        """Index of target in a rotated ascending (distinct) array, else -1. O(log n).

        Single binary search. At every step at least one of the two halves
        [lo..mid] / [mid..hi] is cleanly sorted (the pivot lives in the other).
        Identify the sorted half, and if target falls inside its known value
        range, search there; otherwise search the other half.

        The two operators that make-or-break this:
          - `nums[lo] <= nums[mid]` is INCLUSIVE so the mid==lo case (window of
            size 1-2) counts as "left sorted" instead of falling through.
          - the range checks bracket target against the sorted half's endpoints.

        Time: O(log n). Space: O(1)  -- no slicing, so the log-n bound holds.
        """
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return mid
            if nums[lo] <= nums[mid]:                 # left half is sorted
                if nums[lo] <= target < nums[mid]:    # target inside sorted left
                    hi = mid - 1
                else:
                    lo = mid + 1
            else:                                     # right half is sorted
                if nums[mid] < target <= nums[hi]:    # target inside sorted right
                    lo = mid + 1
                else:
                    hi = mid - 1
        return -1


if __name__ == "__main__":
    solution = Solution()
    test_cases = [
        ([4, 5, 6, 7, 0, 1, 2], 0, 4),
        ([4, 5, 6, 7, 0, 1, 2], 3, -1),
        ([4, 5, 6, 7, 0, 1, 2], 4, 0),
        ([4, 5, 6, 7, 0, 1, 2], 5, 1),
        ([1], 0, -1),
        ([1], 1, 0),
        ([3, 1], 1, 1),                 # 2-element rotation (the mid==lo trap)
        ([5, 1, 2, 3, 4], 1, 1),
        ([6, 7, 0, 1, 2, 4, 5], 3, -1),
        ([1, 2, 3, 4, 5], 6, -1),
    ]
    for nums, target, expected in test_cases:
        result = solution.search(nums, target)
        assert result == expected, f"Failed search({nums}, {target}): expected {expected}, got {result}"

    # fuzz against a linear-scan reference over many rotations
    import random
    random.seed(0)
    for _ in range(5000):
        k = random.randint(1, 9)
        base = sorted(random.sample(range(30), k))
        r = random.randint(0, k - 1)
        arr = base[r:] + base[:r]
        t = random.randint(-2, 30)
        ref = arr.index(t) if t in arr else -1
        assert solution.search(arr, t) == ref, f"Fuzz fail: {arr}, {t}"

    print("All tests passed.")
