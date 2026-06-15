from typing import List


class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        """Minimum ship capacity to ship weights (in order) within `days` days.
        O(n log(sum)). Binary search ON THE ANSWER.

        Search the capacity space [max(weights), sum(weights)]:
          - low  = max(weights): capacity must fit the heaviest single package.
          - high = sum(weights): one capacity that ships everything in a single day.
        can_ship(cap) greedily counts days; it is monotonic (bigger ship -> fewer
        days), so capacities read F...F T...T and we want the first True.
        """
        def can_ship(capacity: int) -> bool:
            num_days, load = 1, 0          # already on day 1 before any reset (fencepost!)
            for w in weights:
                if load + w > capacity:    # w overflows today's load -> start a new day
                    num_days += 1
                    load = 0
                load += w
            return num_days <= days

        low, high = max(weights), sum(weights)
        while low < high:
            mid = (low + high) // 2
            if can_ship(mid):
                high = mid                 # mid works -> smallest feasible is mid or lower
            else:
                low = mid + 1              # too small
        return low


def test_solution():
    sol = Solution()
    assert sol.shipWithinDays([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5) == 15
    assert sol.shipWithinDays([3, 2, 2, 4, 1, 4], 3) == 6
    assert sol.shipWithinDays([1, 2, 3, 1, 1], 4) == 3
    assert sol.shipWithinDays([10], 1) == 10
    assert sol.shipWithinDays([1, 2, 3, 4, 5], 1) == 15      # one day -> need the whole sum
    print("All test cases passed!")


if __name__ == "__main__":
    test_solution()
