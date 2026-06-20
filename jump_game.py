from typing import List


class Solution:
    def canJump(self, nums: List[int]) -> bool:
        """Can you reach the last index? nums[i] = max jump from i. O(n) time, O(1) space.

        Greedy / furthest-reach: track `furthest`, the farthest index reachable so
        far. Reachability is contiguous (you can jump short), so the only failure
        is a gap: standing on an index i > furthest means you could never get here.
        Collapses an O(n^2) reachability DP into one number.
        """
        furthest = 0
        for i in range(len(nums)):
            if i > furthest:                 # can't even reach index i -> stuck
                return False
            furthest = max(furthest, i + nums[i])
        return True


if __name__ == "__main__":
    solution = Solution()
    cases = [
        ([2, 3, 1, 1, 4], True),
        ([3, 2, 1, 0, 4], False),
        ([0], True),
        ([0, 1], False),
        ([1, 0, 1], False),
        ([2, 0, 0], True),
    ]
    for nums, expected in cases:
        assert solution.canJump(nums[:]) == expected, f"{nums}"
    print("All tests passed.")
