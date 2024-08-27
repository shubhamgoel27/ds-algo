from collections import defaultdict, deque
from typing import List, Optional
import unittest

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def verticalOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        d = defaultdict(list)
        if root is None:
            return [] 
        q = deque()
        q.append((root,0))
        left, right = 0, 0 
        while q:
            node, level = q.popleft()
            d[level].append(node.val)
            if node.left:
                left = min(left, level-1)
                q.append((node.left, level-1))
            if node.right:
                right = max(right, level+1)
                q.append((node.right, level+1))
        final = []
        for i in range(left, right+1):
            final.append(d[i])
        return final 

# Test cases
class TestVerticalOrder(unittest.TestCase):
    def setUp(self):
        self.solution = Solution()

    def test_empty_tree(self):
        self.assertEqual(self.solution.verticalOrder(None), [])

    def test_single_node(self):
        root = TreeNode(1)
        self.assertEqual(self.solution.verticalOrder(root), [[1]])

    def test_basic_tree(self):
        root = TreeNode(3)
        root.left = TreeNode(9)
        root.right = TreeNode(20)
        root.right.left = TreeNode(15)
        root.right.right = TreeNode(7)
        self.assertEqual(self.solution.verticalOrder(root), [[9], [3, 15], [20], [7]])

    def test_complex_tree(self):
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        root.left.left = TreeNode(4)
        root.left.right = TreeNode(5)
        root.right.left = TreeNode(6)
        root.right.right = TreeNode(7)
        self.assertEqual(self.solution.verticalOrder(root), [[4], [2], [1, 5, 6], [3], [7]])

    def test_unbalanced_tree(self):
        root = TreeNode(3)
        root.left = TreeNode(9)
        root.right = TreeNode(8)
        root.left.left = TreeNode(4)
        root.left.right = TreeNode(0)
        root.right.left = TreeNode(1)
        root.right.right = TreeNode(7)
        root.left.right.left = TreeNode(5)
        root.right.left.right = TreeNode(2)
        self.assertEqual(self.solution.verticalOrder(root), [[4], [9, 5], [3, 0, 1], [8, 2], [7]])

if __name__ == '__main__':
    unittest.main()

