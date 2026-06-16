import heapq
from typing import List


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        """The k-th largest element (in sorted order, not distinct). O(n log k).

        Bounded min-heap of size k: push each number, and pop the smallest the
        moment the heap exceeds k. What survives is the k largest, and the root
        (the smallest of those) is the k-th largest. Keeping the heap at size k
        makes every op O(log k), not O(log n), and works on a stream.
        """
        heap = []
        for num in nums:
            heapq.heappush(heap, num)
            if len(heap) > k:
                heapq.heappop(heap)        # evict the smallest, keep the k largest
        return heap[0]

    def findKthLargest_pushpop(self, nums: List[int], k: int) -> int:
        """Same idea, one op per element once the heap is full (heappushpop)."""
        heap = []
        for num in nums:
            if len(heap) < k:
                heapq.heappush(heap, num)
            else:
                heapq.heappushpop(heap, num)   # push then pop-smallest in one step
        return heap[0]


if __name__ == "__main__":
    solution = Solution()
    test_cases = [
        ([3, 2, 1, 5, 6, 4], 2, 5),
        ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, 4),
        ([1], 1, 1),
        ([7, 7, 7], 2, 7),
        ([2, 1], 2, 1),
    ]
    for nums, k, expected in test_cases:
        assert solution.findKthLargest(nums[:], k) == expected, f"heap: {nums}, {k}"
        assert solution.findKthLargest_pushpop(nums[:], k) == expected, f"pushpop: {nums}, {k}"
    print("All tests passed.")
