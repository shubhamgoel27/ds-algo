"""
Put Boxes Into the Warehouse II (LeetCode 1580)  ·  Pinterest-tagged
====================================================================
Like Warehouse I, but boxes can enter from EITHER end. Reorder boxes freely,
one box per room. Return the max number placeable.

TRANSFORM (the twist vs I):
  A box chooses the more forgiving entrance, so room i's usable height is
      effective[i] = max( leftMin[i], rightMin[i] )
  leftMin  = prefix min of warehouse   (non-increasing)
  rightMin = suffix min of warehouse   (non-decreasing)
  In I it was leftMin alone -> a non-increasing corridor. Here it's the MAX,
  which is a VALLEY (sinks to the single crossover of the two curves, rises).

TECHNIQUE: the effective array is no longer monotonic, so the corridor sweep
from I doesn't apply. But every effective[i] is a room's reachability capacity,
so sort effective + sort boxes + greedy two-pointer match (smallest box to
smallest capacity that fits).

WHY SORTING IS SAFE (the subtle part -- these capacities are simultaneously
realizable, so rooms are truly independent):
  1. Fill each side DEEPEST-FIRST: when you push a box in, the rooms it passes
     are still empty (filled later), so no collision with a placed box.
  2. leftMin (non-increasing) and rightMin (non-decreasing) cross exactly ONCE.
     Left of the crossover, effective = leftMin (serve from left); right of it,
     effective = rightMin (serve from right). Left fills a contiguous prefix,
     right a contiguous suffix -> they never overlap.
  => all effective[i] hold at once -> independent capacities -> sort + greedy
     match is optimal (exchange argument).

Time O(n log n + m log m), space O(m).
"""
from typing import List


class Solution:
    def maxBoxesInWarehouse(self, boxes: List[int], warehouse: List[int]) -> int:
        n = len(warehouse)
        left = warehouse[:]
        right = warehouse[:]
        for i in range(1, n):
            left[i] = min(left[i - 1], warehouse[i])       # prefix min
        for i in range(n - 2, -1, -1):
            right[i] = min(right[i + 1], warehouse[i])      # suffix min
        eff = sorted(max(left[i], right[i]) for i in range(n))

        boxes.sort()
        count = b = r = 0
        while b < len(boxes) and r < n:
            if boxes[b] <= eff[r]:      # compare against sorted effective heights (not raw warehouse)
                count += 1
                b += 1
            r += 1
        return count


def run_tests():
    s = Solution()
    assert s.maxBoxesInWarehouse([1, 2, 2, 3, 4], [3, 4, 1, 2]) == 4
    assert s.maxBoxesInWarehouse([3, 5, 5, 2], [2, 1, 3, 4, 5]) == 3
    assert s.maxBoxesInWarehouse([1, 2, 3], [1, 2, 3, 4]) == 3
    assert s.maxBoxesInWarehouse([9], [1]) == 0
    assert s.maxBoxesInWarehouse([1], [9]) == 1
    assert s.maxBoxesInWarehouse([2, 2], [1, 2, 1]) == 0   # middle room flanked by 1s -> eff 1 everywhere
    assert s.maxBoxesInWarehouse([2, 2], [2, 1, 2]) == 2   # both ends win: room0 from left, room2 from right
    print("All test cases passed!")


run_tests()

# Hints:
# 1. Two entrances -> effective[i] = MAX(prefixMin[i], suffixMin[i]) (a valley, not a corridor).
# 2. Not monotonic -> rooms become independent capacities -> sort eff + sort boxes + greedy match.
# 3. Compare boxes[b] <= eff[r], NOT warehouse[r] (use the derived array you sorted).
# 4. Safe because deepest-first insertion + single crossover => all capacities realizable at once.
