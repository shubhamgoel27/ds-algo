"""
Put Boxes Into the Warehouse I (LeetCode 1564)  ·  Pinterest-tagged
==================================================================
Boxes (heights) pushed into a corridor of rooms from the LEFT; each room holds
one box; a box must fit under EVERY room it passes on the way in. Boxes can be
reordered. Return the max number of boxes placeable.

Pattern = TRANSFORM + TECHNIQUE (not DP):
  1. Transform: a box reaching room j had to pass rooms 0..j, so room j's usable
     height is the PREFIX MINIMUM of the warehouse. That array is non-increasing.
  2. Technique: sort boxes; greedy two-pointer. Match the smallest box to the
     deepest (smallest) room, walking both inward.

Why greedy is safe (exchange argument): take the smallest remaining box vs the
smallest remaining room. If it doesn't fit, NO box fits -> that room is dead
weight, skip it. If it fits, using the smallest box here is never worse (save
bigger boxes for bigger rooms still ahead).

Time O(n log n + m), space O(m).
"""
from typing import List


class Solution:
    def maxBoxesInWarehouse(self, boxes: List[int], warehouse: List[int]) -> int:
        boxes.sort()
        eff = warehouse[:]                       # effective heights = prefix min
        for i in range(1, len(eff)):
            eff[i] = min(eff[i - 1], warehouse[i])

        total = 0
        box = 0                                  # smallest box
        room = len(warehouse) - 1                # deepest (smallest) room
        while box < len(boxes) and room >= 0:
            if boxes[box] <= eff[room]:
                total += 1
                box += 1                         # advance box ONLY on a fit
            room -= 1                            # always try a bigger room next
        return total


def run_tests():
    s = Solution()
    assert s.maxBoxesInWarehouse([4, 3, 4, 1], [5, 3, 3, 4, 1]) == 3
    assert s.maxBoxesInWarehouse([1, 2, 2, 3, 4], [3, 4, 1, 2]) == 3
    assert s.maxBoxesInWarehouse([1, 2, 3], [1, 2, 3, 4]) == 1
    assert s.maxBoxesInWarehouse([9], [1]) == 0            # tallest box, shortest room
    assert s.maxBoxesInWarehouse([1], [9]) == 1
    assert s.maxBoxesInWarehouse([2, 2, 2], [2, 2, 2]) == 3
    print("All test cases passed!")


run_tests()

# Hints:
# 1. NOT DP. "reorder freely" + "max count that fit" -> sort + greedy.
# 2. "must fit past every earlier room" = cumulative constraint -> prefix MIN
#    (non-increasing effective heights).
# 3. while-loop with a box pointer: advance box only on a fit, always shrink room.
#    (A for-each can't retry the same box in a bigger room -- that was the bug.)
