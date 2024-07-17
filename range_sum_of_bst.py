import unittest
from typing import Optional
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def rangeSumBST(self, root: Optional[TreeNode], low: int, high: int) -> int:
        if root is None:
            return 0
        
        if root.val > low and root.val > high:
            return self.rangeSumBST(root.left, low, high)
        
        if root.val < low and root.val < high:
            return self.rangeSumBST(root.right, low, high)
        
        else:
            return root.val + self.rangeSumBST(root.left, low, high) + self.rangeSumBST(root.right, low, high)
        
class TestRangeSumBST(unittest.TestCase):
    def test_empty_tree(self):
        solution = Solution()
        self.assertEqual(solution.rangeSumBST(None, 1, 10), 0)
    
    def test_single_node_in_range(self):
        solution = Solution()
        root = TreeNode(5)
        self.assertEqual(solution.rangeSumBST(root, 1, 10), 5)

    def test_single_node_out_of_range(self):
        solution = Solution()
        root = TreeNode(5)
        self.assertEqual(solution.rangeSumBST(root, 6, 10), 0)

    def test_all_nodes_in_range(self):
        solution = Solution()
        root = TreeNode(10, TreeNode(5), TreeNode(15))
        self.assertEqual(solution.rangeSumBST(root, 5, 15), 30)

    def test_some_nodes_in_range(self):
        solution = Solution()
        root = TreeNode(10, TreeNode(5), TreeNode(15))
        self.assertEqual(solution.rangeSumBST(root, 7, 15), 25)

    def test_no_nodes_in_range(self):
        solution = Solution()
        root = TreeNode(10, TreeNode(5), TreeNode(15))
        self.assertEqual(solution.rangeSumBST(root, 20, 30), 0)

    def test_complex_tree(self):
        solution = Solution()
        root = TreeNode(10, 
                        TreeNode(5, TreeNode(3), TreeNode(7)),
                        TreeNode(15, None, TreeNode(18)))
        self.assertEqual(solution.rangeSumBST(root, 7, 15), 32)

if __name__ == '__main__':
    unittest.main()