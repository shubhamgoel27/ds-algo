import unittest
from typing import List
from collections import defaultdict, deque

class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        """
        Returns the order of courses to take given the number of courses and their prerequisites.

        Args:
            numCourses (int): Total number of courses.
            prerequisites (List[List[int]]): List of prerequisite pairs where the second course is required before the first.

        Returns:
            List[int]: A list representing the order of courses, or an empty list if it's not possible to finish all courses.
        """
        # Create a graph and in-degree array
        graph = defaultdict(list)
        in_degree = [0] * numCourses
        
        # Build the graph and in-degree count
        for course, req in prerequisites:
            graph[req].append(course)
            in_degree[course] += 1

        # Initialize the queue with courses that have no prerequisites
        q = deque([i for i in range(numCourses) if in_degree[i] == 0])
        final_order = []

        # Process the courses
        while q:
            course = q.popleft()
            final_order.append(course)

            # Decrease in-degree for neighbors and add to queue if they have no prerequisites left
            for n in graph[course]:
                in_degree[n] -= 1
                if in_degree[n] == 0:
                    q.append(n)

        # Check if all courses are taken
        return final_order if len(final_order) == numCourses else []

# Unit tests
class TestSolution(unittest.TestCase):
    def setUp(self):
        self.solution = Solution()

    def test_findOrder(self):
        self.assertIn(self.solution.findOrder(4, [[1, 0], [2, 1], [3, 2]]), [[0, 1, 2, 3], [0, 2, 1, 3], [1, 2, 3, 0], [0, 3, 1, 2]])  # Valid orders
        self.assertEqual(self.solution.findOrder(2, [[1, 0]]), [0, 1])  # Expected output: [0, 1]
        self.assertEqual(self.solution.findOrder(3, [[0, 1], [1, 0]]), [])  # Expected output: [] (cycle detected)

if __name__ == "__main__":
    unittest.main()

# Hints for future reference:
# 1. Understand the concept of topological sorting in directed graphs.
# 2. Familiarize yourself with Kahn's algorithm for topological sorting.
# 3. Consider edge cases like cycles in the graph and how they affect course completion.
# 4. Practice with different graph representations (adjacency list vs. matrix).
