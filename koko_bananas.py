from typing import List


class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        """Minimum integer eating speed to finish all piles within h hours. O(n log(max)).

        Binary search ON THE ANSWER: there is no array to scan; you search the
        space of possible speeds [1, max(piles)] and test feasibility at each.
        feasible(speed) is monotonic (faster is never worse), so speeds read
        F...F T...T and we want the FIRST True (smallest feasible speed).
        """
        def feasible(speed: int) -> bool:
            # hours = sum of ceil(pile / speed), integer math to avoid float error
            hours = sum((pile + speed - 1) // speed for pile in piles)
            return hours <= h

        low, high = 1, max(piles)
        while low < high:
            mid = (low + high) // 2
            if feasible(mid):
                high = mid            # mid works -> smallest feasible is mid or lower
            else:
                low = mid + 1         # too slow
        return low


if __name__ == "__main__":
    solution = Solution()
    test_cases = [
        ([3, 6, 7, 11], 8, 4),
        ([30, 11, 23, 4, 20], 5, 30),
        ([30, 11, 23, 4, 20], 6, 23),
        ([1], 1, 1),
        ([1000000000], 2, 500000000),     # large-value (integer ceil matters)
    ]
    for piles, h, expected in test_cases:
        result = solution.minEatingSpeed(piles, h)
        assert result == expected, f"minEatingSpeed({piles}, {h}) = {result}, expected {expected}"
    print("All tests passed.")
