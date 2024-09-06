import heapq 
from typing import List
import unittest

class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        """
        Find the k closest points to the origin (0, 0) in the plane.
        
        Args:
            points (List[List[int]]): A list of points on a plane, where each point is represented as [x, y].
            k (int): The number of closest points to return.
        
        Returns:
            List[List[int]]: The k closest points to the origin.
        
        Time complexity: O(n log k), where n is the number of points.
        Space complexity: O(k) for the heap.
        """
        heap = []
        for i, (x, y) in enumerate(points):
            dist = x**2 + y**2 
            heapq.heappush(heap, (dist, i))
        
        res = []
        for _ in range(k):
            dist, i = heapq.heappop(heap)
            res.append(points[i])
        return res

class TestSolution(unittest.TestCase):
    def setUp(self):
        self.solution = Solution()

    def test_case_1(self):
        points = [[1,3],[-2,2]]
        k = 1
        self.assertEqual(self.solution.kClosest(points, k), [[-2,2]])

    def test_case_2(self):
        points = [[3,3],[5,-1],[-2,4]]
        k = 2
        self.assertCountEqual(self.solution.kClosest(points, k), [[3,3],[-2,4]])

    def test_case_3(self):
        points = [[0,1],[1,0]]
        k = 2
        self.assertCountEqual(self.solution.kClosest(points, k), [[0,1],[1,0]])

if __name__ == "__main__":
    unittest.main()
