from typing import List


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        """Largest-sum contiguous subarray (Kadane's). O(n) time, O(1) space.

        Greedy: keep a `running` sum; the instant it goes negative, reset to 0,
        because a negative prefix can only drag down whatever follows (exchange
        argument). Record `best` BEFORE the reset so an all-negative array still
        keeps its least-negative element. This is the DP dp[i]=max(nums[i],
        dp[i-1]+nums[i]) collapsed to O(1) space.
        """
        running = 0
        best = -float("inf")
        for x in nums:
            running += x
            best = max(best, running)        # record BEFORE the reset
            if running < 0:
                running = 0
        return best


if __name__ == "__main__":
    solution = Solution()
    cases = [
        ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6),
        ([5, 4, -1, 7, 8], 23),
        ([-3, -1, -2], -1),       # all negative -> least-negative element
        ([1], 1),
        ([-5], -5),
    ]
    for nums, expected in cases:
        assert solution.maxSubArray(nums[:]) == expected, f"{nums}"
    print("All tests passed.")
