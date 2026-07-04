"""
Kth Largest Element in a Stream (LeetCode 703)
==============================================
Track the k-th largest element (including duplicates) as values stream in.

Key inversion: to track the k-th LARGEST, keep a MIN-heap of size k. The heap
holds the k biggest elements seen; its root (the smallest of those k) IS the
k-th largest. Anything smaller than the root can't be top-k, so it's discarded.

Bounded heap = O(k) memory even on an infinite stream. add() is O(log k).

Two mechanical traps (both cost a fuzz round here):
  - push THEN trim: settle the heap back to size k before reading the root.
  - no aliasing: build into a fresh list, don't mutate the input while iterating.

Sister framing (same mechanics): append_pins_to_shortest_column below.
"""
import heapq
from typing import List


class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.nums = []                         # fresh list -> no aliasing of input
        for x in nums:                         # iterate input, push into a different list
            heapq.heappush(self.nums, x)
            if len(self.nums) > k:
                heapq.heappop(self.nums)

    def add(self, val: int) -> int:
        heapq.heappush(self.nums, val)         # add first
        if len(self.nums) > self.k:            # then trim back to size k
            heapq.heappop(self.nums)
        return self.nums[0]                     # root of a size-k min-heap = k-th largest


def append_pins_to_shortest_column(heights: List[int], pins: List[int]) -> List[int]:
    """Pinterest framing of the same min-heap drill: place each pin onto the
    currently shortest column (ties -> lowest index). Return final heights."""
    heap = [(h, i) for i, h in enumerate(heights)]
    heapq.heapify(heap)
    for pin in pins:
        h, i = heapq.heappop(heap)
        heapq.heappush(heap, (h + pin, i))
    result = [0] * len(heights)
    for h, i in heap:
        result[i] = h
    return result


def run_tests():
    kth = KthLargest(3, [4, 5, 8, 2])
    assert kth.add(3) == 4
    assert kth.add(5) == 5
    assert kth.add(10) == 5
    assert kth.add(9) == 8
    assert kth.add(4) == 8

    k2 = KthLargest(1, [])                      # starts empty, fills up
    assert k2.add(-3) == -3
    assert k2.add(-2) == -2
    assert k2.add(-4) == -2

    k3 = KthLargest(2, [0])
    assert k3.add(-1) == -1
    assert k3.add(1) == 0
    assert k3.add(-2) == 0
    assert k3.add(3) == 1

    assert append_pins_to_shortest_column([0, 0, 0], [3, 1, 2]) == [3, 1, 2]
    assert append_pins_to_shortest_column([5, 1, 3], [2, 2]) == [5, 5, 3]
    assert append_pins_to_shortest_column([2, 2], [1, 1, 1]) == [4, 3]
    print("All test cases passed!")


run_tests()

# Hints:
# 1. k-th LARGEST -> MIN-heap of size k; root is the answer.
# 2. add: push, then pop if size > k, then return root (order matters).
# 3. Build init into a fresh list; never mutate the list you iterate by index.
# 4. Optimized add once full: if val > heap[0]: heapreplace(heap, val).
