from typing import List
import heapq
from collections import Counter


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        """The k most frequent elements. O(n log k) time, O(n) space.

        Count frequencies, then it is top-k by frequency. We keep the k LARGEST
        frequencies, so the one on the chopping block is the SMALLEST kept
        frequency -> bounded MIN-heap of size k, evicting the least frequent.
        (Prod one-liner: [x for x, _ in Counter(nums).most_common(k)].)
        """
        count = Counter(nums)
        heap = []  # min-heap of (frequency, element), bounded to size k
        for element, freq in count.items():
            heapq.heappush(heap, (freq, element))
            if len(heap) > k:
                heapq.heappop(heap)        # evict the least frequent kept
        return [element for _, element in heap]


if __name__ == "__main__":
    solution = Solution()
    cases = [
        ([1, 1, 1, 2, 2, 3], 2, {1, 2}),
        ([1], 1, {1}),
        ([4, 4, 4, 5, 5, 6], 2, {4, 5}),
        ([5, 5, 5, 5], 1, {5}),
    ]
    for nums, k, expected in cases:
        got = set(solution.topKFrequent(nums[:], k))
        assert got == expected, f"topKFrequent({nums}, {k}) = {got}, expected {expected}"
    print("All tests passed.")
