import heapq
from typing import List


class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        """The k points closest to the origin. O(n log k) time, O(k) space.

        Bounded MAX-heap of size k. We are keeping the k SMALLEST distances, so
        the one "on the chopping block" is the LARGEST kept distance -> the heap
        root must be the farthest -> a max-heap. Python heapq is a min-heap, so
        we push the NEGATED distance to invert it. Skip sqrt: x^2 + y^2 preserves
        ordering. The (-dist, i) tuple uses the index as a tiebreaker so the heap
        never has to compare the point lists.
        """
        heap = []  # max-heap by distance, via negation: (-dist, index)
        for i, (x, y) in enumerate(points):
            dist = x * x + y * y
            heapq.heappush(heap, (-dist, i))
            if len(heap) > k:
                heapq.heappop(heap)        # evict the farthest kept point
        return [points[i] for _, i in heap]


def _dist_multiset(pts):
    return sorted(x * x + y * y for x, y in pts)


if __name__ == "__main__":
    solution = Solution()
    cases = [
        ([[1, 3], [-2, 2]], 1),
        ([[3, 3], [5, -1], [-2, 4]], 2),
        ([[0, 1], [1, 0]], 2),
        ([[1, 1]], 1),
    ]
    for points, k in cases:
        got = solution.kClosest([p[:] for p in points], k)
        expected = sorted(points, key=lambda p: p[0] ** 2 + p[1] ** 2)[:k]
        assert len(got) == k and _dist_multiset(got) == _dist_multiset(expected), f"{points}, k={k}"
    print("All tests passed.")
